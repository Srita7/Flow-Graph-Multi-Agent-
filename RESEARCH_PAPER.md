# Multi-Agent Program Repair via Code-Block Graphs: An In-Depth Study

## Abstract

This paper presents an in-depth study of a multi-agent automated program repair (APR) system that repairs buggy Python code through a structured, graph-based pipeline. The system employs four specialized agents: (1) a code-block graph builder that converts source code into block-level directed graphs using AST analysis and optional LLM fallback; (2) a semantic fault detector that identifies faulty nodes using relation-driven patterns and a large language model (LLM); (3) a graph rectification agent that applies minimal structural repairs to the graph; and (4) a source code reconstruction agent that maps the repaired graph back to fixed Python. The pipeline is evaluated on buggy snippets from real-world libraries (pandas, FastAPI, matplotlib, Keras, spaCy) using Levenshtein distance, cosine similarity, and line-edit distance. We detail each agent’s role, implementation, usage, real-life applicability, and what makes this project distinctive in the landscape of automated program repair and multi-agent systems.

**Keywords:** Automated Program Repair, Multi-Agent Systems, Code Representation, Fault Localization, Graph-Based Repair, LLM, Gemini, Python, Semantic Analysis.

---

## 1. Introduction

### 1.1 Problem and Motivation

Software defects—bugs—are costly. Locating and fixing them manually is time-consuming and error-prone. **Automated Program Repair (APR)** aims to generate patches for buggy code with minimal human intervention. Traditional APR often operates at the level of source text or patches, which can lead to overfitting, unnecessary changes, or loss of program structure. Representing code as a **structured graph** (nodes = code blocks, edges = relationships) allows reasoning about *semantic* and *structural* faults—such as broken data flow, unreachable code, or circular dependencies—and applying **minimal, targeted repairs** before regenerating source.

This project implements a **multi-agent pipeline** where each agent has a single, well-defined responsibility: build the graph, detect faults, repair the graph, then reconstruct code. Such a design improves interpretability, allows independent improvement of each stage, and constrains the LLM to surgical edits rather than full-file rewrites.

### 1.2 Research Questions Addressed

- **What do the agents do?** — We provide a precise description of each agent’s input, output, and behavior.
- **How are they implemented?** — We document the technical stack, algorithms, and LLM prompts.
- **How are they useful?** — We explain the value of graph-based fault detection and minimal repair.
- **How is the system used in real-life scenarios?** — We describe deployment contexts and benchmark libraries.
- **What makes this project special?** — We highlight the relation-driven semantic model, multi-agent decomposition, and graph-first repair strategy.

---

## 2. Background and Related Concepts

### 2.1 Automated Program Repair (APR)

APR systems typically: (1) **localize** the fault (where is the bug?), (2) **generate** a patch (what change fixes it?), and (3) **validate** the patch (does the program pass tests?). This project focuses on *semantic-structural* fault localization and repair using a graph representation, with evaluation based on textual similarity and edit distance between original and repaired code.

### 2.2 Code as a Graph

Code can be represented as graphs (e.g., AST, CFG, PDG, dependency graphs). Here, the representation is **block-level**: nodes are logical blocks (functions, classes, assignments, returns, calls, control structures), and edges are typed relationships:

- **contains** — hierarchy (e.g., function contains assignment).
- **data_flow** — dependency (e.g., assignment feeds return).
- **control_flow** — sequencing/branching (e.g., if → assignment).
- **call** — invocation (e.g., function → call).

This allows the pipeline to reason about *relations* (e.g., “assignment has no data_flow to return”) rather than raw text.

### 2.3 Multi-Agent Design

Splitting the repair process into multiple agents has benefits:

- **Modularity:** Each agent can be tested and improved in isolation.
- **Interpretability:** Intermediate artifacts (graphs, fault lists, rectified graphs) are inspectable.
- **Constraint:** Later agents receive structured input (e.g., “fix only these nodes”), reducing LLM drift and over-editing.

---

## 3. System Overview and Architecture

### 3.1 Pipeline Data Flow

The system is a **linear pipeline** of four agents plus an evaluation step:

```
Source Code (.py)  →  Agent 1  →  Block Graph (.dot)
                                        ↓
Block Graph (.dot) →  Agent 2  →  Fault Analysis (JSON)
                                        ↓
Fault JSON + DOT   →  Agent 3  →  Rectified Graph (JSON + .dot)
                                        ↓
Original Code +    →  Agent 4  →  Repaired Source (.py)
Agent 3 JSON
                                        ↓
Original + Repaired → calculate.py → Similarity Results (JSON)
```

There is no single “run all” orchestrator; each stage is invoked manually in sequence. Paths (e.g., `pandas_input_path`, `pandas_agent1_graph`) are configured per script for different libraries.

### 3.2 Directory and Artifact Layout

| Stage        | Input Location                          | Output Location                               |
|-------------|------------------------------------------|-----------------------------------------------|
| Agent 1     | `input_path/<lib>_input_path/*.py`       | `agent1_output_graph/<lib>_agent1_graph/*.dot` |
| Agent 2     | `agent1_graph/<lib>_agent1_graph/*.dot`  | `agent2_results/<lib>_agent2_results/*.json`  |
| Agent 3     | Agent 2 JSON + same DOT folder           | `agent3_rectified_graph/<lib>_agent3_rectified_graph/` |
| Agent 4     | Original `.py` + Agent 3 JSON            | `agent4_output_code/<lib>_agent4_output_code/*.py` |
| Evaluation  | Original + Agent 4 `.py`                 | `results/<lib>_agent4_similarity_results.json` |

Naming convention: for a file `bug100.py`, the graph is `bug100.blocks_graph.dot`, Agent 2 output is `bug100.blocks_graph_agent2.json`, Agent 3 output is `bug100.blocks_graph_agent3_full.json`, and Agent 4 produces `bug100.py` in the output folder.

---

## 4. Algorithm: Integrated Pipeline and Agent Coordination

This section gives a formal algorithmic view of the entire approach and how the agents integrate.

### 4.0 Combined End-to-End Algorithm (Single Unified View)

The following is **one combined algorithm** that describes the full pipeline from buggy source code to repaired code and evaluation. All four agents and the evaluation step are inlined; artifact naming uses file stem \(s\) (e.g., for `bug100.py`, \(s = \texttt{bug100}\)).

**Algorithm 0: Multi-Agent Program Repair (combined, per file)**

```
Input:  source_file (e.g., bug100.py), paths for graph/results/rectified/output/results
Output: repaired_code, metrics

--- AGENT 1: Build block graph ---
1.  code ← READ_FILE(source_file)
2.  result ← AST_ANALYZE(code)                    // nodes + relationships (contains, data_flow, control_flow, call)
3.  if |result.nodes| < 3 then result ← GEMINI_BLOCK_GRAPH(code)
4.  G ← BUILD_DIGRAPH(result)
5.  G_dot ← WRITE_DOT(G, s + ".blocks_graph.dot")

--- AGENT 2: Detect faulty nodes ---
6.  G ← READ_DOT(G_dot)
7.  stats ← COMPUTE_GRAPH_STATS(G)                 // total_nodes, avg_degree, root, edge_types, preview
8.  fault_json ← GEMINI_JSON(FILL(AGENT2_PROMPT, stats))   // faulty_nodes[], fault_summary
9.  WRITE_JSON(fault_json, s + ".blocks_graph_agent2.json")

--- AGENT 3: Rectify graph ---
10. faulty_list ← fault_json.faulty_nodes
11. context ← BUILD_REPAIR_CONTEXT(faulty_list, G)  // faulty details + full graph DOT
12. rect_json ← GEMINI_JSON(FILL(AGENT3_PROMPT, context))
13. WRITE_JSON(rect_json, s + ".blocks_graph_agent3_full.json")
14. if rect_json.full_rectified_graph exists then WRITE_DOT(rect_json.full_rectified_graph, s + ".blocks_graph_repaired.dot")

--- AGENT 4: Reconstruct source ---
15. original_code ← READ_FILE(source_file)
16. repaired_code ← GEMINI_TEXT(FILL(AGENT4_PROMPT, original_code, rect_json.rectified_nodes, rect_json.full_rectified_graph))
17. WRITE_FILE(OUTPUT_DIR / name(source_file), repaired_code)

--- EVALUATION ---
18. metrics.levenshtein_distance ← LEVENSHTEIN(original_code, repaired_code)
19. metrics.cosine_similarity ← COSINE_3GRAM(original_code, repaired_code)
20. metrics.line_edit_distance ← LINE_EDIT_DISTANCE(original_code, repaired_code)
21. return repaired_code, metrics
```

**Summary:** Steps 1–5 (Agent 1) build the block graph; 6–9 (Agent 2) detect semantic faults; 10–14 (Agent 3) repair the graph; 15–17 (Agent 4) reconstruct Python; 18–21 compute similarity metrics. All agents are **chained by stem \(s\)**: same \(s\) links DOT, Agent 2 JSON, Agent 3 JSON, and the repaired file.

---

### 4.1 Master Pipeline Algorithm

The end-to-end process is a **sequential pipeline**: each agent consumes the output of the previous agent (and Agent 4 also consumes the original source). There is no feedback loop; execution is one-pass per file.

**Algorithm 1: Master pipeline (per file)**

```
Input:  source_file (e.g., bug100.py), INPUT_PATH, OUTPUT_PATHs for each stage
Output: repaired_file, similarity_metrics

1.  G_dot ← AGENT1_BUILD_GRAPH(source_file)           // Agent 1
2.  fault_json ← AGENT2_DETECT_FAULTS(G_dot)          // Agent 2
3.  rect_json, G_repaired_dot ← AGENT3_REPAIR_GRAPH(fault_json, G_dot)   // Agent 3
4.  repaired_code ← AGENT4_RECONSTRUCT_SOURCE(source_file, rect_json)    // Agent 4
5.  metrics ← EVALUATE(source_file, repaired_code)   // calculate.py
6.  return repaired_code, metrics
```

**Integration rule:** For a given source file with stem \(s\) (e.g., `bug100`), all artifacts share the same stem: graph `s.blocks_graph.dot`, Agent 2 output `s.blocks_graph_agent2.json`, Agent 3 output `s.blocks_graph_agent3_full.json`, and Agent 4 matches by \(s\) when loading the Agent 3 JSON. Thus the pipeline is **file-stem aligned** across agents.

### 4.2 Agent 1: Code-Block Graph Construction

**Algorithm 2: AGENT1_BUILD_GRAPH(source_file)**

```
Input:  source_file (path to .py)
Output: G_dot (path to .blocks_graph.dot)

1.  code ← READ_FILE(source_file)
2.  result ← AST_ANALYZE(code)     // CodeBlockVisitor: nodes + relationships
3.  if |result.nodes| < 3 then
4.      result ← GEMINI_BLOCK_GRAPH(code)   // LLM fallback, same schema
5.  G ← BUILD_DIGRAPH(result)      // NetworkX DiGraph from result.nodes, result.relationships
6.  G_dot ← WRITE_DOT(G, stem(source_file) + ".blocks_graph.dot")
7.  return G_dot
```

**AST_ANALYZE** (conceptual): Walk AST; for each FunctionDef, ClassDef, Assign, Return, Call, If, For, While, With, Try, create a node (id, type, start_line, end_line, code_snippet) and edges: `contains` from current function/class to new block, `control_flow` from previous block to current, `call` from function to call node. **BUILD_DIGRAPH** maps each node to a vertex and each relationship to a directed edge with attribute `label` ∈ {contains, data_flow, control_flow, call}.

### 4.3 Agent 2: Semantic Fault Detection

**Algorithm 3: AGENT2_DETECT_FAULTS(G_dot)**

```
Input:  G_dot (path to .dot from Agent 1)
Output: fault_json (dict: faulty_nodes, fault_summary, file_name, total_nodes, ...)

1.  G ← READ_DOT(G_dot)
2.  stats ← COMPUTE_GRAPH_STATS(G)   // total_nodes, avg_degree, root_node, edge_types, nodes_preview, relations_sample
3.  prompt ← FILL(AGENT2_PROMPT, stats, file_stem = stem(G_dot))
4.  response ← GEMINI_JSON(prompt)    // response_mime_type = application/json
5.  fault_json ← PARSE_JSON(response) // with fallback: brace-balanced extract, regex
6.  WRITE_JSON(fault_json, stem(G_dot) + "_agent2.json")
7.  return fault_json
```

**Integration with Agent 1:** Input is the exact DOT file produced by Agent 1. **Integration with Agent 3:** The output `fault_json` contains `faulty_nodes` (list of node_id, fault_type, relations, fault_score) and `fault_summary`; Agent 3 reads this file by stem (e.g., `bug100.blocks_graph_agent2.json`) and the corresponding DOT from Agent 1’s folder.

### 4.4 Agent 3: Graph Rectification

**Algorithm 4: AGENT3_REPAIR_GRAPH(fault_json, G_dot)**

```
Input:  fault_json (from Agent 2), G_dot (same stem as fault_json)
Output: rect_json (rectified_nodes, full_rectified_graph, rectification_summary), G_repaired_dot (optional)

1.  G ← READ_DOT(G_dot)
2.  faulty_list ← fault_json.faulty_nodes
3.  context ← BUILD_REPAIR_CONTEXT(faulty_list, G)   // faulty node details + full graph as DOT string
4.  prompt ← FILL(AGENT3_PROMPT, context, file_name, total_faults, total_nodes, root_node)
5.  response ← GEMINI_JSON(prompt)
6.  rect_json ← PARSE_JSON(response)
7.  WRITE_JSON(rect_json, stem(G_dot) + ".blocks_graph_agent3_full.json")
8.  if rect_json.full_rectified_graph exists then
9.      G_rep ← PARSE_DOT(rect_json.full_rectified_graph)
10.     WRITE_DOT(G_rep, stem(G_dot) + ".blocks_graph_repaired.dot")
11. return rect_json, path_to_repaired_dot (if any)
```

**Integration with Agent 2:** Consumes `fault_json` and the **same** DOT as Agent 2 (so fault ids refer to nodes in that graph). **Integration with Agent 4:** Agent 4 needs `rect_json.rectified_nodes` and `rect_json.full_rectified_graph`; it loads the JSON by matching source file stem to `{stem}.blocks_graph_agent3_full.json`.

### 4.5 Agent 4: Source Code Reconstruction

**Algorithm 5: AGENT4_RECONSTRUCT_SOURCE(source_file, rect_json)**

```
Input:  source_file (original .py), rect_json (from Agent 3)
Output: repaired_code (full Python source string)

1.  original_code ← READ_FILE(source_file)
2.  rectified_nodes ← rect_json.rectified_nodes
3.  rectified_graph ← rect_json.full_rectified_graph
4.  prompt ← FILL(AGENT4_PROMPT, original_code, rectified_nodes, rectified_graph)
5.  repaired_code ← GEMINI_TEXT(prompt)   // temperature=0, no markdown
6.  WRITE_FILE(OUTPUT_DIR / name(source_file), repaired_code)
7.  return repaired_code
```

**Integration with Agent 3:** Agent 4 runs only when a matching Agent 3 JSON exists for the same file stem. The prompt constrains the LLM to output the **full file** and to change **only** lines corresponding to rectified nodes (surgical edit).

### 4.6 Evaluation Algorithm

**Algorithm 6: EVALUATE(original_path, repaired_path)**

```
Input:  original_path, repaired_path (matching .py files)
Output: metrics = {levenshtein_distance, cosine_similarity, line_edit_distance}

1.  a ← READ_FILE(original_path)
2.  b ← READ_FILE(repaired_path)
3.  metrics.levenshtein_distance ← LEVENSHTEIN(a, b)
4.  metrics.cosine_similarity ← COSINE_3GRAM(a, b)
5.  metrics.line_edit_distance ← LINE_EDIT_DISTANCE(a, b)
6.  return metrics
```

Applied for every pair (input_path/file.py, output_path/file.py); results aggregated per library in `results/<lib>_agent4_similarity_results.json`.

### 4.7 End-to-End Integration Summary

| Step | Agent / Stage | Input(s) | Output(s) | Consumed next by |
|------|----------------|----------|-----------|-------------------|
| 1 | Agent 1 | source_file | G_dot | Agent 2 (and Agent 3 for same G_dot) |
| 2 | Agent 2 | G_dot | fault_json | Agent 3 |
| 3 | Agent 3 | fault_json, G_dot | rect_json, G_repaired_dot | Agent 4 (rect_json only) |
| 4 | Agent 4 | source_file, rect_json | repaired_code | Evaluation |
| 5 | Evaluation | source_file, repaired_code | metrics | — |

**Key integration points:**

- **Naming:** All artifacts for one source file share the same stem; Agent 3 and Agent 4 resolve files by stem (e.g., `bug100` → `bug100.blocks_graph_agent3_full.json`).
- **No cycles:** The pipeline is acyclic; no agent reads output from a later stage.
- **Single representation:** The block graph (DOT) is the only shared structure between Agents 1–3; Agent 4 uses it only as context and uses `rectified_nodes` as the set of allowed edit locations.
- **Structured handoffs:** Every handoff is a file (DOT or JSON) with a fixed schema, so each agent can be run or re-run independently as long as upstream outputs exist.

---

## 5. In-Depth Study of Each Agent

### 5.1 Agent 1: Code-Block Graph Builder

#### 5.1.1 What It Does

Agent 1 converts **Python source code** into a **block-level directed graph** encoded in DOT format. Each node corresponds to a logical code block (function, class, assignment, return, call, if/for/while/with/try). Each edge is one of: `contains`, `data_flow`, `control_flow`, `call`. This graph is the **single shared representation** used by Agents 2, 3, and 4.

#### 5.1.2 Implementation

- **AST path:** A custom `CodeBlockVisitor` (Python `ast.NodeVisitor`) walks the AST and, for each relevant node type, records:
  - Block id (e.g., `b1`, `b2`), type, `start_line`, `end_line`, and an optional code snippet (via `ast.get_source_segment`).
  - **Relationships:** “contains” from the current function/class to the new block; “control_flow” from the previous block to the current; “call” for call nodes within a function.
- **LLM fallback:** If the AST yields **fewer than three nodes** (e.g., malformed or very small code), the script optionally calls **Google Gemini** (`gemini-2.5-flash`) with a fixed prompt (`BLOCK_GRAPH_PROMPT`) that asks for the same JSON schema (nodes + relationships). The response is parsed (with robust brace matching and JSON extraction) and used to build the graph.
- **Graph construction:** A NetworkX `DiGraph` is built from the nodes and relationships; node attributes include `label` (e.g., line range and type) and `type`; edge attribute is `label` (relationship type). The graph is written to disk using `write_dot` from `networkx.drawing.nx_pydot`.

#### 5.1.3 Usage

- **Invocation:** `python agent1.py` (paths are hardcoded in `if __name__ == "__main__"`, e.g., `INPUT_PATH = Path("./input_path/pandas_input_path")`, `OUTPUT_PATH = Path("./agent1_output_graph/pandas_agent1_graph")`).
- **Input:** All `.py` (and optionally `.txt`) files under the input path.
- **Output:** One `.dot` file per input file, e.g. `bug100.blocks_graph.dot`.

#### 5.1.4 Why It Is Useful

- Provides a **uniform, relation-typed** representation that downstream agents can reason about.
- AST-first approach is fast and deterministic for well-formed code; LLM fallback handles edge cases.
- Line numbers and snippets preserve traceability to source for Agent 4.

---

### 5.2 Agent 2: Semantic Fault Detector

#### 5.2.1 What It Does

Agent 2 performs **fault localization** on the block graph. It does *not* look at source code directly; it analyzes the **graph structure and edge types** to identify nodes that violate semantic patterns (e.g., broken dependency, flow mismatch, orphaned computation). It outputs a list of faulty nodes with fault types and a fault summary.

#### 5.2.2 Semantic Patterns Detected

The Agent 2 prompt defines seven relation-driven patterns:

1. **Broken dependency** — An assignment has no `data_flow` to a return/call that should use it.
2. **Flow mismatch** — `control_flow` is used where `data_flow` is expected (e.g., between data-dependent assignments).
3. **Incomplete convergence** — Multiple assignments feed into a single return but some paths are missing.
4. **Orphaned computation** — An assignment has no downstream `data_flow` to any use.
5. **Circular dependency** — A cycle in `data_flow` (e.g., assignment → assignment → assignment).
6. **Disconnected return** — A return has no incoming `data_flow` from the function scope.
7. **Unreachable call** — A call has no path from the function that contains it (e.g., missing `contains` or control path).

The prompt explicitly instructs the model to avoid self-loop or graph-density bias and to base faults on **relations → semantics → fault** in three steps. It requests a semantic correctness score (0–10) per node and allows an empty `faulty_nodes` list when no defects are found.

#### 5.2.3 Implementation

- **Input:** DOT file path. The graph is loaded with `read_dot` into a NetworkX `DiGraph`.
- **Prompt preparation:** The `FaultyNodeDetector` computes:
  - Total nodes, average degree, root node (max “contains” out-degree), edge-type counts.
  - A short preview of nodes and a sample of edges (e.g., first 6 nodes, first 8 edges) for the prompt.
- **LLM call:** The prompt (`AGENT2_PROMPT`) is filled with these variables and sent to Gemini with `response_mime_type="application/json"`. The model returns a JSON object with `file_name`, `total_nodes`, `avg_degree`, `faulty_nodes` (each with `node_id`, `type`, `relations_in`, `relations_out`, `fault_score`, `fault_type`), and `fault_summary` (e.g., `total_faults`, `common_patterns`, `clean_nodes`).
- **Robustness:** The code includes fallback JSON extraction (direct parse, balanced-brace search, regex) to handle markdown or extra text around the JSON.

#### 5.2.4 Usage

- **Invocation:** `python agent2.py` with input folder set to the Agent 1 output (e.g., `./agent1_graph/pandas_agent1_graph`) and output folder to `./agent2_results/pandas_agent2_results`.
- **Output:** One JSON file per DOT file, e.g. `bug100.blocks_graph_agent2.json`.

#### 5.2.5 Why It Is Useful

- **Semantic fault localization** without executing code: purely structural/relational analysis.
- **Interpretable output:** Each fault is tied to a node and a named pattern, which supports debugging and research.
- **Structured input for Agent 3:** The fault list and types drive the repair rules.

---

### 5.3 Agent 3: Graph Rectification (Repair) Agent

#### 5.3.1 What It Does

Agent 3 **repairs the graph** so that the structural/semantic faults identified by Agent 2 are fixed. It does *not* generate source code; it produces a **rectified graph** (and a list of rectified nodes with fix descriptions) that Agent 4 will use to guide source changes.

#### 5.3.2 Repair Rules (Aligned with Agent 2 Fault Types)

- **BROKEN_DEPENDENCY** → Add `data_flow` from producer to consumer.
- **FLOW_MISMATCH** → Replace `control_flow` with `data_flow` where appropriate.
- **INCOMPLETE_CONVERGENCE** → Add missing `data_flow` into the return.
- **ORPHANED_COMPUTATION** → Connect to the nearest downstream use.
- **CIRCULAR_DEPENDENCY** → Break the cycle (e.g., via one intermediate node).
- **DISCONNECTED_RETURN** → Connect the nearest assignment.
- **UNREACHABLE_CALL** → Add `contains` (or appropriate edge) from the function.

The prompt stresses **minimality**: only add or relabel edges, or add a small temp node if needed to break cycles. No renaming or deleting nodes, no restructuring of the program, no inventing new logic.

#### 5.3.3 Implementation

- **Input:** Agent 2 JSON (faulty nodes, fault summary) and the original DOT graph.
- **Context building:** The agent prepares a string of faulty node details (node_id, fault_type, relations) and the full graph in DOT form. Token limit is considered (e.g., up to ~12k tokens in the prompt).
- **LLM call:** `AGENT3_PROMPT` is sent to Gemini. The model must return JSON containing:
  - `rectified_nodes`: list of {node_id, fault_type, fix_description, confidence}.
  - `full_rectified_graph`: the **entire** corrected graph as a single DOT string.
  - `rectification_summary`: e.g., total_fixes, edge_additions, edge_modifications, nodes_added.
- **Output handling:** The full repair JSON is written (e.g., `*_agent3_full.json`). When `full_rectified_graph` is present, it is parsed and written as a separate `.blocks_graph_repaired.dot` file.

#### 5.3.4 Usage

- **Invocation:** `python agent3.py` with paths to Agent 2 results and Agent 1 graph folder; output to `agent3_rectified_graph/...`.
- **Output:** One full repair JSON and, when available, one repaired DOT file per input.

#### 5.3.5 Why It Is Useful

- **Repair in graph space** keeps the LLM focused on structure, reducing the risk of arbitrary code rewrites.
- **Minimal-edit discipline** encourages small, interpretable fixes.
- **Full rectified graph** gives Agent 4 a complete view of the intended structure for code generation.

---

### 5.4 Agent 4: Source Code Reconstruction

#### 5.4.1 What It Does

Agent 4 **back-translates** the repaired graph and the list of rectified nodes into **fixed Python source code**. It receives the original source and the Agent 3 output; it must output the **complete** file, changing **only** the lines that correspond to rectified nodes, and preserve all other lines exactly (no reformatting, no extra comments).

#### 5.4.2 Implementation

- **Matching:** For each `.py` file in the input code directory, the script looks for the corresponding Agent 3 JSON (e.g., `{file_stem}.blocks_graph_agent3_full.json`). If missing, the file is skipped.
- **Prompt:** `AGENT4_PROMPT` includes:
  - The original Python code (authoritative).
  - The rectified nodes (only these may change).
  - The rectified graph (for context only).
- **Constraints:** Output must be valid Python only; no markdown, no explanations, no diffs. The prompt frames the task as a “surgical edit.”
- **LLM:** Gemini (`gemini-2.5-flash`) with temperature 0 and sufficient max_output_tokens (e.g., 6000). Response text is stripped and written to the output directory under the same filename.

#### 5.4.3 Usage

- **Invocation:** `python agent4.py` with `INPUT_CODE_DIR` (original code), `AGENT3_DIR` (Agent 3 JSON), and `OUTPUT_DIR` (repaired code).
- **Output:** One repaired `.py` file per successfully matched input.

#### 5.4.4 Why It Is Useful

- **Controlled code generation:** The LLM is constrained by the graph and the rectified-node list, which should limit over-editing.
- **Traceability:** Changes are tied to graph nodes, supporting accountability and debugging.

---

### 5.5 Evaluation: calculate.py

#### 5.5.1 What It Does

The evaluation script compares **original** (input path) and **repaired** (Agent 4 output) Python files and computes three metrics per file:

1. **Levenshtein distance** — Character-level edit distance (number of insertions, deletions, substitutions).
2. **Cosine similarity** — Based on character 3-grams; value in [0, 1], higher means more similar.
3. **Line-edit distance** — Number of lines that differ (by position) plus the difference in line count.

Results are written to a single JSON file per library (e.g., `results/pandas_agent4_similarity_results.json`).

#### 5.5.2 Implementation

- Levenshtein: classic dynamic programming.
- Cosine: build character 3-gram counts, compute cosine of the two vectors.
- Line-edit: pairwise line comparison and length difference.
- All pairs (input_file, output_file) with matching names are processed; missing outputs are reported and skipped.

#### 5.5.3 Interpretation

- **High cosine similarity** and **low Levenshtein/line-edit distance** suggest **minimal, targeted** repairs—desirable for APR.
- The metrics do not measure correctness (tests are not run); they measure how much the repaired code *differs* from the original, which can support studies on repair minimality and overfitting.

---

## 6. Implementation Details (Technology and Data Flow)

### 6.1 Technology Stack

- **Language:** Python 3.
- **Libraries:** `pathlib`, `os`, `json`, `ast`, `re`, `typing`, `collections` (e.g., `Counter`, `deque`); **NetworkX** for graphs; **networkx.drawing.nx_pydot** for `read_dot`/`write_dot`/`to_pydot`; **google.generativeai** (Gemini API); **python-dotenv** for loading `.env`.
- **Model:** `gemini-2.5-flash`; API key from environment (`GEMINI_API_KEY`) after loading `.env` from the project root.
- **Configuration:** No `requirements.txt` or README in the repository; paths are hardcoded in each script’s main block. Different libraries (pandas, fastapi, mlib, keras, spacy) are supported by changing these paths and the corresponding folder names.

### 6.2 Artifact Flow Summary

| From        | To        | Artifact |
|------------|-----------|----------|
| Source     | Agent 1   | Python (.py) |
| Agent 1    | Agent 2   | DOT (.blocks_graph.dot) |
| Agent 2    | Agent 3   | JSON (faulty_nodes, fault_summary) |
| Agent 3    | Agent 4   | JSON (rectified_nodes, full_rectified_graph) + optional repaired DOT |
| Agent 4    | Evaluation| Repaired .py |
| Evaluation | —         | results/*_similarity_results.json |

### 6.3 Graph Schema (Recap)

- **Nodes:** id (e.g., b1), type (function, class, assignment, return, call, if, for, while, with, try), start_line, end_line, optional code snippet.
- **Edges:** label in {contains, data_flow, control_flow, call}. Used for hierarchy, dependencies, control flow, and calls so that Agents 2 and 3 can reason about semantic faults and minimal graph edits.

---

## 7. Real-Life Scenarios and Usefulness

### 7.1 Benchmark and Target Domains

The project is evaluated on **buggy, non-modular Python snippets** drawn from real libraries:

- **pandas** — Data manipulation (e.g., bug100, bug102, …).
- **FastAPI** — Web APIs.
- **matplotlib (mlib)** — Plotting.
- **Keras** — Deep learning.
- **spaCy** — NLP.

This indicates use in **automated program repair** and **defect localization** experiments on real-world, library-dependent code.

### 7.2 Concrete Use Cases

1. **Automated repair of structural/semantic defects**  
   Fixing wrong or missing data/control flow, unreachable or orphaned code, and circular dependencies by: (1) representing code as a block graph, (2) detecting faulty nodes, (3) repairing the graph, (4) regenerating source. Useful in continuous integration (e.g., “suggest a minimal fix for this graph-identified fault”) or in-house tools for code quality.

2. **Fault localization and triage**  
   Agent 2’s output (faulty nodes + fault types) can support developers in **where** to look and **what kind** of fault (e.g., “incomplete_convergence” at node b7). This can be integrated into IDEs or code-review pipelines.

3. **Research and benchmarking**  
   The pipeline provides a **reproducible** setup: same agents, same prompts, same metrics. Researchers can compare graph-based repair with other APR approaches or ablate agents (e.g., different fault patterns, different LLMs).

4. **Refactoring and dependency cleanup**  
   The same relation-driven view (data_flow, control_flow, contains, call) can inform refactoring tools that aim to fix structural issues (e.g., breaking cycles, connecting orphaned computations) before or alongside semantic fixes.

### 7.3 Limitations in Practice

- **No test execution:** Repair quality is measured by textual similarity and edit distance, not by passing tests. Integration with a test suite would strengthen claims about correctness.
- **Manual pipeline:** Running and path configuration are manual; automation (e.g., a single entry point and config file) would improve usability.
- **Library-specific paths:** Switching libraries requires editing path constants in multiple scripts.

---

## 8. What Makes This Project Special

### 8.1 Relation-Driven Semantic Model

Faults are defined in terms of **graph relations** (contains, data_flow, control_flow, call), not raw code or heuristics on text. This yields:

- A **clear, declarative** set of fault patterns (e.g., “assignment has no data_flow to return”).
- **Consistency** between detection (Agent 2) and repair (Agent 3) via the same vocabulary.
- **Interpretability:** Analysts can inspect the graph and the fault list to understand why a node was flagged.

### 8.2 Graph-First Repair

Repair is performed **in graph space** (Agent 3) before any code generation (Agent 4). Benefits:

- **Minimality:** The prompt enforces “smallest possible correction” (add/relabel edges, optional temp node).
- **Reduced LLM drift:** The model edits a structured object (graph) with fixed schema, then Agent 4 maps that to code with strict constraints (surgical edit only on rectified nodes).
- **Reusability:** The same rectified graph could, in principle, be mapped to other representations or languages if Agent 4 were extended.

### 8.3 Multi-Agent Decomposition

- **Single responsibility:** Each agent has one job (build, detect, repair, reconstruct), which simplifies reasoning and testing.
- **Structured handoffs:** Each stage consumes and produces well-defined artifacts (DOT, JSON), so the pipeline is **auditable** and **extensible** (e.g., swap a different detector or a different LLM for one agent).
- **Hybrid logic:** Agent 1 uses **deterministic AST** first and **LLM only as fallback**; Agents 2–4 use the LLM with **strong prompting** (JSON format, relation-driven rules), combining symbolic structure with neural generation.

### 8.4 Real-World Evaluation Across Libraries

The system is not only demonstrated on one benchmark but run across **five** real-world libraries (pandas, FastAPI, matplotlib, Keras, spaCy), with similarity results collected for each. This shows **breadth** of application and supports generalizability claims for the approach.

### 8.5 Evaluation Metrics for Minimality

Levenshtein distance, cosine similarity, and line-edit distance directly measure **how much** the repaired code differs from the original. High similarity and low edit distance align with the goal of **minimal patches**, which is a recognized objective in APR to avoid overfitting and preserve behavior.

---

## 9. Evaluation Results (Illustrative)

Using the existing results for the pandas benchmark (16 files), the evaluation script produces per-file metrics. Examples from `results/pandas_agent4_similarity_results.json`:

- **bug105.py:** Levenshtein 1, cosine 1.0, line-edit 0 — repair is nearly identical to original (minimal or no change).
- **bug100.py:** Levenshtein 33, cosine 0.993, line-edit 12 — moderate edits, high similarity.
- **bug120.py:** Levenshtein 52, cosine 0.9932, line-edit 2 — fewer line changes but more character-level edits (e.g., longer lines modified).

These results illustrate that the pipeline produces repairs that **vary in magnitude** (from almost no change to larger edits) while often keeping **high cosine similarity**, consistent with targeted, structure-guided fixes.

---

## 10. Conclusion

This paper presented an in-depth study of a **multi-agent program repair system** built around a **block-level code graph**. We described what each of the four agents does, how they are implemented (AST + optional LLM for graph building; LLM with relation-driven prompts for fault detection, graph repair, and code reconstruction), and how the pipeline is used and evaluated. We discussed **real-life scenarios** (APR, fault localization, research, refactoring) and **what makes the project special**: the relation-driven semantic model, graph-first repair, multi-agent decomposition, hybrid symbolic/neural design, and evaluation across multiple real-world libraries with minimality-oriented metrics.

Future work could include: (1) integrating test execution to measure correctness, (2) a single orchestration script and config-driven paths, (3) extending the fault catalog and repair rules, and (4) comparing with other APR and multi-agent repair systems on standardized benchmarks.

---

## References (Suggested)

- Automated Program Repair (APR) surveys and benchmarks.
- Code representation (AST, CFG, PDG, dependency graphs).
- Multi-agent systems for software engineering.
- LLM-based code generation and repair (e.g., Gemini, Codex, etc.).
- Minimal patch generation and overfitting in APR.

---

## Appendix: Quick Reference Table

| Agent   | Script      | Input                          | Output                                      | Invocation        |
|---------|-------------|--------------------------------|---------------------------------------------|-------------------|
| 1       | agent1.py   | input_path/.../*.py            | *.blocks_graph.dot                           | python agent1.py  |
| 2       | agent2.py   | agent1_graph/.../*.dot         | *_agent2.json                                | python agent2.py  |
| 3       | agent3.py   | Agent 2 JSON + same DOT        | *_agent3_full.json, *.blocks_graph_repaired.dot | python agent3.py  |
| 4       | agent4.py   | Original .py + Agent 3 JSON    | Repaired .py                                 | python agent4.py  |
| —       | calculate.py| Original + Agent 4 .py         | results/*_similarity_results.json           | python calculate.py |
