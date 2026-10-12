import sys
from pathlib import Path

import streamlit as st
from PIL import Image

project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from router.engine import AdaptiveRouter, RequestMetaData

SAMPLE_QUESTIONS = {
    "Simple · explain an API (8B route)": (
        "Explain what an API is in one sentence.",
        False,
    ),
    "Complex · plan HTTP retries (70B route)": (
        "Explain step by step how to design a Python function for retrying "
        "failed HTTP requests. Include exponential backoff, a maximum retry "
        "count, handling timeouts, and how to avoid retrying non-recoverable "
        "errors. Then compare this approach with retrying at fixed intervals, "
        "and explain the trade-offs in latency and reliability. Include a short "
        "Python example and describe two tests that would verify the behavior.",
        False,
    ),
    "Private · summarize a note (Qwen route)": (
        "Summarize this note: The project meeting is at 2 p.m. on Thursday. "
        "Please bring the draft budget.",
        True,
    ),
}


def load_sample_question():
    prompt, private = SAMPLE_QUESTIONS[st.session_state.sample_question]
    st.session_state.prompt = prompt
    st.session_state.privacy_restricted = private


st.set_page_config(
    page_title="LLM Router Gateway and Adaptive Router",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 LLM Router Gateway and Adaptive Router")
st.caption(
    "Interactive routing preview · demonstrates route selection without "
    "calling model providers or using API keys."
)

tester_tab, benchmark_tab = st.tabs(["🚀 Gateway & project guide", "📊 Benchmarks"])
router_engine = AdaptiveRouter()

with tester_tab:
    controls_col, guide_col = st.columns([0.9, 1.1], gap="medium")
    send_btn = False

    with controls_col:
        st.subheader("Test a request")
        st.selectbox(
            "Sample questions",
            options=list(SAMPLE_QUESTIONS),
            key="sample_question",
        )
        st.button("Load sample question", on_click=load_sample_question)
        with st.form("gateway_request"):
            prompt = st.text_area(
                "Prompt",
                height=100,
                placeholder="Type a prompt or load a sample question above.",
                key="prompt",
            )
            max_latency = st.slider("Latency target (ms)", 100, 3000, 1000)
            privacy = st.checkbox("Restricted / private data", key="privacy_restricted")
            send_btn = st.form_submit_button(
                "Preview routing", type="primary", use_container_width=True
            )
        st.caption("Public preview · no API key or backend setup required")

    with guide_col:
        st.subheader("Meet your project guide")
        tour_html = Path(__file__).with_name("mascot_tour.html").read_text(encoding="utf-8")
        st.iframe(tour_html, height=400)

    if send_btn:
        selected_model = router_engine.route(
            RequestMetaData(
                prompt=prompt,
                max_latency_ms=max_latency,
                privacy_restricted=privacy,
            )
        )

        st.divider()
        model_col, provider_col, keys_col = st.columns(3)
        model_col.metric("Selected route", selected_model)
        provider_col.metric("Provider request", "Not made")
        keys_col.metric("API keys used", "No")
        st.subheader("Routing preview")
        st.info(
            f"The router selects **{selected_model}** for this request. This "
            "public preview demonstrates route selection only; it does not "
            "generate a model answer or send your prompt to an AI provider."
        )

with benchmark_tab:
    st.header("Benchmark & Pareto Frontier Analysis")
    st.markdown(
        "Comparing quality retention vs. cost per 1k requests across four routing strategies."
    )

    chart_path = project_root / "docs" / "pareto_frontier.png"
    if chart_path.exists():
        image = Image.open(chart_path)
        st.image(
            image,
            caption="Pareto Frontier: Quality Retention vs. Cost per 1k Requests",
            width="stretch",
        )
    else:
        st.warning(
            "Pareto chart not generated yet. Run `python benchmarks/evaluate.py` "
            "in your terminal to generate it."
        )
