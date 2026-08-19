"""Product Intelligence — Streamlit Frontend.

Landing page and system dashboard for the AI-powered product intelligence platform.
Polls the backend health and readiness endpoints to display a real connection indicator.
"""

import os
from datetime import UTC, datetime

import requests
import streamlit as st

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
API_PREFIX = "/api/v1"


def check_backend_health(base_url: str) -> dict | None:
    """Call the backend liveness endpoint. Returns the JSON body or None on failure."""
    try:
        resp = requests.get(f"{base_url}{API_PREFIX}/health", timeout=3)
        if resp.status_code == 200:
            return resp.json()
    except requests.RequestException:
        pass
    return None


def check_backend_readiness(base_url: str) -> dict | None:
    """Call the backend readiness endpoint. Returns the JSON body or None on failure."""
    try:
        resp = requests.get(f"{base_url}{API_PREFIX}/ready", timeout=3)
        if resp.status_code == 200:
            return resp.json()
    except requests.RequestException:
        pass
    return None


def render_connection_indicator(health: dict | None, ready: dict | None) -> None:
    """Render the backend connection status indicator."""
    if health is None:
        st.error("Backend: **unavailable** — cannot reach the API server.")
        st.caption(f"Attempted URL: `{BACKEND_URL}{API_PREFIX}/health`")
        return

    liveness = health.get("status", "unknown")
    readiness = ready.get("status", "unknown") if ready else "unavailable"

    if liveness == "ok" and readiness == "ready":
        st.success("Backend: **connected and ready**")
    elif liveness == "ok":
        st.warning("Backend: **connected but not ready** (database unavailable)")
    else:
        st.error(f"Backend: **unhealthy** (status: {liveness})")

    with st.expander("Backend details", expanded=False):
        st.json({
            "liveness": health,
            "readiness": ready,
        })


def render_sidebar() -> str:
    """Render sidebar navigation. Returns the selected page."""
    st.sidebar.title("Product Intelligence")
    st.sidebar.caption("AI-Powered Industrial Commerce")

    page = st.sidebar.radio(
        "Navigate",
        ["Dashboard", "System Status"],
        label_visibility="collapsed",
    )

    st.sidebar.divider()
    st.sidebar.markdown(
        f"**API:** `{BACKEND_URL}`  \n"
        f"**Time (UTC):** {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')}"
    )

    return page


def render_dashboard(health: dict | None, ready: dict | None) -> None:
    """Render the main dashboard page."""
    st.title("Product Intelligence Dashboard")
    st.markdown(
        "AI-powered system for creating, enriching, and validating "
        "industrial product information from fragmented sources."
    )

    render_connection_indicator(health, ready)

    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Products", "—", help="Will show product count when ingestion is implemented.")
    with col2:
        st.metric("Attributes", "—", help="Will show extracted attribute count.")
    with col3:
        st.metric("Conflicts", "—", help="Will show unresolved conflict count.")

    st.info(
        "This is the Module 4 foundation. Product ingestion, extraction, "
        "validation, and enrichment capabilities will be added in subsequent modules."
    )


def render_system_status(health: dict | None, ready: dict | None) -> None:
    """Render the system status page."""
    st.title("System Status")

    render_connection_indicator(health, ready)

    st.divider()

    st.subheader("Services")

    services = {
        "Backend API": {
            "status": "online" if health and health.get("status") == "ok" else "offline",
            "version": health.get("version", "unknown") if health else "unknown",
            "url": f"{BACKEND_URL}{API_PREFIX}",
        },
        "Database": {
            "status": "online" if ready and ready.get("database") == "ok" else "offline",
        },
    }

    for name, info in services.items():
        status_color = "green" if info["status"] == "online" else "red"
        st.markdown(f"**{name}** — :{status_color}[{info['status']}]")
        if "version" in info:
            st.caption(f"Version: {info['version']}")
        if "url" in info:
            st.caption(f"URL: `{info['url']}`")


def main() -> None:
    st.set_page_config(
        page_title="Product Intelligence",
        page_icon="🏭",
        layout="wide",
    )

    health = check_backend_health(BACKEND_URL)
    ready = check_backend_readiness(BACKEND_URL)

    page = render_sidebar()

    if page == "Dashboard":
        render_dashboard(health, ready)
    elif page == "System Status":
        render_system_status(health, ready)


if __name__ == "__main__":
    main()
