"""
Multi-Agent Program Repair — Streamlit UI
Run: streamlit run streamlit_app.py
"""
import os
from pathlib import Path

import streamlit as st

from graph_image import render_dot_image
from pipeline_ui import ROOT, ensure_work_dir, run_agent1, run_agent2, run_agent3, run_agent4

try:
    from dotenv import load_dotenv

    # Do not override os.environ — so a key set in the UI (or shell) wins over .env
    load_dotenv(ROOT / ".env", override=False)
except ImportError:
    pass

STEM = "session"

st.set_page_config(
    page_title="Multi-Agent Program Repair",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;600;700&family=JetBrains+Mono:wght@400&display=swap');
    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
    .stTextArea textarea {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 13px !important;
        border-radius: 10px !important;
    }
    .title-center {
        text-align: center;
        padding: 0.5rem 0 1.25rem 0;
    }
    .title-center h1 {
        color: #f8fafc;
        font-weight: 700;
        font-size: 1.75rem;
        margin: 0;
        letter-spacing: -0.02em;
    }
    .title-center p {
        color: #94a3b8;
        margin: 0.4rem 0 0 0;
        font-size: 0.95rem;
    }
    div[data-testid="stExpander"] {
        border-radius: 10px !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


def patch_agent_api_keys():
    """Sync GEMINI_API_KEY into agent modules + google.generativeai global config."""
    key = os.getenv("GEMINI_API_KEY", "").strip()
    try:
        import google.generativeai as genai

        if key:
            genai.configure(api_key=key)
    except Exception:
        pass

    import sys

    for mod_name in ("agent1", "agent2", "agent3", "agent4"):
        try:
            m = sys.modules.get(mod_name) or __import__(mod_name)
            m.GEMINI_API_KEY = key or None
            if getattr(m, "genai", None) is not None:
                m.HAS_GENAI = bool(key and m.genai is not None)
        except Exception:
            pass


def apply_stored_api_key_to_environ():
    """Re-apply UI key on every rerun (password field clears; load_dotenv must not wipe it)."""
    stored = st.session_state.get("applied_api_key", "").strip()
    if stored:
        os.environ["GEMINI_API_KEY"] = stored


def init_state():
    if "sid" not in st.session_state:
        import uuid

        st.session_state.sid = str(uuid.uuid4())[:8]
    if "work_dir" not in st.session_state:
        st.session_state.work_dir = ensure_work_dir(st.session_state.sid)
    defaults = [
        (
            "code",
            """def add(a, b):
    x = a + b
    return a
""",
        ),
        ("dot_path", None),
        ("dot_text", None),
        ("agent1_meta", None),
        ("agent2_out", None),
        ("agent3_out", None),
        ("agent4_out", None),
        ("error", None),
        ("step_done", 0),
        ("output_tab", 1),
        ("manual_api_key", ""),
        ("applied_api_key", ""),
    ]
    for k, v in defaults:
        if k not in st.session_state:
            st.session_state[k] = v


def reset_pipeline():
    st.session_state.dot_path = None
    st.session_state.dot_text = None
    st.session_state.agent1_meta = None
    st.session_state.agent2_out = None
    st.session_state.agent3_out = None
    st.session_state.agent4_out = None
    st.session_state.error = None
    st.session_state.step_done = 0


init_state()


def dot_path() -> Path:
    return st.session_state.work_dir / f"{STEM}.blocks_graph.dot"


def sidebar():
    with st.sidebar:
        st.markdown("### Gemini API")
        key_in = st.text_input(
            "API key",
            value=st.session_state.get("manual_api_key", ""),
            type="password",
            placeholder="AIza…",
            label_visibility="collapsed",
        )
        st.session_state.manual_api_key = key_in
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Apply key", use_container_width=True):
                if key_in.strip():
                    st.session_state.applied_api_key = key_in.strip()
                    os.environ["GEMINI_API_KEY"] = st.session_state.applied_api_key
                    patch_agent_api_keys()
                    st.success("Applied — key saved for this session")
                    st.rerun()
                else:
                    st.warning("Enter a key")
        with c2:
            if st.button("Clear", use_container_width=True):
                st.session_state.manual_api_key = ""
                st.session_state.applied_api_key = ""
                os.environ.pop("GEMINI_API_KEY", None)
                load_dotenv(ROOT / ".env", override=False)
                patch_agent_api_keys()
                st.rerun()

        if st.session_state.get("applied_api_key"):
            st.caption("Session key active (hidden)")
        elif os.getenv("GEMINI_API_KEY"):
            st.caption("Key from environment / `.env`")
        else:
            st.caption("No key — apply above or set `.env`")

        st.divider()
        if st.button("Reset pipeline", use_container_width=True):
            reset_pipeline()
            st.rerun()


def run_step1():
    patch_agent_api_keys()
    st.session_state.error = None
    with st.spinner("Agent 1…"):
        dot_text, meta, _ = run_agent1(st.session_state.code, st.session_state.work_dir, STEM)
    st.session_state.dot_text = dot_text
    st.session_state.agent1_meta = meta
    st.session_state.dot_path = dot_path()
    st.session_state.step_done = max(st.session_state.step_done, 1)
    st.session_state.agent2_out = None
    st.session_state.agent3_out = None
    st.session_state.agent4_out = None
    st.session_state.output_tab = 1


def run_step2():
    patch_agent_api_keys()
    st.session_state.error = None
    p = st.session_state.dot_path
    if not p or not Path(p).exists():
        st.session_state.error = "Run Agent 1 first."
        return
    with st.spinner("Agent 2…"):
        out = run_agent2(Path(p), st.session_state.work_dir)
    st.session_state.agent2_out = out
    st.session_state.step_done = max(st.session_state.step_done, 2)
    st.session_state.agent3_out = None
    st.session_state.agent4_out = None
    st.session_state.output_tab = 2


def run_step3():
    patch_agent_api_keys()
    st.session_state.error = None
    p = st.session_state.dot_path
    a2 = st.session_state.agent2_out
    if not p or not a2:
        st.session_state.error = "Run Agents 1 and 2 first."
        return
    with st.spinner("Agent 3…"):
        out = run_agent3(a2, Path(p), st.session_state.work_dir)
    st.session_state.agent3_out = out
    st.session_state.step_done = max(st.session_state.step_done, 3)
    st.session_state.agent4_out = None
    st.session_state.output_tab = 3


def run_step4():
    patch_agent_api_keys()
    st.session_state.error = None
    a3 = st.session_state.agent3_out
    if not a3:
        st.session_state.error = "Run Agent 3 first."
        return
    with st.spinner("Agent 4…"):
        fixed = run_agent4(st.session_state.code, a3)
    st.session_state.agent4_out = fixed
    st.session_state.step_done = 4
    st.session_state.output_tab = 4


def run_full():
    reset_pipeline()
    run_step1()
    if st.session_state.error:
        return
    run_step2()
    if st.session_state.error:
        return
    run_step3()
    if st.session_state.error:
        return
    run_step4()


def _show_graph_png(dot_str: str, agent2_json=None, title_hint: str = ""):
    """Show graph image from DOT; optional Agent 2 JSON for fault highlights."""
    png, note = render_dot_image(dot_str, agent2_result=agent2_json)
    if png:
        st.image(png, use_container_width=True)
        st.caption(f"Graph preview ({note}){title_hint}")
    else:
        st.warning(note or "Could not draw graph.")


def render_output(tab: int):
    if tab == 1:
        if st.session_state.dot_text:
            meta = st.session_state.agent1_meta or {}
            st.caption(f"{meta.get('nodes', 0)} nodes · {meta.get('edges', 0)} edges")
            _show_graph_png(st.session_state.dot_text)
            with st.expander("DOT source"):
                st.code(st.session_state.dot_text, language="dot")
        else:
            st.info("Run Agent 1 or full pipeline.")
    elif tab == 2:
        if st.session_state.agent2_out and st.session_state.dot_text:
            a2 = st.session_state.agent2_out
            faults = a2.get("faulty_nodes") or []
            st.caption(
                f"{len(faults)} faulty node(s) · "
                f"{a2.get('fault_summary', {}).get('total_faults', 0)} total faults"
            )
            _show_graph_png(st.session_state.dot_text, agent2_json=a2, title_hint=" · red = faulty")
            with st.expander("Fault analysis JSON"):
                st.json(a2)
        elif st.session_state.agent2_out:
            st.json(st.session_state.agent2_out)
            st.caption("No graph DOT in session — run Agent 1 first.")
        else:
            st.info("Run Agent 2 after Agent 1.")
    elif tab == 3:
        if st.session_state.agent3_out:
            a3 = st.session_state.agent3_out
            fg = (a3.get("full_rectified_graph") or "").strip()
            dot_src = fg if fg else st.session_state.dot_text
            if dot_src:
                _show_graph_png(dot_src)
                with st.expander("Repair JSON"):
                    st.json(a3)
                with st.expander("Rectified DOT" if fg else "Original DOT"):
                    st.code(dot_src, language="dot")
            else:
                st.json(a3)
        else:
            st.info("Run Agent 3 after Agent 2.")
    else:
        if st.session_state.agent4_out:
            st.code(st.session_state.agent4_out, language="python")
        else:
            st.info("Run Agent 4 after Agent 3.")


def main():
    apply_stored_api_key_to_environ()
    patch_agent_api_keys()
    sidebar()

    st.markdown(
        '<div class="title-center"><h1>Multi-Agent Program Repair</h1>'
        "<p>Graph pipeline: build graph → find faults → repair graph → fix code</p></div>",
        unsafe_allow_html=True,
    )

    left, right = st.columns([1.15, 1], gap="large")

    with left:
        st.markdown("**Python code**")
        st.session_state.code = st.text_area(
            "code",
            value=st.session_state.code,
            height=360,
            label_visibility="collapsed",
            placeholder="Paste buggy Python here…",
        )

    with right:
        st.markdown("**Agents**")
        r1, r2, r3, r4 = st.columns(4)
        with r1:
            if st.button("1 · Graph", use_container_width=True):
                try:
                    run_step1()
                except Exception as e:
                    st.session_state.error = str(e)
                st.rerun()
        with r2:
            if st.button("2 · Faults", use_container_width=True):
                try:
                    run_step2()
                except Exception as e:
                    st.session_state.error = str(e)
                st.rerun()
        with r3:
            if st.button("3 · Repair", use_container_width=True):
                try:
                    run_step3()
                except Exception as e:
                    st.session_state.error = str(e)
                st.rerun()
        with r4:
            if st.button("4 · Code", use_container_width=True):
                try:
                    run_step4()
                except Exception as e:
                    st.session_state.error = str(e)
                st.rerun()

        if st.button("Run full pipeline (1→4)", type="primary", use_container_width=True):
            with st.spinner("Running…"):
                try:
                    run_full()
                except Exception as e:
                    st.session_state.error = str(e)
            st.rerun()

        st.markdown("**Output**")
        view = st.radio(
            "view",
            ["Graph", "Faults", "Repair", "Code"],
            horizontal=True,
            label_visibility="collapsed",
            index=st.session_state.output_tab - 1,
        )
        st.session_state.output_tab = ["Graph", "Faults", "Repair", "Code"].index(view) + 1
        render_output(st.session_state.output_tab)

    if st.session_state.error:
        st.error(st.session_state.error)


if __name__ == "__main__":
    main()
