"""
Analyze Paper workspace — document upload, text editor, live AI inference, and structured results.
All internal technical endpoints and connection errors are sanitized before presentation.
"""
from __future__ import annotations

import html
import streamlit as st

from components.ui import render_preview, render_results
from config.settings import SAMPLE_ABSTRACT
from services.api_client import APIError, get_api_client, sanitize_error
from utils import session
from utils.icons import svg


def _format_size(size_bytes: int) -> str:
    """Format bytes into a human-readable size string."""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.2f} MB"


def render() -> None:
    # ---- Workspace Page Header ----
    st.markdown(
        f"""
        <div class="institutional-hero" style="padding: 24px 28px; margin-bottom: 20px;">
            <div class="institutional-badge">
                {svg("file-search", size=13, color="#1D4ED8")}
                Analysis Workspace
            </div>
            <h1 class="institutional-hero-title" style="font-size: 1.65rem; margin-bottom: 6px;">
                Research Paper Analysis Workspace
            </h1>
            <p class="institutional-hero-desc" style="font-size: 0.92rem;">
                Submit a scientific abstract below or upload a research publication (.pdf or .txt) to generate a structured five-dimension synthesis.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Section 1: Document Upload Area ----
    uploaded_file = st.file_uploader(
        "Upload a research publication (.pdf or .txt)",
        type=["pdf", "txt"],
        help="Upload a research publication PDF or plain text file (maximum 10 MB).",
        key="file_uploader",
    )

    # Check if a new file was uploaded or file changed
    if uploaded_file is not None:
        cached_info = session.get_extracted_file_info()
        file_key = f"{uploaded_file.name}_{uploaded_file.size}"

        # If not cached or different file, extract via backend
        if not cached_info or cached_info.get("key") != file_key:
            with st.spinner("Processing uploaded research document..."):
                try:
                    client = get_api_client(token=session.get_auth_token())
                    raw_bytes = uploaded_file.getvalue()
                    content_type = uploaded_file.type or "application/octet-stream"

                    data = client.extract_text(
                        filename=uploaded_file.name,
                        file_bytes=raw_bytes,
                        content_type=content_type,
                    )

                    new_info = {
                        "key": file_key,
                        "filename": uploaded_file.name,
                        "file_type": uploaded_file.name.rsplit(".", 1)[-1].upper(),
                        "size_str": _format_size(uploaded_file.size),
                        "text": data.get("text", ""),
                        "char_count": data.get("char_count", 0),
                        "word_count": data.get("word_count", 0),
                    }
                    session.set_extracted_file_info(new_info)

                except Exception as e:
                    session.clear_extracted_file_info()
                    st.error("Unable to extract text from the document. Please verify the file contains selectable text and try again.")

    elif session.get_extracted_file_info() is not None:
        # User removed file from uploader
        session.clear_extracted_file_info()

    # Render Extracted File Info Box if file is currently loaded
    current_file_info = session.get_extracted_file_info()
    analyze_direct_clicked = False

    if current_file_info:
        fname = html.escape(current_file_info["filename"])
        ftype = html.escape(current_file_info["file_type"])
        fsize = current_file_info["size_str"]
        c_count = current_file_info["char_count"]
        w_count = current_file_info["word_count"]

        st.markdown(
            f"""
            <div class="institutional-card" style="margin-bottom:14px;padding:14px 18px;background:#F8FAFC;">
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px;">
                    <div style="font-weight:700;font-size:0.92rem;color:#0F172A;display:flex;align-items:center;gap:8px;">
                        {svg("file-check", 16, "#059669")}
                        <span>{fname}</span>
                    </div>
                    <span class="inst-tag inst-tag--verified">{ftype}</span>
                </div>
                <div style="display:flex;gap:18px;font-size:0.8rem;color:#64748B;">
                    <span>Size: <strong>{fsize}</strong></span>
                    <span>Characters: <strong>{c_count:,}</strong></span>
                    <span>Words: <strong>{w_count:,}</strong></span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_f1, col_f2 = st.columns([1.2, 1.4], gap="small")
        with col_f1:
            if st.button("Load into Text Editor", use_container_width=True, key="btn_apply_extracted"):
                session.set_abstract_text(current_file_info["text"])
                st.rerun()

        with col_f2:
            analyze_direct_clicked = st.button(
                "Analyse Uploaded Document Directly",
                type="primary",
                use_container_width=True,
                key="btn_analyze_direct",
            )

    st.markdown("<div style='height:8px;'></div>", unsafe_allow_html=True)

    # ---- Section 2: Abstract Text Editor ----
    abstract_input = st.text_area(
        label="Scientific Paper Abstract / Document Text",
        value=session.get_abstract_text(),
        height=220,
        placeholder=(
            "Paste your scientific paper abstract here...\n\n"
            "Typical structure includes:\n"
            "• Background & Objectives: The problem being addressed\n"
            "• Methods: Experimental or theoretical approach\n"
            "• Key Findings: Measured outcomes, statistics, and observations\n"
            "• Conclusions & Impact: Broader scientific significance"
        ),
        help="Paste the abstract text of the scientific research paper you want to analyze.",
        key="abstract_textarea",
    )
    session.set_abstract_text(abstract_input)

    # Character and Word Count Bar
    char_count = len(abstract_input)
    word_count = len(abstract_input.split()) if abstract_input.strip() else 0

    st.markdown(
        f"""
        <div class="counter-bar">
            <div class="counter-item">
                Characters: <span class="counter-value">{char_count:,}</span>
            </div>
            <div class="counter-item">
                Words: <span class="counter-value">{word_count:,}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Action Buttons Row ----
    col_btn1, col_btn2, col_btn3 = st.columns([2.0, 1.4, 1.0], gap="small")

    with col_btn1:
        analyze_editor_clicked = st.button(
            "Analyse Abstract",
            type="primary",
            use_container_width=True,
            key="btn_analyze_main",
        )

    with col_btn2:
        if st.button("Load Sample Abstract", use_container_width=True, key="btn_load_sample"):
            session.set_abstract_text(SAMPLE_ABSTRACT)
            session.clear_analysis()
            st.rerun()

    with col_btn3:
        if st.button("Clear Input", use_container_width=True, key="btn_clear_all"):
            session.set_abstract_text("")
            session.clear_analysis()
            st.rerun()

    # ---- Determine effective text for analysis ----
    effective_text = ""
    if analyze_direct_clicked and current_file_info:
        effective_text = current_file_info["text"].strip()
    elif analyze_editor_clicked:
        effective_text = abstract_input.strip()
        if not effective_text and current_file_info:
            effective_text = current_file_info["text"].strip()

    # ---- Trigger Analysis Pipeline ----
    if analyze_editor_clicked or analyze_direct_clicked:
        if not effective_text:
            st.warning("Please enter an abstract or upload a research document before running analysis.")
        elif len(effective_text) < 50:
            st.warning("Input text is too short. Please provide at least 50 characters of scientific text.")
        else:
            # Check if text changed since last submission
            if effective_text != session.get_submitted_abstract():
                session.set_analysis_result(None)
                session.set_analysis_error(None)

            session.set_analysis_triggered(True)
            session.set_submitted_abstract(effective_text)

            # Perform call if not already cached
            if session.get_analysis_result() is None and session.get_analysis_error() is None:
                with st.status("Analyzing research document...", expanded=True) as status_box:
                    st.write("Extracting methodology, experimental claims, and data points...")
                    try:
                        client = get_api_client(token=session.get_auth_token())
                        st.write("Synthesizing structured research dimensions...")
                        response = client.analyze_text(effective_text)
                        session.set_analysis_result(response.get("result"))
                        session.set_analysis_error(None)
                        status_box.update(label="Analysis complete! Structured insights generated.", state="complete", expanded=False)
                    except Exception as exc:
                        safe_msg = sanitize_error(exc, action="analyze")
                        session.set_analysis_result(None)
                        session.set_analysis_error(safe_msg)
                        status_box.update(label="Unable to complete analysis.", state="error", expanded=False)

    # ---- Results Area ----
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)

    if session.is_analysis_triggered() and session.get_submitted_abstract():
        render_results(
            results=session.get_analysis_result(),
            error=session.get_analysis_error(),
            submitted=session.get_submitted_abstract(),
        )
    else:
        render_preview()
