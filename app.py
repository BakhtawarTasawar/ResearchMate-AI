"""
====================================================================
ResearchMate AI - Scientific Research Assistant
Developed for the STEM2Connect AI Hackathon
====================================================================
A modern, light-themed SaaS dashboard designed to help students,
researchers, and academics understand scientific abstracts through
clear, structured insights. Styled with consistent Lucide-style outline icons.
"""

from pathlib import Path
import streamlit as st

# ====================================================================
# 1. Page Configuration & Setup
# ====================================================================
FAVICON_PATH = Path(__file__).parent / "favicon.svg"
PAGE_ICON = str(FAVICON_PATH) if FAVICON_PATH.exists() else None

st.set_page_config(
    page_title="ResearchMate AI - Scientific Research Assistant",
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)


# ====================================================================
# 2. Custom CSS Loader
# ====================================================================
def load_custom_css():
    """Load external CSS stylesheet for clean SaaS styling."""
    css_path = Path(__file__).parent / "styles.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        st.markdown(
            """
            <style>
                .block-container { padding-top: 2rem; max-width: 1160px; }
            </style>
            """,
            unsafe_allow_html=True
        )


load_custom_css()


# ====================================================================
# 3. Lucide-Style SVG Icon System
# ====================================================================
LUCIDE_SVG_PATHS = {
    "microscope": (
        '<path d="M6 18h8"/><path d="M3 22h18"/><path d="M14 22a7 7 0 1 0 0-14h-1"/>'
        '<path d="M9 14h2"/><path d="M9 12a2 2 0 0 1-2-2V6h6v4a2 2 0 0 1-2 2Z"/>'
        '<path d="M12 6V3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3"/>'
    ),
    "house": (
        '<path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8"/>'
        '<path d="M3 10a2 2 0 0 1 .709-1.528l7-5.999a2 2 0 0 1 2.582 0l7 5.999A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>'
    ),
    "file-text": (
        '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>'
        '<path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M10 9H8"/><path d="M16 13H8"/><path d="M16 17H8"/>'
    ),
    "file-search": (
        '<path d="M14 2v4a2 2 0 0 0 2 2h4"/>'
        '<path d="M4.268 21a2 2 0 0 0 1.732 1H18a2 2 0 0 0 2-2V7l-5-5H6a2 2 0 0 0-2 2v3"/>'
        '<path d="m9 18-1.5-1.5"/><circle cx="5" cy="14" r="3"/>'
    ),
    "file-check": (
        '<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/>'
        '<path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="m9 15 2 2 4-4"/>'
    ),
    "book-open": (
        '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>'
        '<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>'
    ),
    "target": (
        '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>'
    ),
    "lightbulb": (
        '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/>'
        '<path d="M9 18h6"/><path d="M10 22h4"/>'
    ),
    "tag": (
        '<path d="M12.586 2.586A2 2 0 0 0 11.172 2H4a2 2 0 0 0-2 2v7.172a2 2 0 0 0 .586 1.414l8.704 8.704a2.426 2.426 0 0 0 3.42 0l6.58-6.58a2.426 2.426 0 0 0 0-3.42z"/>'
        '<circle cx="7.5" cy="7.5" r=".5" fill="currentColor"/>'
    ),
    "compass": (
        '<circle cx="12" cy="12" r="10"/>'
        '<polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>'
    ),
    "info": (
        '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>'
    ),
    "clock": (
        '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>'
    ),
    "circle-dot": (
        '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="2"/>'
    ),
    "check-circle": (
        '<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>'
    ),
    "shield-alert": (
        '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10"/>'
        '<line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>'
    ),
    "award": (
        '<circle cx="12" cy="8" r="6"/><path d="M15.477 12.89 17 22l-5-3-5 3 1.523-9.11"/>'
    ),
    "cpu": (
        '<rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/>'
        '<path d="M15 2v2"/><path d="M15 20v2"/><path d="M2 15h2"/><path d="M2 9h2"/>'
        '<path d="M20 15h2"/><path d="M20 9h2"/><path d="M9 2v2"/><path d="M9 20v2"/>'
    ),
    "layers": (
        '<polygon points="12 2 2 7 12 12 22 7 12 2"/>'
        '<polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>'
    ),
    "bar-chart-2": (
        '<line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/>'
    ),
    "layout-grid": (
        '<rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/>'
        '<rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/>'
    ),
    "sparkles": (
        '<path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/>'
    ),
}


def icon_svg(name: str, size: int = 18, color: str = "currentColor", stroke_width: float = 2.0) -> str:
    """
    Return a clean, consistent inline Lucide SVG string.
    Ensures standard stroke, viewBox (24x24), and outline aesthetics.
    """
    path_data = LUCIDE_SVG_PATHS.get(name, LUCIDE_SVG_PATHS["file-text"])
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-{name}">'
        f'{path_data}'
        f'</svg>'
    )


# ====================================================================
# 4. Constants & Sample Data
# ====================================================================
PAGE_HOME = "Home"
PAGE_ANALYZE = "Analyze Paper"
PAGE_ABOUT = "About"
PAGES = [PAGE_HOME, PAGE_ANALYZE, PAGE_ABOUT]

PAGE_LABELS = {
    PAGE_HOME: ":material/home:  Home",
    PAGE_ANALYZE: ":material/description:  Analyze Paper",
    PAGE_ABOUT: ":material/info:  About",
}

SAMPLE_ABSTRACT = (
    "CRISPR-Cas9 technology has emerged as a transformative tool for targeted "
    "genome engineering, offering unprecedented precision in modifying genomic "
    "sequences. However, off-target mutations and variable editing efficiencies "
    "remain significant bottlenecks for therapeutic applications in human "
    "pluripotent stem cells (hPSCs). In this study, we developed an engineered "
    "high-fidelity Cas9 variant (eCas9-HF) combined with chemically modified "
    "single guide RNAs (sgRNAs) to address these limitations. We evaluated "
    "cleavage specificity and targeted insertion efficiency across 14 loci "
    "associated with monogenic neurodegenerative disorders. Our results "
    "demonstrated a 7.4-fold reduction in detectable off-target cleavage events "
    "while retaining over 88% on-target editing efficiency compared to wild-type "
    "SpCas9. Furthermore, whole-genome sequencing of treated hPSC clones confirmed "
    "long-term genomic integrity and pluripotency marker retention. These findings "
    "provide a robust methodology for high-precision therapeutic gene editing and "
    "establish a foundation for safe cellular replacement therapies."
)


# ====================================================================
# 5. State Management Helpers
# ====================================================================
def initialize_session_state():
    """Initialize necessary Streamlit session variables."""
    if "nav_page" not in st.session_state:
        st.session_state["nav_page"] = PAGE_HOME
    if "abstract_text" not in st.session_state:
        st.session_state["abstract_text"] = ""
    if "analysis_triggered" not in st.session_state:
        st.session_state["analysis_triggered"] = False
    if "submitted_abstract" not in st.session_state:
        st.session_state["submitted_abstract"] = ""


initialize_session_state()


# ====================================================================
# 6. Sidebar Navigation Component
# ====================================================================
def render_sidebar():
    """Render the modern sidebar with branding, outline navigation icons, and info."""
    with st.sidebar:
        # Compact Branding Header Box with Microscope Outline SVG
        st.markdown(
            f"""
            <div class="sidebar-brand-box">
                <div class="brand-header-row">
                    <div class="brand-icon-box">
                        {icon_svg("microscope", size=18, color="#2563EB")}
                    </div>
                    <div class="brand-text-group">
                        <div class="sidebar-brand-title">ResearchMate AI</div>
                        <div class="sidebar-brand-subtitle">Scientific Research Assistant</div>
                    </div>
                </div>
                <div class="brand-badge-row">
                    <span class="sidebar-tag">STEM2Connect Hackathon</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Clean Uppercase Section Heading
        st.markdown(
            '<div class="sidebar-section-heading">WORKSPACE</div>',
            unsafe_allow_html=True
        )

        # Navigation Menu with Outline Icons
        current_index = PAGES.index(st.session_state["nav_page"]) if st.session_state["nav_page"] in PAGES else 0

        selected_page = st.radio(
            label="WORKSPACE",
            options=PAGES,
            index=current_index,
            format_func=lambda x: PAGE_LABELS.get(x, x),
            key="sidebar_radio_selection",
            label_visibility="collapsed"
        )

        # Sync selection if user clicks radio directly
        if selected_page != st.session_state["nav_page"]:
            st.session_state["nav_page"] = selected_page
            st.rerun()

        # Sidebar Information Card
        st.markdown(
            f"""
            <div class="sidebar-info-card">
                <div class="sidebar-info-title">
                    <span class="icon-inline" style="color: #2563EB;">{icon_svg("info", size=14, color="#2563EB")}</span>
                    System Overview
                </div>
                <div style="margin-bottom: 4px;">
                    <strong>AI Engine:</strong> Gemini 1.5 (Planned)
                </div>
                <div style="margin-bottom: 4px;">
                    <strong>Mode:</strong> UI Prototype v0.2
                </div>
                <div style="margin-bottom: 4px;">
                    <strong>Theme:</strong> Light SaaS Dashboard
                </div>
                <div style="margin-top: 8px; font-size: 0.76rem; color: #64748B;">
                    Deconstructs scientific papers into 5 structured insight pillars.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ====================================================================
# 7. Hero & Welcome Component
# ====================================================================
def render_welcome_hero(compact=False):
    """
    Render the professional SaaS welcome header.
    compact: If True, renders a streamlined version for the workspace.
    """
    if compact:
        st.markdown(
            f"""
            <div class="hero-card" style="padding: 22px 24px; margin-bottom: 18px;">
                <div class="hero-badge">
                    <span class="icon-inline">{icon_svg("file-search", size=14, color="#1E40AF")}</span>
                    Paper Analysis Workspace
                </div>
                <div class="hero-heading" style="font-size: 1.65rem; margin-bottom: 6px;">
                    Understand Research. Discover Insights.
                </div>
                <div class="hero-subtitle" style="font-size: 0.95rem; margin-bottom: 0;">
                    Turn complex scientific abstracts into clear, structured research insights with ResearchMate AI.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            f"""
            <div class="hero-card">
                <div class="hero-badge">
                    <span class="icon-inline">{icon_svg("award", size=14, color="#1E40AF")}</span>
                    STEM2Connect AI Hackathon Prototype
                </div>
                <div class="hero-heading">
                    Understand Research. Discover Insights.
                </div>
                <div class="hero-subtitle">
                    Turn complex scientific abstracts into clear, structured research insights with ResearchMate AI.
                </div>
                <div class="hero-stats-row">
                    <div class="hero-stat-pill">
                        <span class="icon-inline" style="color: #2563EB;">{icon_svg("file-text", size=15, color="#2563EB")}</span>
                        Plain-English Summaries
                    </div>
                    <div class="hero-stat-pill">
                        <span class="icon-inline" style="color: #0F766E;">{icon_svg("target", size=15, color="#0F766E")}</span>
                        Research Objectives
                    </div>
                    <div class="hero-stat-pill">
                        <span class="icon-inline" style="color: #7C3AED;">{icon_svg("lightbulb", size=15, color="#7C3AED")}</span>
                        Key Findings & Metrics
                    </div>
                    <div class="hero-stat-pill">
                        <span class="icon-inline" style="color: #C2410C;">{icon_svg("tag", size=15, color="#C2410C")}</span>
                        Concept Keywords
                    </div>
                    <div class="hero-stat-pill">
                        <span class="icon-inline" style="color: #BE185D;">{icon_svg("compass", size=15, color="#BE185D")}</span>
                        Future Research Questions
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ====================================================================
# 8. View: Home Page
# ====================================================================
def render_home_page():
    """Render the Home overview page."""
    render_welcome_hero(compact=False)

    # Call to Action Banner
    col_c1, col_c2 = st.columns([3, 1])
    with col_c1:
        st.markdown(
            """
            <div style="font-size: 1.05rem; font-weight: 600; color: #1E293B; margin-top: 6px;">
                Ready to analyze a scientific paper?
            </div>
            <div style="font-size: 0.88rem; color: #64748B;">
                Paste any research paper abstract or upload a .txt file to explore our structured analysis framework.
            </div>
            """,
            unsafe_allow_html=True
        )
    with col_c2:
        if st.button("Open Workspace", key="home_cta_btn", type="primary", icon=":material/arrow_forward:", use_container_width=True):
            st.session_state["nav_page"] = PAGE_ANALYZE
            st.rerun()

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # Core Capabilities Grid
    st.markdown(
        f"""
        <div class="section-heading-with-icon">
            <span class="icon-inline" style="color: #2563EB;">{icon_svg("layers", size=20, color="#2563EB")}</span>
            Five Structured Research Dimensions
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        """
        ResearchMate AI systematically deconstructs dense academic writing into five
        accessible pillars, enabling students and researchers to accelerate their literature reviews.
        """
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div class="feature-box dim-summary">
                <div class="feature-box-icon">
                    {icon_svg("file-text", size=20, color="#2563EB")}
                </div>
                <div class="feature-box-title">1. Simple Summary</div>
                <div class="feature-box-text">
                    A plain-language synthesis explaining the study's problem, methodology, and primary takeaway without academic jargon.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div class="feature-box dim-keywords" style="margin-top: 14px;">
                <div class="feature-box-icon">
                    {icon_svg("tag", size=20, color="#C2410C")}
                </div>
                <div class="feature-box-title">4. Important Keywords</div>
                <div class="feature-box-text">
                    High-salience scientific concept tags, domain ontology, and technical terminology identified in the text.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="feature-box dim-objectives">
                <div class="feature-box-icon">
                    {icon_svg("target", size=20, color="#0F766E")}
                </div>
                <div class="feature-box-title">2. Research Objectives</div>
                <div class="feature-box-text">
                    Clear extraction of the core hypotheses, research questions, and specific aims the investigators set out to solve.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div class="feature-box dim-questions" style="margin-top: 14px;">
                <div class="feature-box-icon">
                    {icon_svg("compass", size=20, color="#BE185D")}
                </div>
                <div class="feature-box-title">5. Future Questions</div>
                <div class="feature-box-text">
                    Open research directions, study limitations, and forward-looking hypotheses sparked by the findings.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col3:
        st.markdown(
            f"""
            <div class="feature-box dim-findings">
                <div class="feature-box-icon">
                    {icon_svg("lightbulb", size=20, color="#7C3AED")}
                </div>
                <div class="feature-box-title">3. Key Findings</div>
                <div class="feature-box-text">
                    Bulleted breakdown of quantitative metrics, experimental outcomes, discoveries, and measured significance.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div class="feature-box-gemini" style="margin-top: 14px;">
                <div class="gemini-header-row">
                    <div class="gemini-icon-bubble">
                        {icon_svg("cpu", size=20, color="#6D28D9")}
                    </div>
                    <span class="gemini-phase-badge">Phase 2 Planned</span>
                </div>
                <div class="feature-box-title" style="color: #1E1B4B; margin-top: 6px;">Gemini AI Integration</div>
                <div class="feature-box-text" style="color: #4338CA;">
                    Scheduled for Phase 2: Live AI inference via Google Gemini with structured JSON schema outputs.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Workflow Steps
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="section-heading-with-icon">
            <span class="icon-inline" style="color: #2563EB;">{icon_svg("layers", size=20, color="#2563EB")}</span>
            How ResearchMate AI Works
        </div>
        """,
        unsafe_allow_html=True
    )

    step_c1, step_c2, step_c3 = st.columns(3)
    with step_c1:
        st.markdown(
            f"""
            <div class="workflow-card workflow-1">
                <span class="workflow-step-pill">Step 01</span>
                <div class="workflow-icon-bubble">
                    {icon_svg("file-text", size=22, color="#2563EB")}
                </div>
                <div class="workflow-title">01 Input Abstract</div>
                <div class="workflow-text">Paste scientific text or upload a plain text .txt file from any research paper.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with step_c2:
        st.markdown(
            f"""
            <div class="workflow-card workflow-2">
                <span class="workflow-step-pill">Step 02</span>
                <div class="workflow-icon-bubble">
                    {icon_svg("cpu", size=22, color="#7C3AED")}
                </div>
                <div class="workflow-title">02 AI Deconstruction</div>
                <div class="workflow-text">Gemini LLM pipeline analyzes methodology, claims, and conclusions.</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with step_c3:
        st.markdown(
            f"""
            <div class="workflow-card workflow-3">
                <span class="workflow-step-pill">Step 03</span>
                <div class="workflow-icon-bubble">
                    {icon_svg("layout-grid", size=22, color="#0F766E")}
                </div>
                <div class="workflow-title">03 Structured Discovery</div>
                <div class="workflow-text">Review 5 modular insight cards tailored for rapid research comprehension.</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ====================================================================
# 9. View: Paper Analysis Workspace
# ====================================================================
def render_analysis_workspace():
    """Render the primary paper analysis workspace."""
    render_welcome_hero(compact=True)

    # ----------------------------------------------------------------
    # Card: Analyze a Research Paper (Input Section)
    # ----------------------------------------------------------------
    st.markdown(
        f"""
        <div class="saas-card-header">
            <div class="saas-card-title">
                <span class="icon-inline" style="color: #2563EB;">{icon_svg("file-search", size=22, color="#2563EB")}</span>
                Analyze a Research Paper
            </div>
            <div class="saas-card-desc">
                Paste a scientific abstract below or upload an abstract text file to begin.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Optional .txt File Uploader
    uploaded_file = st.file_uploader(
        label="Upload a scientific paper abstract (.txt file)",
        type=["txt"],
        help="Select a .txt file containing the research paper abstract.",
        key="abstract_file_uploader"
    )

    uploaded_text_content = ""
    if uploaded_file is not None:
        try:
            raw_bytes = uploaded_file.getvalue()
            try:
                uploaded_text_content = raw_bytes.decode("utf-8").strip()
            except UnicodeDecodeError:
                uploaded_text_content = raw_bytes.decode("latin-1", errors="replace").strip()

            st.markdown(
                f"""
                <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 12px 14px; margin-top: 10px; margin-bottom: 12px; font-size: 0.88rem; color: #1E40AF; display: flex; align-items: center; gap: 8px;">
                    <span class="icon-inline" style="color: #2563EB;">{icon_svg("file-check", size=18, color="#2563EB")}</span>
                    <span><strong>File Uploaded:</strong> <code>{uploaded_file.name}</code> ({len(uploaded_text_content):,} characters | ~{len(uploaded_text_content.split()):,} words)</span>
                </div>
                """,
                unsafe_allow_html=True
            )

            col_file1, col_file2 = st.columns([1, 3])
            with col_file1:
                if st.button("Load File into Editor", icon=":material/file_open:", key="btn_apply_file"):
                    st.session_state["abstract_text"] = uploaded_text_content
                    st.rerun()
            with col_file2:
                st.caption("Click to transfer the uploaded file's contents into the text area below.")

        except Exception as file_error:
            st.error(f"Error reading uploaded file: {file_error}", icon=":material/error:")

    # Abstract Text Area Input
    abstract_input = st.text_area(
        label="Paste your scientific paper abstract",
        value=st.session_state.get("abstract_text", ""),
        height=220,
        placeholder=(
            "Paste your scientific paper abstract here...\n\n"
            "Example sections typically include:\n"
            "- Background & Motivation: The scientific problem being addressed\n"
            "- Methodology: Experimental design, models, or datasets utilized\n"
            "- Key Findings: Measured outcomes, statistical results, or discoveries\n"
            "- Conclusions: Broader impact and scientific significance"
        ),
        help="Paste the abstract text of the scientific paper you wish to understand."
    )

    # Keep session state updated with user's typed changes
    st.session_state["abstract_text"] = abstract_input

    # Character and Word Count Bar with SVG Icons
    char_count = len(abstract_input)
    word_count = len(abstract_input.split()) if abstract_input.strip() else 0

    st.markdown(
        f"""
        <div class="counter-bar">
            <div class="counter-item">
                <span class="icon-inline" style="color: #64748B;">{icon_svg("bar-chart-2", size=14, color="#64748B")}</span>
                Character count: <span class="counter-value">{char_count:,}</span> characters
            </div>
            <div class="counter-item">
                <span class="icon-inline" style="color: #64748B;">{icon_svg("file-text", size=14, color="#64748B")}</span>
                Word count: <span class="counter-value">{word_count:,}</span> words
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Action Buttons Row with Outline Icons
    col_btn1, col_btn2, col_btn3 = st.columns([2, 1.3, 1])

    with col_btn1:
        analyze_clicked = st.button(
            "Analyze Abstract",
            type="primary",
            icon=":material/search:",
            use_container_width=True,
            key="btn_analyze_main"
        )

    with col_btn2:
        if st.button("Load Sample Abstract", icon=":material/description:", use_container_width=True, key="btn_load_sample"):
            st.session_state["abstract_text"] = SAMPLE_ABSTRACT
            st.session_state["analysis_triggered"] = False
            st.rerun()

    with col_btn3:
        if st.button("Clear", icon=":material/delete_outline:", use_container_width=True, key="btn_clear_text"):
            st.session_state["abstract_text"] = ""
            st.session_state["analysis_triggered"] = False
            st.session_state["submitted_abstract"] = ""
            st.rerun()

    # Determine effective text for analysis
    effective_abstract = abstract_input.strip()
    if not effective_abstract and uploaded_text_content.strip():
        effective_abstract = uploaded_text_content.strip()

    # Handle Analysis Action
    if analyze_clicked:
        if effective_abstract:
            st.session_state["analysis_triggered"] = True
            st.session_state["submitted_abstract"] = effective_abstract
        else:
            st.session_state["analysis_triggered"] = False
            st.warning("Please enter an abstract or upload a .txt file before running analysis.", icon=":material/warning:")

    # ----------------------------------------------------------------
    # Results Area
    # ----------------------------------------------------------------
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    if st.session_state.get("analysis_triggered", False) and st.session_state.get("submitted_abstract", ""):
        render_results_area(st.session_state["submitted_abstract"])
    else:
        render_preview_area()


# ====================================================================
# 10. Results Area Component
# ====================================================================
def render_results_area(abstract_content: str):
    """
    Render the 5 structured results sections upon abstract submission.
    Features Lucide outline icons and structured output preview.
    """
    # Success & Status Notifications with Outline Icons
    st.success("Scientific abstract received and verified.", icon=":material/check_circle:")

    st.info(
        "AI Analysis Status: Your abstract has been processed by ResearchMate AI. "
        "Full AI-powered extraction will be generated automatically once Google Gemini API is "
        "connected in Phase 2. Below is the structured analysis framework ready for live model integration.",
        icon=":material/info:"
    )

    # Received Abstract Inspector (Preserves existing functionality)
    with st.expander("View Submitted Abstract Text", expanded=False):
        st.markdown(
            f"""
            <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; font-size: 0.92rem; line-height: 1.6; color: #1E293B;">
                {abstract_content}
            </div>
            """,
            unsafe_allow_html=True
        )
        st.caption(f"Metrics: {len(abstract_content):,} characters | ~{len(abstract_content.split()):,} words")

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="saas-card-title" style="margin-bottom: 14px;">
            <span class="icon-inline" style="color: #2563EB;">{icon_svg("bar-chart-2", size=20, color="#2563EB")}</span>
            Structured Research Insights
        </div>
        """,
        unsafe_allow_html=True
    )

    # 5 Separated Tabs with Outline Icons
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        ":material/description: Simple Summary",
        ":material/track_changes: Research Objectives",
        ":material/lightbulb: Key Findings",
        ":material/label: Important Keywords",
        ":material/explore: Future Questions"
    ])

    # Tab 1: Simple Summary
    with tab1:
        st.markdown(
            f"""
            <div class="dimension-card dim-summary">
                <div class="dimension-header">
                    <div class="dimension-title-group">
                        <div class="dimension-icon-bubble">
                            {icon_svg("book-open", size=20, color="#2563EB")}
                        </div>
                        <div>
                            <div class="dimension-name">Simple Summary</div>
                            <div class="dimension-target">Accessible Plain-Language Synthesis</div>
                        </div>
                    </div>
                    <span class="badge-placeholder">
                        <span class="icon-inline">{icon_svg("clock", size=13, color="#92400E")}</span>
                        Awaiting Gemini API Integration
                    </span>
                </div>
                <p style="color: #475569; font-size: 0.9rem; line-height: 1.55; margin-bottom: 12px;">
                    This section will synthesize the paper's core hypothesis, scientific methodology,
                    and main conclusion into a clear, jargon-free 2 to 3 sentence summary designed for students and cross-disciplinary researchers.
                </p>
                <div class="wireframe-container">
                    <strong>Planned Gemini Output Schema:</strong><br>
                    - <em>Executive Plain-Language Abstract:</em> Contextual problem statement, experimental solution, and final scientific verdict.<br>
                    - <em>Target Reading Level:</em> Undergraduate / General STEM comprehension.<br>
                    <div class="wireframe-note">[Live AI inference will replace this block upon Gemini API key configuration]</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Tab 2: Research Objectives
    with tab2:
        st.markdown(
            f"""
            <div class="dimension-card dim-objectives">
                <div class="dimension-header">
                    <div class="dimension-title-group">
                        <div class="dimension-icon-bubble">
                            {icon_svg("target", size=20, color="#0F766E")}
                        </div>
                        <div>
                            <div class="dimension-name">Research Objectives</div>
                            <div class="dimension-target">Core Hypotheses & Investigated Aims</div>
                        </div>
                    </div>
                    <span class="badge-placeholder">
                        <span class="icon-inline">{icon_svg("clock", size=13, color="#92400E")}</span>
                        Awaiting Gemini API Integration
                    </span>
                </div>
                <p style="color: #475569; font-size: 0.9rem; line-height: 1.55; margin-bottom: 12px;">
                    This section will isolate the primary research question, investigated hypotheses,
                    and specific experimental aims the authors sought to validate or disprove.
                </p>
                <div class="wireframe-container">
                    <strong>Planned Gemini Output Schema:</strong><br>
                    - <em>Primary Research Question:</em> The central problem under investigation.<br>
                    - <em>Specific Aims (Bulleted):</em> Concrete experimental targets and validation criteria.<br>
                    - <em>Methodological Scope:</em> Experimental boundaries and biological/physical systems examined.<br>
                    <div class="wireframe-note">[Live AI inference will replace this block upon Gemini API key configuration]</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Tab 3: Key Findings
    with tab3:
        st.markdown(
            f"""
            <div class="dimension-card dim-findings">
                <div class="dimension-header">
                    <div class="dimension-title-group">
                        <div class="dimension-icon-bubble">
                            {icon_svg("lightbulb", size=20, color="#7C3AED")}
                        </div>
                        <div>
                            <div class="dimension-name">Key Findings</div>
                            <div class="dimension-target">Empirical Results, Discoveries & Metrics</div>
                        </div>
                    </div>
                    <span class="badge-placeholder">
                        <span class="icon-inline">{icon_svg("clock", size=13, color="#92400E")}</span>
                        Awaiting Gemini API Integration
                    </span>
                </div>
                <p style="color: #475569; font-size: 0.9rem; line-height: 1.55; margin-bottom: 12px;">
                    This section will extract the most significant empirical discoveries, measured improvements,
                    statistical outcomes, and experimental observations reported in the abstract.
                </p>
                <div class="wireframe-container">
                    <strong>Planned Gemini Output Schema:</strong><br>
                    - <em>Primary Breakthrough:</em> Leading quantitative or qualitative breakthrough reported.<br>
                    - <em>Key Metrics & Statistics:</em> Concrete values, fold-changes, percentage improvements, or p-values.<br>
                    - <em>Comparative Baselines:</em> How the findings compare with prior state-of-the-art methods.<br>
                    <div class="wireframe-note">[Live AI inference will replace this block upon Gemini API key configuration]</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Tab 4: Important Keywords
    with tab4:
        st.markdown(
            f"""
            <div class="dimension-card dim-keywords">
                <div class="dimension-header">
                    <div class="dimension-title-group">
                        <div class="dimension-icon-bubble">
                            {icon_svg("tag", size=20, color="#C2410C")}
                        </div>
                        <div>
                            <div class="dimension-name">Important Keywords</div>
                            <div class="dimension-target">Scientific Ontology & Concept Tags</div>
                        </div>
                    </div>
                    <span class="badge-placeholder">
                        <span class="icon-inline">{icon_svg("clock", size=13, color="#92400E")}</span>
                        Awaiting Gemini API Integration
                    </span>
                </div>
                <p style="color: #475569; font-size: 0.9rem; line-height: 1.55; margin-bottom: 12px;">
                    This section will extract key scientific terminology, taxonomy tags, methodologies,
                    and domain concepts to facilitate literature indexing and cross-paper search.
                </p>
                <div class="wireframe-container">
                    <strong>Planned Gemini Output Schema:</strong><br>
                    - <em>Domain Tags:</em> 6 to 10 categorized badges spanning Methodology, Biological Entities, and Applications.<br>
                    - <em>Quick Concept Glossary:</em> One-sentence definitions for the paper's most complex technical terms.<br>
                    <div class="wireframe-note">[Live AI inference will replace this block upon Gemini API key configuration]</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # Tab 5: Future Research Questions
    with tab5:
        st.markdown(
            f"""
            <div class="dimension-card dim-questions">
                <div class="dimension-header">
                    <div class="dimension-title-group">
                        <div class="dimension-icon-bubble">
                            {icon_svg("compass", size=20, color="#BE185D")}
                        </div>
                        <div>
                            <div class="dimension-name">Future Research Questions</div>
                            <div class="dimension-target">Open Challenges, Limitations & Next Steps</div>
                        </div>
                    </div>
                    <span class="badge-placeholder">
                        <span class="icon-inline">{icon_svg("clock", size=13, color="#92400E")}</span>
                        Awaiting Gemini API Integration
                    </span>
                </div>
                <p style="color: #475569; font-size: 0.9rem; line-height: 1.55; margin-bottom: 12px;">
                    This section will highlight open questions, unaddressed limitations,
                    and promising next steps implied by the study's conclusions.
                </p>
                <div class="wireframe-container">
                    <strong>Planned Gemini Output Schema:</strong><br>
                    - <em>Immediate Next Steps:</em> Logical follow-up experiments or clinical trials needed.<br>
                    - <em>Recognized Limitations:</em> Scope constraints acknowledged in the work.<br>
                    - <em>Broader Scientific Hypotheses:</em> New research questions enabled by these findings.<br>
                    <div class="wireframe-note">[Live AI inference will replace this block upon Gemini API key configuration]</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


def render_preview_area():
    """Render a clean placeholder preview before the user initiates analysis."""
    st.markdown(
        f"""
        <div class="results-header-box">
            <div class="results-header-title">
                <span class="icon-inline" style="color: #2563EB;">{icon_svg("layout-grid", size=18, color="#2563EB")}</span>
                Structured Results Framework
            </div>
            <div class="results-header-desc">
                Paste an abstract above and click <strong>Analyze Abstract</strong> to populate these 5 scientific insight dimensions:
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            f"""
            <div class="dimension-card dim-summary">
                <div class="dimension-header">
                    <div class="dimension-title-group">
                        <div class="dimension-icon-bubble">
                            {icon_svg("file-text", size=18, color="#2563EB")}
                        </div>
                        <div>
                            <div class="dimension-name">1. Simple Summary</div>
                            <div class="dimension-target">Plain-language explanation</div>
                        </div>
                    </div>
                    <span class="badge-placeholder">
                        <span class="icon-inline">{icon_svg("circle-dot", size=12, color="#92400E")}</span>
                        Ready for Input
                    </span>
                </div>
                <div style="font-size: 0.85rem; color: #64748B;">
                    Deconstructs complex academic prose into accessible concepts for quick comprehension.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div class="dimension-card dim-objectives">
                <div class="dimension-header">
                    <div class="dimension-title-group">
                        <div class="dimension-icon-bubble">
                            {icon_svg("target", size=18, color="#0F766E")}
                        </div>
                        <div>
                            <div class="dimension-name">2. Research Objectives</div>
                            <div class="dimension-target">Hypotheses & goals</div>
                        </div>
                    </div>
                    <span class="badge-placeholder">
                        <span class="icon-inline">{icon_svg("circle-dot", size=12, color="#92400E")}</span>
                        Ready for Input
                    </span>
                </div>
                <div style="font-size: 0.85rem; color: #64748B;">
                    Extracts what questions the paper intended to investigate and solve.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div class="dimension-card dim-findings">
                <div class="dimension-header">
                    <div class="dimension-title-group">
                        <div class="dimension-icon-bubble">
                            {icon_svg("lightbulb", size=18, color="#7C3AED")}
                        </div>
                        <div>
                            <div class="dimension-name">3. Key Findings</div>
                            <div class="dimension-target">Results & outcomes</div>
                        </div>
                    </div>
                    <span class="badge-placeholder">
                        <span class="icon-inline">{icon_svg("circle-dot", size=12, color="#92400E")}</span>
                        Ready for Input
                    </span>
                </div>
                <div style="font-size: 0.85rem; color: #64748B;">
                    Highlights empirical measurements, statistical changes, and breakthrough observations.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            f"""
            <div class="dimension-card dim-keywords">
                <div class="dimension-header">
                    <div class="dimension-title-group">
                        <div class="dimension-icon-bubble">
                            {icon_svg("tag", size=18, color="#C2410C")}
                        </div>
                        <div>
                            <div class="dimension-name">4. Important Keywords</div>
                            <div class="dimension-target">Concepts & tags</div>
                        </div>
                    </div>
                    <span class="badge-placeholder">
                        <span class="icon-inline">{icon_svg("circle-dot", size=12, color="#92400E")}</span>
                        Ready for Input
                    </span>
                </div>
                <div style="font-size: 0.85rem; color: #64748B;">
                    Identifies core scientific terminology for tagging, search, and literature indexing.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            f"""
            <div class="dimension-card dim-questions">
                <div class="dimension-header">
                    <div class="dimension-title-group">
                        <div class="dimension-icon-bubble">
                            {icon_svg("compass", size=18, color="#BE185D")}
                        </div>
                        <div>
                            <div class="dimension-name">5. Future Research Questions</div>
                            <div class="dimension-target">Next steps & open problems</div>
                        </div>
                    </div>
                    <span class="badge-placeholder">
                        <span class="icon-inline">{icon_svg("circle-dot", size=12, color="#92400E")}</span>
                        Ready for Input
                    </span>
                </div>
                <div style="font-size: 0.85rem; color: #64748B;">
                    Formulates follow-up directions, study boundaries, and emerging research frontiers.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ====================================================================
# 11. View: About Page
# ====================================================================
def render_about_page():
    """Render the About project and mission section."""
    st.markdown(
        f"""
        <div class="hero-card">
            <div class="hero-badge">
                <span class="icon-inline">{icon_svg("info", size=14, color="#1E40AF")}</span>
                About ResearchMate AI
            </div>
            <div class="hero-heading" style="font-size: 1.85rem;">
                Empowering Scientific Discovery with AI
            </div>
            <div class="hero-subtitle">
                ResearchMate AI helps students and researchers understand scientific abstracts by organizing research information into clear and accessible insights.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    col_a1, col_a2 = st.columns([1.8, 1.2])

    with col_a1:
        st.markdown(
            f"""
            <div class="section-heading-with-icon">
                <span class="icon-inline" style="color: #2563EB;">{icon_svg("target", size=20, color="#2563EB")}</span>
                Mission & Background
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            **ResearchMate AI** was developed for the **STEM2Connect AI Hackathon** to bridge
            the gap between dense scientific literature and modern research learning.

            Every year, millions of scientific papers are published across arXiv, PubMed, IEEE,
            and Nature. For high school students, undergraduates, and researchers entering new
            domains, scientific papers often present formidable reading barriers:
            - **Jargon-dense vocabulary** obscures straightforward experimental concepts.
            - **Unstructured abstracts** make it difficult to locate findings and quantitative results quickly.
            - **Time constraints** slow down preliminary literature reviews and cross-disciplinary exploration.

            ResearchMate AI transforms how students and researchers approach scientific reading
            by systematically deconstructing abstracts into five clear, structured analytical dimensions.
            """
        )

        st.markdown(
            f"""
            <div class="section-heading-with-icon">
                <span class="icon-inline" style="color: #2563EB;">{icon_svg("microscope", size=20, color="#2563EB")}</span>
                Five Core Pillars
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            1. **Simple Summary:** Eliminates academic barrier-to-entry with clear language.
            2. **Research Objectives:** Identifies investigated questions and study hypotheses.
            3. **Key Findings:** Extracts empirical results, metrics, and conclusions.
            4. **Important Keywords:** Catalogs technical terms and scientific ontology.
            5. **Future Research Questions:** Bridges current results to future research directions.
            """
        )

    with col_a2:
        st.markdown(
            f"""
            <div class="section-heading-with-icon">
                <span class="icon-inline" style="color: #2563EB;">{icon_svg("layers", size=20, color="#2563EB")}</span>
                Project Architecture
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div class="saas-card" style="padding: 20px;">
                <div style="font-weight: 700; color: #0F172A; margin-bottom: 8px;">
                    Development Roadmap
                </div>
                <div style="font-size: 0.85rem; color: #475569; line-height: 1.6;">
                    <div style="margin-bottom: 8px;">
                        <span style="color: #059669; font-weight: 600;">[Phase 1 - Current]</span><br>
                        Light SaaS dashboard UI, structured input workspace, character analytics, and outline icon system.
                    </div>
                    <div style="margin-bottom: 8px;">
                        <span style="color: #2563EB; font-weight: 600;">[Phase 2 - Upcoming]</span><br>
                        Google Gemini 1.5 API integration with structured JSON schemas and streaming insight generation.
                    </div>
                    <div>
                        <span style="color: #64748B; font-weight: 600;">[Phase 3 - Planned]</span><br>
                        Multi-abstract synthesis, PDF paper upload, export to PDF/Markdown, and interactive Q&A.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="saas-card" style="padding: 20px; background: #F8FAFC;">
                <div style="font-weight: 700; color: #0F172A; margin-bottom: 8px; display: flex; align-items: center; gap: 8px;">
                    <span class="icon-inline" style="color: #2563EB;">{icon_svg("award", size=18, color="#2563EB")}</span>
                    Hackathon Information
                </div>
                <div style="font-size: 0.85rem; color: #475569; line-height: 1.6;">
                    <strong>Event:</strong> STEM2Connect AI Hackathon<br>
                    <strong>Category:</strong> AI for Scientific Research & Education<br>
                    <strong>Framework:</strong> Python + Streamlit<br>
                    <strong>Icons:</strong> Consistent Outline SVG System
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ====================================================================
# 12. Footer Component
# ====================================================================
def render_footer():
    """Render the standard SaaS footer and required disclaimer."""
    st.markdown(
        f"""
        <div class="footer-divider"></div>
        <div class="footer-content">
            <div class="footer-brand">
                <span class="icon-inline" style="color: #2563EB;">{icon_svg("microscope", size=16, color="#2563EB")}</span>
                ResearchMate AI | AI-powered Scientific Research Assistant
            </div>
            <div class="footer-disclaimer">
                <span class="icon-inline" style="color: #64748B;">{icon_svg("shield-alert", size=14, color="#64748B")}</span>
                <em>Disclaimer: AI-generated research insights should be reviewed and verified by the user.</em>
            </div>
            <div class="footer-badge">
                STEM2Connect AI Hackathon • Built with Python & Streamlit
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ====================================================================
# 13. Main Application Controller
# ====================================================================
def main():
    """Main routing function for ResearchMate AI."""
    # Render Sidebar Navigation
    render_sidebar()

    # Route based on navigation state
    current_page = st.session_state.get("nav_page", PAGE_HOME)

    if current_page == PAGE_HOME:
        render_home_page()
    elif current_page == PAGE_ANALYZE:
        render_analysis_workspace()
    elif current_page == PAGE_ABOUT:
        render_about_page()

    # Render Persistent Footer
    render_footer()


if __name__ == "__main__":
    main()
