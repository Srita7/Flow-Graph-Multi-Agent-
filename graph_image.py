"""
Render block-graph DOT strings as PNG images.
Uses pydot + Graphviz when available; otherwise matplotlib + NetworkX.
Optional: highlight faulty node ids from Agent 2 JSON.
"""
from __future__ import annotations

import io
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional, Set, Tuple

import networkx as nx


def _normalize_node_id(n: Any) -> str:
    s = str(n).strip().strip('"').strip("'")
    return s


def graph_from_dot_string(dot_str: str) -> Optional[nx.DiGraph]:
    if not dot_str or not dot_str.strip():
        return None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".dot", delete=False, encoding="utf-8"
        ) as f:
            f.write(dot_str)
            path = f.name
        try:
            G = nx.DiGraph(nx.nx_pydot.read_dot(path))
        finally:
            Path(path).unlink(missing_ok=True)
        return G
    except Exception:
        return None


def dot_string_to_png_pydot(dot_str: str) -> Optional[bytes]:
    """Fast, high-quality PNG if Graphviz is installed."""
    try:
        import pydot

        graphs = pydot.graph_from_dot_data(dot_str)
        if graphs:
            return graphs[0].create_png()
    except Exception:
        pass
    return None


def fault_node_ids(agent2_result: Dict[str, Any]) -> Set[str]:
    out: Set[str] = set()
    for n in agent2_result.get("faulty_nodes") or []:
        nid = n.get("node_id")
        if nid:
            out.add(_normalize_node_id(nid))
    return out


def graph_to_png_matplotlib(
    G: nx.DiGraph,
    *,
    highlight: Optional[Set[str]] = None,
    title: str = "",
    figsize: tuple = (10, 7),
    dpi: int = 120,
) -> Optional[bytes]:
    """Draw directed graph with optional fault highlights (no Graphviz required)."""
    if G is None or len(G.nodes) == 0:
        return None

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    highlight = highlight or set()
    # Map graph node -> normalized id for matching
    norm = {_normalize_node_id(n): n for n in G.nodes()}
    fault_graph_nodes = {norm[f] for f in highlight if f in norm}

    pos = nx.spring_layout(G, seed=42, k=2 / max(1, len(G.nodes()) ** 0.5))

    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    ax.set_facecolor("#0f172a")
    fig.patch.set_facecolor("#0f172a")

    node_colors = []
    for n in G.nodes():
        nn = _normalize_node_id(n)
        if n in fault_graph_nodes or nn in highlight:
            node_colors.append("#f87171")  # red-400 fault
        else:
            node_colors.append("#52d1c1")  # teal ok

    labels = {}
    for n, data in G.nodes(data=True):
        lab = data.get("label", n)
        if isinstance(lab, str) and len(lab) > 28:
            lab = lab[:25] + "…"
        labels[n] = str(lab).replace("\\n", "\n")

    nx.draw_networkx_nodes(
        G, pos, node_color=node_colors, node_size=900, alpha=0.95, ax=ax, edgecolors="#334155"
    )
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=7, font_color="#f8fafc", ax=ax)
    nx.draw_networkx_edges(
        G,
        pos,
        edge_color="#475569",
        arrows=True,
        arrowsize=14,
        connectionstyle="arc3,rad=0.08",
        ax=ax,
        alpha=0.85,
    )

    edge_labels = {}
    for u, v, d in G.edges(data=True):
        lab = d.get("label", "")
        if lab:
            edge_labels[(u, v)] = str(lab)[:12]

    if edge_labels:
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, font_size=6, font_color="#94a3b8", ax=ax, rotate=False
        )

    if title:
        ax.set_title(title, color="#e2e8f0", fontsize=12, pad=12)
    ax.axis("off")
    plt.tight_layout()

    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    buf.seek(0)
    return buf.read()


def render_dot_image(
    dot_str: str,
    *,
    agent2_result: Optional[Dict[str, Any]] = None,
    prefer_matplotlib_highlight: bool = False,
) -> Tuple[Optional[bytes], str]:
    """
    Returns (png_bytes, note).
    If agent2_result has faulty_nodes, use matplotlib path to highlight faults
    (unless prefer_matplotlib_highlight is False and pydot works without highlights).
    """
    if not dot_str or not dot_str.strip():
        return None, "No DOT data."

    faults = fault_node_ids(agent2_result) if agent2_result else set()

    # With faults, matplotlib gives clear highlighting
    if faults:
        G = graph_from_dot_string(dot_str)
        if G is None:
            return None, "Could not parse DOT for drawing."
        png = graph_to_png_matplotlib(G, highlight=faults, title="Faulty nodes (red)")
        if png:
            return png, "matplotlib (faults highlighted)"
        return None, "Matplotlib render failed."

    if not prefer_matplotlib_highlight:
        png = dot_string_to_png_pydot(dot_str)
        if png:
            return png, "Graphviz (pydot)"

    G = graph_from_dot_string(dot_str)
    if G is None:
        return None, "Could not parse DOT."
    png = graph_to_png_matplotlib(G, highlight=None, title="Block graph")
    if png:
        return png, "matplotlib"
    return None, "Render failed."
