# Architecture Draft: Multi-Agent Program Repair System

This document describes **how the system architecture should be designed** so that a single, coherent implementation (or code generator) can be built from it. It defines layers, components, interfaces, data contracts, and orchestration.

---

## 1. High-Level Architecture

### 1.1 Layered View

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ORCHESTRATION LAYER                                    │
│  (Pipeline runner: config, run all / run stage, file-stem alignment)         │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AGENT LAYER                                            │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐                  │
│  │ Agent 1  │ → │ Agent 2  │ → │ Agent 3  │ → │ Agent 4  │   (sequential)     │
│  │ Graph    │   │ Fault    │   │ Rectify  │   │ Reconstruct│                  │
│  │ Builder  │   │ Detector │   │ Graph    │   │ Source    │                  │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SHARED SERVICES LAYER                                  │
│  • Graph I/O (read_dot, write_dot, DiGraph)                                  │
│  • LLM client (Gemini: prompt, JSON/text, config)                             │
│  • Config loader (paths, API key, model name)                                │
└─────────────────────────────────────────────────────────────────────────────┘
                                      │
                                      ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ARTIFACT STORAGE (FILE SYSTEM)                        │
│  input_path / agent1_graph / agent2_results / agent3_rectified /            │
│  agent4_output_code / results                                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 Component Diagram

```
                    ┌─────────────────┐
                    │   Config        │
                    │   (YAML/ENV)    │
                    └────────┬────────┘
                             │
     ┌───────────────────────┼───────────────────────┐
     │                       │                       │
     ▼                       ▼                       ▼
┌─────────┐            ┌──────────┐            ┌─────────────┐
│ Runner  │───────────▶│ Agent 1  │───────────▶│ Agent 2     │
│ (main)  │            │ (graph)  │            │ (faults)    │
└─────────┘            └──────────┘            └──────┬──────┘
     │                        │                      │
     │                        │                      ▼
     │                        │               ┌─────────────┐
     │                        │               │ Agent 3     │
     │                        │               │ (rectify)   │
     │                        │               └──────┬──────┘
     │                        │                      │
     │                        │                      ▼
     │                        │               ┌─────────────┐
     │                        └──────────────│ Agent 4     │
     │                         (original .py) │ (reconstruct)│
     │                                        └──────┬──────┘
     │                                               │
     ▼                                               ▼
┌─────────────┐                               ┌─────────────┐
│ Evaluation  │◀─────────────────────────────│ Repaired    │
│ (metrics)   │   (original + repaired .py)   │ .py         │
└─────────────┘                               └─────────────┘
```

---

## 2. Component Specifications

### 2.1 Orchestration Layer

**Responsibility:** Drive the pipeline for one or many files; resolve paths from config; enforce file-stem alignment.

**Interface (conceptual):**

- `run_pipeline(config: PipelineConfig, file_or_dir: Path) -> PipelineResult`
  - If `file_or_dir` is a file: run Agents 1→2→3→4→Evaluation for that file.
  - If directory: for each `.py` in dir, run pipeline; aggregate results.
- `run_stage(config: PipelineConfig, stage: AgentId, file_stem: str) -> StageOutput`
  - Run only one stage (1, 2, 3, or 4) for the given stem; read inputs from config paths, write outputs to config paths.

**Config shape (to be loaded once):**

- `input_code_dir: Path`
- `agent1_graph_dir: Path`
- `agent2_results_dir: Path`
- `agent3_rectified_dir: Path`
- `agent4_output_dir: Path`
- `results_dir: Path`
- `llm_api_key: str`, `llm_model: str` (optional overrides)

**Naming rule:** For source file `{stem}.py`, all artifacts use the same stem:  
`{stem}.blocks_graph.dot`, `{stem}.blocks_graph_agent2.json`, `{stem}.blocks_graph_agent3_full.json`, repaired file `{stem}.py` in `agent4_output_dir`.

---

### 2.2 Agent 1: Graph Builder

**Input:** Raw Python source (string or path).  
**Output:** Block graph in memory (e.g. `nx.DiGraph`) and/or path to `.dot` file.

**Contract:**

- **Nodes:** id (e.g. `b1`), type ∈ {function, class, assignment, return, call, if, for, while, with, try}, start_line, end_line, optional code snippet.
- **Edges:** from, to, label ∈ {contains, data_flow, control_flow, call}.

**Internal steps:**

1. Parse source → AST.
2. Run block visitor → nodes + relationships (same schema as above).
3. If `len(nodes) < 3`: optional LLM fallback → same schema.
4. Build `DiGraph` from nodes/relationships; write DOT to `agent1_graph_dir / f"{stem}.blocks_graph.dot"`.

**Dependencies:** AST parser, optional LLM client (shared service), graph I/O (shared service).

---

### 2.3 Agent 2: Fault Detector

**Input:** Path to `.dot` (from Agent 1) or in-memory graph.  
**Output:** Fault result: `{ file_name, total_nodes, avg_degree, faulty_nodes: [...], fault_summary }`.

**Contract (faulty_nodes item):** node_id, type, relations_in, relations_out, fault_score (0–10), fault_type (e.g. broken_dependency, flow_mismatch, incomplete_convergence, orphaned_computation, circular_dependency, disconnected_return, unreachable_call).

**Internal steps:**

1. Load graph from DOT.
2. Compute stats (node count, degree, root, edge types, small preview).
3. Fill AGENT2_PROMPT; call LLM (JSON mode).
4. Parse JSON (with fallback); write to `agent2_results_dir / f"{stem}.blocks_graph_agent2.json"`.

**Dependencies:** Graph I/O, LLM client (shared service).

---

### 2.4 Agent 3: Graph Rectifier

**Input:** Path to Agent 2 JSON (or in-memory fault result) + path to same stem’s DOT (or in-memory graph).  
**Output:** Rectification result: `{ file_name, rectified_nodes: [...], full_rectified_graph (DOT string), rectification_summary }`.

**Contract (rectified_nodes item):** node_id, fault_type, fix_description, confidence.

**Internal steps:**

1. Load fault_json and graph (DOT).
2. Build repair context (faulty list + full graph as string).
3. Fill AGENT3_PROMPT; call LLM (JSON mode).
4. Parse JSON; write to `agent3_rectified_dir / f"{stem}.blocks_graph_agent3_full.json"`.
5. If `full_rectified_graph` present, write to `agent3_rectified_dir / f"{stem}.blocks_graph_repaired.dot"`.

**Dependencies:** Graph I/O, LLM client (shared service).

---

### 2.5 Agent 4: Source Reconstructor

**Input:** Original source (string or path) + Agent 3 result (rectified_nodes + full_rectified_graph).  
**Output:** Repaired Python source (string); also write to `agent4_output_dir / f"{stem}.py"`.

**Contract:** Output is exactly one full Python file; only lines corresponding to rectified_nodes may differ from original (surgical edit).

**Internal steps:**

1. Load original code and Agent 3 JSON.
2. Fill AGENT4_PROMPT (original code, rectified_nodes, full_rectified_graph).
3. Call LLM (text mode, temperature 0); strip response.
4. Write to output path.

**Dependencies:** LLM client (shared service).

---

### 2.6 Evaluation

**Input:** Path to original `.py` and path to repaired `.py` (same stem).  
**Output:** `{ levenshtein_distance, cosine_similarity, line_edit_distance }`.

**Internal steps:** Read both files; compute the three metrics; optionally append to a per-library results file (e.g. `results_dir / "{lib}_agent4_similarity_results.json"`).

**Dependencies:** None (pure functions on strings).

---

## 3. Shared Services

### 3.1 Graph I/O

- `load_graph(path: Path) -> nx.DiGraph`  (read_dot).
- `save_graph(G: nx.DiGraph, path: Path) -> None`  (write_dot).
- Node/edge schema: node attributes `label`, `type`; edge attribute `label` (contains | data_flow | control_flow | call).

### 3.2 LLM Client

- `generate_json(prompt: str, model: str, api_key: str, **kwargs) -> dict`  (Gemini JSON; robust parse).
- `generate_text(prompt: str, model: str, api_key: str, **kwargs) -> str`  (Gemini text).
- Config: api_key, model name (e.g. gemini-2.5-flash), temperature, max_tokens; loaded from config/env.

### 3.3 Config Loader

- Load from: (1) config file (e.g. `config.yaml` or `config.json`) and (2) environment (e.g. `GEMINI_API_KEY`, overrides).
- Expose: all paths (input, agent1–4, results), LLM settings. Single `PipelineConfig` (or similar) object consumed by Runner and agents.

---

## 4. Directory and File Layout (Target)

```
project_root/
├── config.yaml                 # paths, lib name, LLM settings (single source of truth)
├── .env                        # GEMINI_API_KEY (git-ignored)
├── src/
│   ├── __init__.py
│   ├── config.py               # load config + env → PipelineConfig
│   ├── runner.py               # run_pipeline, run_stage
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── agent1_graph.py     # build block graph (AST + optional LLM)
│   │   ├── agent2_faults.py    # detect faulty nodes (LLM)
│   │   ├── agent3_rectify.py   # rectify graph (LLM)
│   │   └── agent4_reconstruct.py  # reconstruct source (LLM)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── graph_io.py         # load_graph, save_graph
│   │   └── llm_client.py      # generate_json, generate_text
│   └── evaluation.py           # levenshtein, cosine_similarity, line_edit; aggregate
├── input_path/
│   └── {lib}_input_path/       # e.g. pandas_input_path/
│       └── *.py
├── agent1_graph/
│   └── {lib}_agent1_graph/
│       └── *.blocks_graph.dot
├── agent2_results/
│   └── {lib}_agent2_results/
│       └── *.blocks_graph_agent2.json
├── agent3_rectified_graph/
│   └── {lib}_agent3_rectified_graph/
│       ├── *.blocks_graph_agent3_full.json
│       └── *.blocks_graph_repaired.dot
├── agent4_output_code/
│   └── {lib}_agent4_output_code/
│       └── *.py
├── results/
│   └── {lib}_agent4_similarity_results.json
├── main.py                     # CLI: run all / run stage / run eval; uses config
└── prompts/                    # optional: AGENT2, AGENT3, AGENT4 prompts as files
    ├── agent2.txt
    ├── agent3.txt
    └── agent4.txt
```

---

## 5. Data Contracts (Schemas)

### 5.1 Block Graph (internal / DOT)

- **Nodes:** id (str), type (str), start_line (int), end_line (int), optional code (str).
- **Edges:** from (node id), to (node id), label ∈ {contains, data_flow, control_flow, call}.

### 5.2 Agent 2 Output (JSON)

```json
{
  "file_name": "string",
  "total_nodes": "number",
  "avg_degree": "number",
  "faulty_nodes": [
    {
      "node_id": "string",
      "type": "string",
      "relations_in": ["string"],
      "relations_out": ["string"],
      "fault_score": "number",
      "fault_type": "string"
    }
  ],
  "fault_summary": {
    "total_faults": "number",
    "common_patterns": ["string"],
    "clean_nodes": "number"
  }
}
```

### 5.3 Agent 3 Output (JSON)

```json
{
  "file_name": "string",
  "rectified_nodes": [
    {
      "node_id": "string",
      "fault_type": "string",
      "fix_description": "string",
      "confidence": "number"
    }
  ],
  "full_rectified_graph": "string (DOT)",
  "rectification_summary": {
    "total_fixes": "number",
    "edge_additions": "number",
    "edge_modifications": "number",
    "nodes_added": "number"
  }
}
```

### 5.4 Evaluation Output (JSON)

```json
{
  "filename.py": {
    "levenshtein_distance": "number",
    "cosine_similarity": "number",
    "line_edit_distance": "number"
  }
}
```

---

## 6. CLI / Entry Point (Target Behavior)

One entry point that can drive the whole system from the architecture above:

```bash
# Run full pipeline for one library (all .py in input path)
python main.py --config config.yaml --lib pandas run

# Run only one stage for all files
python main.py --config config.yaml --lib pandas run --stage 2

# Run pipeline for a single file
python main.py --config config.yaml --lib pandas run --file bug100.py

# Run only evaluation (compare input vs agent4 output)
python main.py --config config.yaml --lib pandas eval
```

Config and `--lib` define all paths; no hardcoded paths in agent code.

---

## 7. Summary: What This Architecture Enables

- **Single pipeline runner** that executes the combined algorithm (Agent 1→2→3→4→Eval) per file, with one config.
- **Clear boundaries:** each agent has defined input/output contracts and uses shared services (graph I/O, LLM, config).
- **File-stem alignment** and directory layout specified in one place (config + runner).
- **Testability:** agents can be unit-tested with in-memory inputs/outputs; shared services can be mocked.
- **Generation-friendly:** a code generator can produce `config.py`, `runner.py`, `agents/*.py`, `services/*.py`, `evaluation.py`, and `main.py` from this draft plus the existing prompts and algorithms.

Use this draft as the **architecture spec** when implementing or generating the system.
