"""
In-memory / temp-dir pipeline for Streamlit UI.
Uses agent1–agent4 logic without modifying original batch scripts.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

import networkx as nx
from networkx.drawing.nx_pydot import write_dot

# Project root (directory containing agent modules)
ROOT = Path(__file__).resolve().parent


def ensure_work_dir(session_key: str) -> Path:
    d = ROOT / ".streamlit_workspace" / session_key
    d.mkdir(parents=True, exist_ok=True)
    return d


def run_agent1(code: str, work_dir: Path, stem: str = "session") -> Tuple[str, Dict[str, Any], nx.DiGraph]:
    from agent1 import analyze_code, build_graph_from_result

    result = analyze_code(code.strip() or "")
    G = build_graph_from_result(result)
    dot_name = f"{stem}.blocks_graph.dot"
    dot_path = work_dir / dot_name
    write_dot(G, dot_path.open("w"))
    dot_text = dot_path.read_text(encoding="utf-8", errors="replace")
    meta = {
        "nodes": len(G.nodes),
        "edges": len(G.edges),
        "nodes_detail": result.get("nodes", []),
        "relationships": result.get("relationships", []),
    }
    return dot_text, meta, G


def run_agent2(dot_path: Path, work_dir: Path) -> Dict[str, Any]:
    from agent2 import FaultyNodeDetector

    detector = FaultyNodeDetector()
    out = detector.analyze_graph(dot_path)
    stem = dot_path.stem  # e.g. session.blocks_graph
    out.setdefault("file_name", stem)
    out["file_name"] = stem
    json_path = work_dir / f"{stem}_agent2.json"
    json_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out


def run_agent3(agent2_json: Dict[str, Any], dot_path: Path, work_dir: Path) -> Dict[str, Any]:
    from agent3 import FullGraphRepairAgent

    stem = dot_path.stem
    json_path = work_dir / f"{stem}_agent2.json"
    json_path.write_text(json.dumps(agent2_json, indent=2), encoding="utf-8")
    agent = FullGraphRepairAgent()
    result = agent.repair_complete_graph(json_path, dot_path)
    out_path = work_dir / f"{stem}_agent3_full.json"
    out_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


def run_agent4(code: str, agent3_result: Dict[str, Any]) -> str:
    from agent4 import generate_fixed_code

    return generate_fixed_code(code, agent3_result)
