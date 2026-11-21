"""
Root config module for frontend.
Re-exports settings for top-level imports.
"""
from config.settings import (
    BACKEND_API_URL,
    APP_TITLE,
    APP_SUBTITLE,
    APP_VERSION,
    PAGE_HOME,
    PAGE_ANALYZE,
    PAGE_ABOUT,
    PAGES,
    ASSETS_DIR,
    STYLES_DIR,
    FAVICON_PATH,
    SAMPLE_ABSTRACT,
)

__all__ = [
    "BACKEND_API_URL",
    "APP_TITLE",
    "APP_SUBTITLE",
    "APP_VERSION",
    "PAGE_HOME",
    "PAGE_ANALYZE",
    "PAGE_ABOUT",
    "PAGES",
    "ASSETS_DIR",
    "STYLES_DIR",
    "FAVICON_PATH",
    "SAMPLE_ABSTRACT",
]
