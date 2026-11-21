"""
About page — Institutional overview, mission, analytical framework, and platform profile.
All technical infrastructure details and internal endpoint names are excluded.
"""
from __future__ import annotations

import streamlit as st

from config.settings import PAGE_ANALYZE
from utils import session
from utils.icons import svg


def render() -> None:
    """Render the institutional About page."""
    # ---- Hero ----
    st.markdown(
        f"""
        <div class="institutional-hero">
            <div class="institutional-badge">
                {svg("info", 13, "#1D4ED8")}
                Institutional Information
            </div>
            <h1 class="institutional-hero-title">About ResearchGate AI</h1>
            <p class="institutional-hero-desc">
                An AI-assisted scientific reading and literature exploration platform built to make peer-reviewed research accessible, transparent, and structured.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Main Content Grid ----
    col_main, col_sidebar = st.columns([2.0, 1.1], gap="large")

    with col_main:
        # Section 1: Purpose & Mission
        st.markdown(
            f"""
            <div class="about-section">
                <h2 class="about-heading">
                    {svg("target", 18, "#1D4ED8")}
                    Mission & Background
                </h2>
                <p class="about-paragraph">
                    Every year, hundreds of thousands of peer-reviewed papers are published across biomedical, physical, and computational disciplines. For undergraduate students, educators, and cross-disciplinary researchers, engaging with newly published literature often poses formidable challenges:
                </p>
                <ul class="about-list">
                    <li><strong>Jargon-dense academic prose:</strong> Highly specialized vocabulary often obscures underlying experimental logic and core findings.</li>
                    <li><strong>Unstructured document formats:</strong> Abstracts frequently compress hypotheses, methods, and numerical metrics into single paragraphs without standardized demarcation.</li>
                    <li><strong>Cognitive overload:</strong> Preliminary literature screening demands substantial time to separate empirical claims from speculative future directions.</li>
                </ul>
                <p class="about-paragraph">
                    <strong>ResearchGate AI</strong> was designed for the <strong>STEM2Connect AI Hackathon</strong> to address these barriers. By combining large language model intelligence with structured schema parsing, the assistant decomposes academic abstracts into five rigorous analytical dimensions.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Section 2: Who Can Use It
        st.markdown(
            f"""
            <div class="about-section">
                <h2 class="about-heading">
                    {svg("users", 18, "#1D4ED8")}
                    Target Audience
                </h2>
                <div class="audience-grid">
                    <div class="audience-card">
                        <div class="audience-title">Students & Learners</div>
                        <div class="audience-desc">Quickly grasp the purpose and outcomes of foundational papers without being overwhelmed by specialized terminology.</div>
                    </div>
                    <div class="audience-card">
                        <div class="audience-title">Cross-Disciplinary Researchers</div>
                        <div class="audience-desc">Rapidly survey adjacent domains to identify relevant methodologies, datasets, and benchmark comparisons.</div>
                    </div>
                    <div class="audience-card">
                        <div class="audience-title">Educators & Mentors</div>
                        <div class="audience-desc">Create structured reading guides and comprehension materials from primary scientific literature.</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Section 3: The Five Analytical Dimensions
        st.markdown(
            f"""
            <div class="about-section">
                <h2 class="about-heading">
                    {svg("layers", 18, "#1D4ED8")}
                    The Five Analytical Dimensions
                </h2>
                <p class="about-paragraph">
                    To maintain research integrity and prevent misinformation, each document is analyzed across five isolated dimensions:
                </p>
                <div class="dimensions-breakdown">
                    <div class="dim-breakdown-row">
                        <strong>1. Simple Summary:</strong> Plain-language synthesis explaining the study’s central question and findings.
                    </div>
                    <div class="dim-breakdown-row">
                        <strong>2. Research Objectives:</strong> Explicit enumeration of hypotheses and tested conditions.
                    </div>
                    <div class="dim-breakdown-row">
                        <strong>3. Key Findings:</strong> Direct extraction of reported measurements, p-values, percentages, and outcomes. If numerical claims are absent from the source, the system explicitly reports their omission.
                    </div>
                    <div class="dim-breakdown-row">
                        <strong>4. Important Keywords:</strong> Extraction of scientific ontology, proteins, compounds, models, and algorithms.
                    </div>
                    <div class="dim-breakdown-row">
                        <strong>5. Future Research Questions:</strong> AI-synthesized research frontiers derived from stated limitations, explicitly demarcated as speculative next steps.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_sidebar:
        # Platform Profile Box
        st.markdown(
            f"""
            <div class="institutional-card">
                <div class="inst-card-title">
                    {svg("server", 15, "#1D4ED8")}
                    Platform Profile
                </div>
                <div class="tech-spec-list">
                    <div class="tech-spec-item">
                        <div class="tech-spec-label">Service Purpose</div>
                        <div class="tech-spec-val">Literature Synthesis & Scientific Exploration</div>
                    </div>
                    <div class="tech-spec-item">
                        <div class="tech-spec-label">Analytical Framework</div>
                        <div class="tech-spec-val">5-Dimension Structured Extraction</div>
                    </div>
                    <div class="tech-spec-item">
                        <div class="tech-spec-label">Document Ingestion</div>
                        <div class="tech-spec-val">PDF Publications & Scientific Abstracts</div>
                    </div>
                    <div class="tech-spec-item">
                        <div class="tech-spec-label">Verification Integrity</div>
                        <div class="tech-spec-val">Grounded Text Boundaries & Absence Reporting</div>
                    </div>
                    <div class="tech-spec-item">
                        <div class="tech-spec-label">Access Model</div>
                        <div class="tech-spec-val">Institutional Researcher Portal</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Hackathon Context Box
        st.markdown(
            f"""
            <div class="institutional-card" style="margin-top:16px;">
                <div class="inst-card-title">
                    {svg("award", 15, "#1D4ED8")}
                    Hackathon Context
                </div>
                <div style="font-size:0.83rem;color:#475569;line-height:1.6;padding:14px 16px;">
                    <p style="margin-bottom:8px;">
                        <strong>Event:</strong> STEM2Connect AI Hackathon
                    </p>
                    <p style="margin-bottom:8px;">
                        <strong>Track:</strong> AI Tools for Scientific Education & Discovery
                    </p>
                    <p style="margin-bottom:0;">
                        <strong>Design Ethos:</strong> Traditional institutional design; human-centered, minimal, verifiable, and free of hyperbole.
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:16px;'></div>", unsafe_allow_html=True)
        if st.button("Open Analysis Workspace", type="primary", use_container_width=True, key="about_open_workspace"):
            session.set_nav_page(PAGE_ANALYZE)
            st.rerun()
