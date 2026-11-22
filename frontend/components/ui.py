"""
Reusable UI components — navbar, hero, dimension cards, results, and footer.
Institutional research design with zero technical information leakage.
"""
from __future__ import annotations

import html
import datetime
import streamlit as st

from config.settings import (
    APP_TITLE,
    APP_SUBTITLE,
    PAGE_HOME,
    PAGE_ANALYZE,
    PAGE_ABOUT,
    PAGE_AUTH,
)
from utils.icons import svg
from utils import session
from utils.export import generate_markdown_report, format_dimension_text


# ---------------------------------------------------------------------------
# Institutional Top Horizontal Navigation Bar
# ---------------------------------------------------------------------------

def render_navbar(current_page: str) -> None:
    """Render the top horizontal institutional navbar."""
    is_auth = session.is_authenticated()
    auth_user = session.get_auth_user() or {}
    user_name = auth_user.get("full_name", "Researcher")
    first_name = user_name.split()[0] if user_name else "Researcher"

    # Brand Wordmark and Top Bar Structure
    st.markdown(
        f"""
        <div class="institutional-navbar">
            <div class="navbar-brand-section">
                <div class="navbar-emblem">R</div>
                <div class="navbar-brand-titles">
                    <span class="navbar-title">{APP_TITLE}</span>
                    <span class="navbar-division">Institutional Research Assistant</span>
                </div>
            </div>
            <div class="navbar-divider-line"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Streamlit Navigation Bar Columns — layout differs by authentication state.
    # Authenticated:   Home | Analyze Paper | About | <fill> | Profile | Sign Out
    # Unauthenticated: <fill> | Sign In | Register
    if is_auth:
        col_h, col_a, col_ab, _fill, col_auth1, col_auth2 = st.columns(
            [0.85, 1.25, 0.85, 4.2, 1.15, 1.1], gap="small"
        )

        with col_h:
            is_active = (current_page == PAGE_HOME)
            if st.button(
                "Home",
                key="nav_btn_home",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                session.set_nav_page(PAGE_HOME)
                st.rerun()

        with col_a:
            is_active = (current_page == PAGE_ANALYZE)
            if st.button(
                "Analyze Paper",
                key="nav_btn_analyze",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                session.set_nav_page(PAGE_ANALYZE)
                st.rerun()

        with col_ab:
            is_active = (current_page == PAGE_ABOUT)
            if st.button(
                "About",
                key="nav_btn_about",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                session.set_nav_page(PAGE_ABOUT)
                st.rerun()

    else:
        # Guest layout: brand fills the left; only auth actions appear on the right.
        _, col_auth1, col_auth2 = st.columns([7.5, 1.15, 1.1], gap="small")

    if not is_auth:
        with col_auth1:
            is_active = (current_page == PAGE_AUTH and session.get_auth_page() == "login")
            if st.button(
                "Sign In",
                key="nav_btn_signin",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                session.set_auth_page("login")
                session.set_nav_page(PAGE_AUTH)
                st.rerun()

        with col_auth2:
            is_active = (current_page == PAGE_AUTH and session.get_auth_page() == "signup")
            if st.button(
                "Register",
                key="nav_btn_signup",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                session.set_auth_page("signup")
                session.set_nav_page(PAGE_AUTH)
                st.rerun()
    else:
        with col_auth1:
            is_active = (current_page == PAGE_AUTH)
            display_label = f"Dr. {first_name}" if not first_name.startswith("Dr") else first_name
            if st.button(
                display_label,
                key="nav_btn_account",
                use_container_width=True,
                type="primary" if is_active else "secondary",
            ):
                session.set_nav_page(PAGE_AUTH)
                st.rerun()

        with col_auth2:
            if st.button(
                "Sign Out",
                key="nav_btn_logout",
                use_container_width=True,
                type="secondary",
            ):
                session.logout()
                # Redirect to login page after logout; the auth gate in app.py
                # would redirect PAGE_HOME anyway, but set it explicitly here
                # so the user lands on the login form immediately.
                session.set_auth_page("login")
                session.set_nav_page(PAGE_AUTH)
                st.rerun()

    st.markdown("<div class='navbar-bottom-border'></div>", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# Dimension Cards (Structured Research Results)
# ---------------------------------------------------------------------------

_DIM_CONFIG: dict[str, dict] = {
    "summary": {
        "icon":     "file-text",
        "num":      "01",
        "title":    "Simple Summary",
        "subtitle": "Accessible Synthesis & Core Takeaway",
    },
    "objectives": {
        "icon":     "target",
        "num":      "02",
        "title":    "Research Objectives",
        "subtitle": "Primary Hypotheses & Experimental Aims",
    },
    "findings": {
        "icon":     "lightbulb",
        "num":      "03",
        "title":    "Key Findings",
        "subtitle": "Empirical Observations, Measurements & Significance",
    },
    "keywords": {
        "icon":     "tag",
        "num":      "04",
        "title":    "Important Keywords",
        "subtitle": "Scientific Ontology & Domain Terminology",
    },
    "questions": {
        "icon":     "compass",
        "num":      "05",
        "title":    "Future Research Questions",
        "subtitle": "Open Frontiers, Limitations & Next Inquiries",
    },
}


def render_dimension_card(key: str, results: dict | None, error: str | None) -> None:
    """Render a clean, institutional dimension card."""
    cfg = _DIM_CONFIG[key]

    if results:
        status_tag = '<span class="inst-tag inst-tag--verified">Verified Extraction</span>'
        content = _build_content(key, results)
    elif error:
        status_tag = '<span class="inst-tag inst-tag--error">Extraction Failed</span>'
        content = '<p class="dim-empty-state">Analysis failed. Please refer to the diagnostic notification above.</p>'
    else:
        status_tag = '<span class="inst-tag inst-tag--waiting">Awaiting Document</span>'
        content = '<p class="dim-empty-state">Submit an abstract or upload a document to populate this dimension.</p>'

    st.markdown(
        f"""
        <div class="institutional-card dim-card">
            <div class="dim-card-header">
                <div class="dim-card-left">
                    <span class="dim-num-badge">{cfg['num']}</span>
                    <div class="dim-title-group">
                        <div class="dim-title">{cfg['title']}</div>
                        <div class="dim-subtitle">{cfg['subtitle']}</div>
                    </div>
                </div>
                <div>{status_tag}</div>
            </div>
            <div class="dim-card-body">{content}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _build_content(key: str, results: dict) -> str:
    """Build accessible inner HTML for a completed dimension."""
    if key == "summary":
        summary_val = results.get("summary", "Not stated in the source document.")
        if "not stated" in summary_val.lower():
            return (
                '<div class="dim-row dim-row--omitted">'
                '<span class="dim-bullet">—</span>'
                '<span class="dim-omitted-notice">Not explicitly stated in the source publication.</span>'
                '</div>'
            )
        return f'<p class="dim-summary-prose">{html.escape(summary_val)}</p>'

    if key == "keywords":
        kws = results.get("keywords", [])
        if not kws:
            return '<p class="dim-empty-state">No keywords extracted from the document.</p>'
        tag_html = "".join(
            f'<span class="inst-keyword-chip">{html.escape(str(kw))}</span>'
            for kw in kws
        )
        return f'<div class="inst-keyword-cloud">{tag_html}</div>'

    items = results.get(key, [])
    if not items:
        return '<p class="dim-empty-state">No items reported for this dimension.</p>'

    prefix_html = ""
    if key == "questions":
        prefix_html = (
            '<div class="inst-disclaimer-box">'
            '<strong>Institutional Notice:</strong> The points below represent speculative research frontiers '
            'and hypotheses synthesized from stated study limitations, not verified conclusions.'
            '</div>'
        )

    rows = []
    for item in items:
        clean_item = str(item).strip()
        if "not stated" in clean_item.lower():
            rows.append(
                '<div class="dim-row dim-row--omitted">'
                '<span class="dim-bullet">—</span>'
                '<span class="dim-omitted-notice">Not explicitly reported in the source document.</span>'
                '</div>'
            )
        else:
            rows.append(
                f'<div class="dim-row">'
                f'<span class="dim-bullet">▪</span>'
                f'<span class="dim-row-content">{html.escape(clean_item)}</span>'
                f'</div>'
            )

    return prefix_html + "".join(rows)


# ---------------------------------------------------------------------------
# Empty State Preview
# ---------------------------------------------------------------------------

def render_preview() -> None:
    """Render clean institutional preview placeholders before running analysis."""
    st.markdown(
        f"""
        <div class="preview-section-header">
            <h3 class="preview-title">
                {svg("layout-grid", 17, "#1D4ED8")}
                Structured Analytical Output Framework
            </h3>
            <p class="preview-desc">
                Submit an abstract above or upload a research document to generate structured results across these five analytical dimensions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        render_dimension_card("summary", results=None, error=None)
        render_dimension_card("objectives", results=None, error=None)
        render_dimension_card("findings", results=None, error=None)
    with col2:
        render_dimension_card("keywords", results=None, error=None)
        render_dimension_card("questions", results=None, error=None)


# ---------------------------------------------------------------------------
# Results Display
# ---------------------------------------------------------------------------

def render_results(results: dict | None, error: str | None, submitted: str) -> None:
    """Display completed research dimensions with export options and view toggles."""
    if error:
        st.error(
            "Unable to complete analysis. Please verify your submission and try again in a moment.",
            icon=":material/error:",
        )
        return

    if not results:
        st.warning(
            "No results available. Please submit a research document to initiate analysis.",
            icon=":material/warning:",
        )
        return

    timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_md = generate_markdown_report(
        results=results,
        original_text=submitted,
        model_name="ResearchGate Assistant",
    )

    # Action Toolbar
    col_tb1, col_tb2, col_tb3 = st.columns([2.6, 1.4, 1.0], gap="small")

    with col_tb1:
        st.markdown(
            f"""
            <div class="results-meta-banner">
                <span class="meta-status-dot"></span>
                <span class="meta-label">Analysis Complete</span>
                <span class="meta-sep">·</span>
                <span class="meta-info">{len(submitted):,} characters · ~{len(submitted.split()):,} words</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_tb2:
        st.download_button(
            label="Download Report (.md)",
            data=report_md,
            file_name=f"research_analysis_{timestamp_str}.md",
            mime="text/markdown",
            icon=":material/download:",
            use_container_width=True,
            help="Download complete structured analysis and source text in Markdown format.",
            key="btn_download_report",
        )

    with col_tb3:
        if st.button(
            "New Analysis",
            icon=":material/refresh:",
            use_container_width=True,
            help="Clear current analysis and analyze another document.",
            key="btn_reset_results",
        ):
            session.clear_analysis()
            st.rerun()

    # Layout Mode Toggle
    layout_mode = st.radio(
        "Display Layout",
        options=["Tabbed Dimensions", "Side-by-Side Comparison"],
        horizontal=True,
        key="results_layout_mode",
        label_visibility="collapsed",
    )

    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

    if layout_mode == "Side-by-Side Comparison":
        col_src, col_dims = st.columns([1.1, 1.3], gap="large")

        with col_src:
            st.markdown(
                f"""
                <div class="institutional-card">
                    <div class="dim-card-header" style="border-bottom:1px solid #E2E8F0;padding:12px 16px;">
                        <div class="dim-title" style="font-size:0.95rem;">
                            {svg("file-text", 15, "#1D4ED8")} Source Document Text
                        </div>
                        <span style="font-size:0.75rem;color:#64748B;">{len(submitted):,} chars</span>
                    </div>
                    <div class="source-document-prose">
                        {html.escape(submitted)}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_dims:
            for k in ["summary", "objectives", "findings", "keywords", "questions"]:
                render_dimension_card(k, results=results, error=error)

    else:
        # Tabbed View
        with st.expander("View Submitted Source Text", expanded=False):
            st.markdown(
                f'<div class="source-document-prose">{html.escape(submitted)}</div>',
                unsafe_allow_html=True,
            )
            st.caption(f"Document Metrics: {len(submitted):,} characters · ~{len(submitted.split()):,} words")

        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "01. Summary",
            "02. Objectives",
            "03. Key Findings",
            "04. Keywords",
            "05. Future Questions",
        ])

        keys = ["summary", "objectives", "findings", "keywords", "questions"]
        for tab, k in zip([tab1, tab2, tab3, tab4, tab5], keys):
            with tab:
                render_dimension_card(k, results=results, error=error)
                with st.expander("Copy Section Markdown", expanded=False):
                    st.code(format_dimension_text(k, results), language="markdown")

    with st.expander("Copy Complete Markdown Report", expanded=False):
        st.code(report_md, language="markdown")


# ---------------------------------------------------------------------------
# Institutional Footer
# ---------------------------------------------------------------------------

def render_footer() -> None:
    """Render minimal institutional footer without technical stack details."""
    st.markdown(
        f"""
        <footer class="institutional-footer">
            <div class="footer-top-line"></div>
            <div class="footer-grid">
                <div class="footer-col-brand">
                    <div class="footer-brand-title">{APP_TITLE}</div>
                    <div class="footer-brand-subtitle">Scientific Research Assistant · Institutional Edition</div>
                </div>
                <div class="footer-col-disclaimer">
                    <div class="footer-disclaimer-text">
                        {svg("shield-alert", 13, "#64748B")}
                        AI-generated insights are synthesized for research screening and must be verified against primary scientific literature.
                    </div>
                </div>
                <div class="footer-col-hackathon">
                    <div class="footer-badge">STEM2Connect AI Hackathon</div>
                    <div class="footer-tech-stack">Academic Research Portal</div>
                </div>
            </div>
        </footer>
        """,
        unsafe_allow_html=True,
    )
