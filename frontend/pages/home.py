"""
Home page — Institutional landing page for ResearchGate AI.
"""
from __future__ import annotations

import streamlit as st

from config.settings import PAGE_ANALYZE, PAGE_ABOUT
from utils import session
from utils.icons import svg


def render() -> None:
    """Render the institutional home landing page."""
    # ---- Hero Section ----
    st.markdown(
        f"""
        <div class="institutional-hero">
            <div class="institutional-badge">
                {svg("award", size=13, color="#1D4ED8")}
                STEM2Connect AI Hackathon · Scientific Research Assistant
            </div>
            <h1 class="institutional-hero-title">
                Make scientific research easier to understand.
            </h1>
            <p class="institutional-hero-desc">
                Explore research abstracts, identify important findings, and organise complex scientific information into clear insights.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Hero CTA Buttons
    col_cta1, col_cta2, _spacer = st.columns([1.2, 1.1, 4.0])
    with col_cta1:
        if st.button(
            "Analyze a Paper",
            type="primary",
            use_container_width=True,
            key="home_hero_cta_analyze",
        ):
            session.set_nav_page(PAGE_ANALYZE)
            st.rerun()
    with col_cta2:
        if st.button(
            "Learn More",
            type="secondary",
            use_container_width=True,
            key="home_hero_cta_learn",
        ):
            session.set_nav_page(PAGE_ABOUT)
            st.rerun()

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    # ---- Section: Five Research Capabilities ----
    st.markdown(
        f"""
        <div class="section-container">
            <div class="section-header-block">
                <div class="section-eyebrow">Analytical Framework</div>
                <h2 class="section-title">Five Structured Research Dimensions</h2>
                <p class="section-subtitle">
                    ResearchGate AI deconstructs dense academic writing into five distinct analytical pillars, accelerating literature synthesis and critical review.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        _capability_card(
            num="01",
            title="Simple Summary",
            desc="A plain-language synthesis that translates complex methodologies and findings into accessible, straightforward summaries without loss of scientific context.",
            icon_name="file-text",
        )
        _capability_card(
            num="02",
            title="Research Objectives",
            desc="Systematic identification of primary hypotheses, study goals, and investigative questions addressed by the authors.",
            icon_name="target",
        )
        _capability_card(
            num="03",
            title="Key Findings",
            desc="Structured extraction of measured outcomes, statistical results, observed phenomena, and empirical conclusions.",
            icon_name="lightbulb",
        )

    with col2:
        _capability_card(
            num="04",
            title="Important Keywords",
            desc="Domain-specific ontology, chemical entities, genes, algorithms, and key terminology tagged for quick indexing and cross-referencing.",
            icon_name="tag",
        )
        _capability_card(
            num="05",
            title="Future Research Questions",
            desc="Analytical synthesis of unanswered questions, reported study limitations, and prospective investigation pathways.",
            icon_name="compass",
        )
        _capability_card(
            num="06",
            title="Automated Synthesis Engine",
            desc="Advanced analytical extraction with strict evidence grounding to eliminate unfounded claims and isolate verifiable textual findings.",
            icon_name="cpu",
        )

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    # ---- Section: Workflow ----
    st.markdown(
        f"""
        <div class="section-container">
            <div class="section-header-block">
                <div class="section-eyebrow">Operating Methodology</div>
                <h2 class="section-title">How the Assistant Operates</h2>
                <p class="section-subtitle">
                    A three-step scientific workflow engineered for students, educators, and domain researchers.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    w1, w2, w3 = st.columns(3, gap="medium")

    with w1:
        st.markdown(
            f"""
            <div class="workflow-card">
                <div class="workflow-step-badge">1</div>
                <div class="workflow-title">Submit Document or Abstract</div>
                <div class="workflow-body">
                    Paste raw text from a journal abstract or upload a research PDF or TXT publication. Automatic text extraction processes and validates document contents.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with w2:
        st.markdown(
            f"""
            <div class="workflow-card">
                <div class="workflow-step-badge">2</div>
                <div class="workflow-title">Let the Assistant Analyse</div>
                <div class="workflow-body">
                    The research assistant processes the document against structured analytical frameworks, strictly separating reported empirical findings from prospective hypotheses.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with w3:
        st.markdown(
            f"""
            <div class="workflow-card">
                <div class="workflow-step-badge">3</div>
                <div class="workflow-title">Review Structured Results</div>
                <div class="workflow-body">
                    Examine the five research dimensions through interactive tabs or side-by-side source comparisons, and export formatted reports as Markdown.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='section-spacer'></div>", unsafe_allow_html=True)

    # ---- Bottom CTA Block ----
    st.markdown(
        f"""
        <div class="institutional-bottom-cta">
            <div class="bottom-cta-text">
                <div class="bottom-cta-title">Ready to explore a research publication?</div>
                <div class="bottom-cta-desc">
                    Paste an abstract or load our pre-configured CRISPR gene therapy sample to explore the platform.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_b_cta, _sp = st.columns([1.5, 4.5])
    with col_b_cta:
        if st.button("Open Analysis Workspace", type="primary", use_container_width=True, key="home_bottom_cta"):
            session.set_nav_page(PAGE_ANALYZE)
            st.rerun()


def _capability_card(num: str, title: str, desc: str, icon_name: str) -> None:
    st.markdown(
        f"""
        <div class="capability-card">
            <div class="capability-header">
                <div class="capability-icon-box">
                    {svg(icon_name, 16, "#1D4ED8")}
                </div>
                <div class="capability-num">{num}</div>
            </div>
            <div class="capability-title">{title}</div>
            <div class="capability-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
