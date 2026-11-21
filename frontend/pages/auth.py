"""
Authentication page — Institutional Login, Registration, and Researcher Profile.
"""
from __future__ import annotations

import re
import html
import streamlit as st

from config.settings import PAGE_ANALYZE, PAGE_HOME
from services.api_client import APIError, get_api_client, sanitize_error
from utils import session
from utils.icons import svg


_EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def render() -> None:
    """Render the authentication workspace (Login, Signup, or Profile)."""
    if session.is_authenticated():
        _render_profile()
    else:
        auth_mode = session.get_auth_page()
        if auth_mode == "signup":
            _render_signup()
        else:
            _render_login()


def _render_login() -> None:
    st.markdown(
        f"""
        <div class="auth-container">
            <div class="auth-header">
                <div class="auth-badge">
                    {svg("shield", 13, "#1D4ED8")}
                    Institutional Access
                </div>
                <div class="auth-title">Sign In to ResearchGate AI</div>
                <div class="auth-subtitle">
                    Enter your research credentials to access your workspace and saved analyses.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_l, col_form, col_r = st.columns([1, 1.4, 1])

    with col_form:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)

        email = st.text_input(
            "Institutional Email Address",
            placeholder="researcher@university.edu",
            key="login_email_input",
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="••••••••",
            key="login_password_input",
        )

        col_btn, col_switch = st.columns([1, 1])
        with col_btn:
            submit_login = st.button(
                "Sign In",
                type="primary",
                use_container_width=True,
                key="btn_submit_login",
            )
        with col_switch:
            if st.button(
                "Create Account",
                type="secondary",
                use_container_width=True,
                key="btn_switch_to_signup",
            ):
                session.set_auth_page("signup")
                st.rerun()

        if submit_login:
            if not email.strip():
                st.error("Please enter your email address.")
            elif not _EMAIL_REGEX.match(email.strip()):
                st.error("Please enter a valid email address.")
            elif not password:
                st.error("Please enter your password.")
            else:
                try:
                    client = get_api_client()
                    result = client.login(email.strip().lower(), password)
                    token = result.get("access_token")
                    user = result.get("user", {})
                    if token and user:
                        session.set_auth(token, user)
                        session.set_nav_page(PAGE_ANALYZE)
                        st.rerun()
                    else:
                        st.error("Invalid email or password.")
                except Exception as exc:
                    st.error(sanitize_error(exc, action="login"))

        st.markdown('</div>', unsafe_allow_html=True)


def _render_signup() -> None:
    st.markdown(
        f"""
        <div class="auth-container">
            <div class="auth-header">
                <div class="auth-badge">
                    {svg("user", 13, "#1D4ED8")}
                    New Account
                </div>
                <div class="auth-title">Create Researcher Account</div>
                <div class="auth-subtitle">
                    Register for institutional access to explore scientific abstracts with ResearchGate AI.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_l, col_form, col_r = st.columns([1, 1.4, 1])

    with col_form:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)

        full_name = st.text_input(
            "Full Name",
            placeholder="Dr. Eleanor Vance",
            key="signup_name_input",
        )
        email = st.text_input(
            "Email Address",
            placeholder="e.vance@institution.edu",
            key="signup_email_input",
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Minimum 8 characters",
            key="signup_password_input",
        )
        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter password",
            key="signup_confirm_password_input",
        )

        col_btn, col_switch = st.columns([1, 1])
        with col_btn:
            submit_signup = st.button(
                "Create Account",
                type="primary",
                use_container_width=True,
                key="btn_submit_signup",
            )
        with col_switch:
            if st.button(
                "Existing User? Sign In",
                type="secondary",
                use_container_width=True,
                key="btn_switch_to_login",
            ):
                session.set_auth_page("login")
                st.rerun()

        if submit_signup:
            if not full_name.strip() or len(full_name.strip()) < 2:
                st.error("Please enter your full name (at least 2 characters).")
            elif not email.strip() or not _EMAIL_REGEX.match(email.strip()):
                st.error("Please enter a valid email address.")
            elif not password or len(password) < 8:
                st.error("Password must be at least 8 characters in length.")
            elif password != confirm_password:
                st.error("Passwords do not match.")
            else:
                try:
                    client = get_api_client()
                    client.register(
                        full_name=full_name.strip(),
                        email=email.strip().lower(),
                        password=password,
                    )
                    # Automatically log in after registration
                    login_res = client.login(email.strip().lower(), password)
                    token = login_res.get("access_token")
                    user = login_res.get("user", {})
                    if token and user:
                        session.set_auth(token, user)
                        session.set_nav_page(PAGE_ANALYZE)
                        st.rerun()
                    else:
                        session.set_auth_page("login")
                        st.success("Account created successfully. Please sign in.")
                        st.rerun()
                except Exception as exc:
                    st.error(sanitize_error(exc, action="register"))

        st.markdown('</div>', unsafe_allow_html=True)


def _render_profile() -> None:
    user = session.get_auth_user() or {}
    name = user.get("full_name", "Researcher")
    email = user.get("email", "")

    st.markdown(
        f"""
        <div class="auth-container">
            <div class="auth-header">
                <div class="auth-badge">
                    {svg("user-check", 13, "#059669")}
                    Researcher Session
                </div>
                <div class="auth-title">Researcher Profile</div>
                <div class="auth-subtitle">
                    Active authenticated session for ResearchGate AI workspace.
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_l, col_center, col_r = st.columns([1, 1.4, 1])

    with col_center:
        initial = name[:1].upper() if name else "R"
        st.markdown(
            f"""
            <div class="auth-card">
                <div style="display:flex;align-items:center;gap:14px;margin-bottom:18px;padding-bottom:16px;border-bottom:1px solid #E2E8F0;">
                    <div style="width:48px;height:48px;border-radius:50%;background:#0F172A;color:#FFFFFF;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:1.1rem;">
                        {html.escape(initial)}
                    </div>
                    <div>
                        <div style="font-weight:700;font-size:1.05rem;color:#0F172A;">{html.escape(name)}</div>
                        <div style="font-size:0.85rem;color:#64748B;">{html.escape(email)}</div>
                    </div>
                </div>
                <div style="margin-bottom:20px;font-size:0.85rem;color:#475569;line-height:1.6;">
                    <div style="display:flex;justify-content:space-between;padding:10px 0;border-bottom:1px solid #F1F5F9;">
                        <span style="color:#64748B;">Account Status</span>
                        <span style="color:#059669;font-weight:600;">Active · Institutional</span>
                    </div>
                    <div style="display:flex;justify-content:space-between;padding:10px 0;">
                        <span style="color:#64748B;">Access Tier</span>
                        <span style="color:#0F172A;font-weight:500;">Research Associate</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
        col_ws, col_lo = st.columns([1.3, 1])
        with col_ws:
            if st.button("Open Research Workspace", type="primary", use_container_width=True, key="profile_btn_workspace"):
                session.set_nav_page(PAGE_ANALYZE)
                st.rerun()
        with col_lo:
            if st.button("Sign Out", type="secondary", use_container_width=True, key="profile_btn_signout"):
                session.logout()
                session.set_nav_page(PAGE_HOME)
                st.rerun()
