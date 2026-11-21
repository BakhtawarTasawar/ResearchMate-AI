"""
ResearchGate AI – Frontend Application
======================================
Streamlit institutional research application.

Start with:
    cd frontend
    streamlit run app.py
"""
from __future__ import annotations

import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Path bootstrap – allows importing sibling packages (config, services, etc.)
# ---------------------------------------------------------------------------
_HERE = Path(__file__).parent.resolve()
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import streamlit as st

from config.settings import (
    APP_TITLE,
    FAVICON_PATH,
    PAGE_ANALYZE,
    PAGE_HOME,
    PAGE_ABOUT,
    PAGE_AUTH,
)
from utils import session
from components.ui import render_navbar, render_footer
from services.api_client import APIError, get_api_client
import pages.home as home_page
import pages.analyze as analyze_page
import pages.about as about_page
import pages.auth as auth_page

# ---------------------------------------------------------------------------
# Page config – MUST be the first Streamlit call
# ---------------------------------------------------------------------------
_favicon = str(FAVICON_PATH) if FAVICON_PATH.exists() else "🔬"
st.set_page_config(
    page_title=f"{APP_TITLE} – Scientific Research Assistant",
    page_icon=_favicon,
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# CSS injection
# ---------------------------------------------------------------------------
_css_path = _HERE / "styles" / "styles.css"
if _css_path.exists():
    css = _css_path.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state initialisation
# ---------------------------------------------------------------------------
session.init()

# ---------------------------------------------------------------------------
# Backend health check (once per session)
# ---------------------------------------------------------------------------
if session.get_backend_status() is None:
    try:
        client = get_api_client()
        health = client.health_check()
        session.set_backend_status("ok", "Connected")
    except Exception:
        session.set_backend_status("error", "Offline")

# ---------------------------------------------------------------------------
# Top navbar (replaces sidebar navigation)
# ---------------------------------------------------------------------------
current_page = session.get_nav_page()
render_navbar(current_page=current_page)

# ---------------------------------------------------------------------------
# Page routing
# ---------------------------------------------------------------------------
page = session.get_nav_page()

if page == PAGE_HOME:
    home_page.render()
elif page == PAGE_ANALYZE:
    analyze_page.render()
elif page == PAGE_ABOUT:
    about_page.render()
elif page == PAGE_AUTH:
    auth_page.render()
else:
    home_page.render()

# ---------------------------------------------------------------------------
# Persistent footer
# ---------------------------------------------------------------------------
render_footer()
