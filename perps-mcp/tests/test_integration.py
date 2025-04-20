import os
import pytest
import httpx
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()


@pytest.fixture(scope="session")
def api_key():
    # Try to get from env, else use fallback
    return os.getenv("RANGER_API_KEY", "sk_test_LAjG9vTZRk10x6ECHbW8MWFxLK1ZuxCbzLl4ERqwkL4=")


@pytest.fixture(scope="session")
def base_url():
    # Adjust this to your actual server URL/port
    return "http://localhost:8000"


def test_ranger_status_action(api_key, base_url):
    headers = {"Authorization": f"Bearer {api_key}"}
    # Assuming FastMCP exposes tools at /tool/{tool_name}
    resp = httpx.post(f"{base_url}/tool/ranger_status",
                      headers=headers, json={})
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "OK"
    assert "sor_base_url" in data
    assert "data_base_url" in data
    assert "fastmcp_version" in data
