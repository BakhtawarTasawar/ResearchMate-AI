
"""
Session state management — application and authentication state.
"""
from __future__ import annotations

from typing import Any
import streamlit as st

from config.settings import PAGE_HOME

_NAV_PAGE = "nav_page"
_ABSTRACT_TEXT = "abstract_text"
_ANALYSIS_TRIGGERED = "analysis_triggered"
_SUBMITTED_ABSTRACT = "submitted_abstract"
_ANALYSIS_RESULT = "analysis_result"
_ANALYSIS_ERROR = "analysis_error"
_BACKEND_STATUS = "backend_status"
_BACKEND_MODEL = "backend_model"
_EXTRACTED_FILE_INFO = "extracted_file_info"
_VIEW_MODE = "view_mode"

# Authentication
_AUTH_TOKEN = "auth_token"
_AUTH_USER = "auth_user"
_AUTH_PAGE = "auth_page"


def init() -> None:
    defaults: dict[str, Any] = {
        _NAV_PAGE: PAGE_HOME,
        _ABSTRACT_TEXT: "",
        _ANALYSIS_TRIGGERED: False,
        _SUBMITTED_ABSTRACT: "",
        _ANALYSIS_RESULT: None,
        _ANALYSIS_ERROR: None,
        _BACKEND_STATUS: None,
        _BACKEND_MODEL: "—",
        _EXTRACTED_FILE_INFO: None,
        _VIEW_MODE: "tabs",
        _AUTH_TOKEN: None,
        _AUTH_USER: None,
        _AUTH_PAGE: "login",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def get_nav_page() -> str:
    return st.session_state.get(_NAV_PAGE, PAGE_HOME)


def set_nav_page(page: str) -> None:
    st.session_state[_NAV_PAGE] = page


def get_abstract_text() -> str:
    return st.session_state.get(_ABSTRACT_TEXT, "")


def set_abstract_text(text: str) -> None:
    st.session_state[_ABSTRACT_TEXT] = text


def get_analysis_result() -> dict | None:
    return st.session_state.get(_ANALYSIS_RESULT)


def set_analysis_result(result: dict | None) -> None:
    st.session_state[_ANALYSIS_RESULT] = result


def get_analysis_error() -> str | None:
    return st.session_state.get(_ANALYSIS_ERROR)


def set_analysis_error(error: str | None) -> None:
    st.session_state[_ANALYSIS_ERROR] = error


def is_analysis_triggered() -> bool:
    return st.session_state.get(_ANALYSIS_TRIGGERED, False)


def set_analysis_triggered(value: bool) -> None:
    st.session_state[_ANALYSIS_TRIGGERED] = value


def get_submitted_abstract() -> str:
    return st.session_state.get(_SUBMITTED_ABSTRACT, "")


def set_submitted_abstract(text: str) -> None:
    st.session_state[_SUBMITTED_ABSTRACT] = text


def get_extracted_file_info() -> dict | None:
    return st.session_state.get(_EXTRACTED_FILE_INFO)


def set_extracted_file_info(info: dict | None) -> None:
    st.session_state[_EXTRACTED_FILE_INFO] = info


def clear_extracted_file_info() -> None:
    st.session_state[_EXTRACTED_FILE_INFO] = None


def get_view_mode() -> str:
    return st.session_state.get(_VIEW_MODE, "tabs")


def set_view_mode(mode: str) -> None:
    st.session_state[_VIEW_MODE] = mode


def clear_analysis() -> None:
    st.session_state[_ANALYSIS_TRIGGERED] = False
    st.session_state[_SUBMITTED_ABSTRACT] = ""
    st.session_state[_ANALYSIS_RESULT] = None
    st.session_state[_ANALYSIS_ERROR] = None


def get_backend_status() -> str | None:
    return st.session_state.get(_BACKEND_STATUS)


def set_backend_status(status: str | None, model: str = "—") -> None:
    st.session_state[_BACKEND_STATUS] = status
    st.session_state[_BACKEND_MODEL] = model


def get_backend_model() -> str:
    return st.session_state.get(_BACKEND_MODEL, "—")


# Authentication accessors

def set_auth(token: str, user: dict) -> None:
    st.session_state[_AUTH_TOKEN] = token
    st.session_state[_AUTH_USER] = user


def get_auth_token() -> str | None:
    return st.session_state.get(_AUTH_TOKEN)


def get_auth_user() -> dict | None:
    return st.session_state.get(_AUTH_USER)


def is_authenticated() -> bool:
    return bool(get_auth_token())


def logout() -> None:
    st.session_state[_AUTH_TOKEN] = None
    st.session_state[_AUTH_USER] = None
    st.session_state[_AUTH_PAGE] = "login"
    if "_api_client" in st.session_state and st.session_state["_api_client"] is not None:
        st.session_state["_api_client"].set_token(None)
    clear_analysis()


def get_auth_page() -> str:
    return st.session_state.get(_AUTH_PAGE, "login")


def set_auth_page(page: str) -> None:
    st.session_state[_AUTH_PAGE] = page
