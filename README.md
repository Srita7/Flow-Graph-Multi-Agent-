# Flow-Graph-Driven Multi-Agent Framework for Automated Bug Detection and Repair

## Overview

This project presents a **Flow-Graph-Driven Multi-Agent Framework** for automated bug detection, fault localization, graph repair, and source code reconstruction.

The framework transforms buggy programs into graph representations, identifies semantic and structural faults, applies minimal graph-level repairs, and reconstructs corrected source code.

The system leverages **Large Language Models (LLMs)** together with graph-based reasoning to improve repair accuracy while preserving program semantics.

---

## Key Features

- Multi-agent architecture for automated program repair
- Flow-graph generation from source code using AST analysis
- Semantic fault localization based on graph relationships
- Graph rectification with minimal structural modifications
- Source code reconstruction from repaired graphs
- Support for Python and C programs
- Chain-of-Thought (CoT) and Tree-of-Thought (ToT) repair strategies
- Streamlit-based visualization interface

### Evaluation Metrics

- Levenshtein Distance (LD)
- Cosine Similarity (CS)
- Line Edit Distance

---

## Architecture

The framework consists of four specialized agents:

### Agent 1 – Graph Builder

Converts source code into a block-level directed graph.

#### Node Types

- Function
- Class
- Assignment
- Return
- Call
- If
- For
- While
- Try
- With

#### Edge Types

- Contains
- Data Flow
- Control Flow
- Call Dependency

---

### Agent 2 – Fault Localizer

Detects semantic and structural faults such as:

- Broken Dependency
- Flow Mismatch
- Incomplete Convergence
- Orphaned Computation
- Circular Dependency
- Disconnected Return
- Unreachable Call

---

### Agent 3 – Graph Repair Agent

Performs minimal graph modifications to repair faulty structures while preserving valid program logic.

---

### Agent 4 – Code Reconstruction Agent

Generates repaired source code from the corrected graph representation.

---

## Project Structure

```text
capstone/
│
├── agent1.py                  # Graph Builder
├── agent2.py                  # Fault Localizer
├── agent3.py                  # Graph Repair Agent
├── agent4.py                  # Code Reconstruction
│
├── streamlit_app.py           # Web Interface
├── pipeline_ui.py             # Pipeline Visualization
├── graph_image.py             # Graph Rendering
│
├── input_path/                # Buggy Source Programs
├── agent2_results/            # Fault Detection Results
├── results/                   # Evaluation Outputs
│
├── COT_TOT_PYTHON/            # CoT and ToT Experiments (Python)
├── COT_TOT_C/                 # CoT and ToT Experiments (C)
│
├── build_tables.py            # Evaluation Table Generator
├── calculate.py               # Metrics Computation
│
├── RESEARCH_PAPER.md
└── ARCHITECTURE_DRAFT.md
```

---

## Technology Stack

### Programming Languages

- Python 3.12
- C

### Libraries

- NetworkX
- Pydot
- Matplotlib
- Streamlit
- Python Dotenv
- Google Generative AI SDK

### Large Language Model

- Gemini 2.5 Flash

---

## Installation

### Clone Repository

```bash
git clone https://github.com/your-username/flow-graph-bug-repair.git

cd flow-graph-bug-repair
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=YOUR_API_KEY
```

---

## Running the Framework

### Run Individual Agents

```bash
python agent1.py
python agent2.py
python agent3.py
python agent4.py
```

### Launch Streamlit Dashboard

```bash
streamlit run streamlit_app.py
```

---

## Experimental Evaluation

The framework was evaluated on buggy programs derived from real-world software repositories including:

- Pandas
- FastAPI
- Matplotlib
- Keras
- SpaCy
- Tornado
- Scrapy
- Luigi
- Black
- Ansible

---

## Evaluation Metrics

### Levenshtein Distance (LD)

Measures textual similarity between repaired and reference code.

### Cosine Similarity (CS)

Measures semantic similarity between repaired and target programs.

### Line Edit Distance

Measures the number of line-level modifications required.

---

## Research Contributions

- Flow-graph-based program representation
- Multi-agent fault localization and repair
- Semantic graph repair before code generation
- Integration of CoT and ToT reasoning strategies
- Support for automated bug fixing across Python and C programs
- Improved repair consistency through graph-guided reconstruction

---

## Future Enhancements

- Multi-file project support
- Automated test-case generation
- Reinforcement learning-based repair ranking
- Graph Neural Network (GNN) integration
- IDE extensions for real-time bug repair

---

## Authors

**Srita Padmanabhuni**

