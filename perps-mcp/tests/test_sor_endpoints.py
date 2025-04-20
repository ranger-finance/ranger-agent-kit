import os
import pytest
import httpx
from dotenv import load_dotenv

load_dotenv()

@pytest.fixture(scope="session")
def api_key():
    return os.getenv("RANGER_API_KEY", "sk_test_L9vTZRk10x6ECHbW8MWFxLK1ZuxCbzLl4ERqwkL4=")

@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:8000"

@pytest.fixture(scope="session")
def fee_payer():
    return "2vZfQDVS1H7tF9M3cTrSoMQkEpwqPRGH4g1kTgbRHodr"

# --- Test SOR Endpoints ---

def test_get_trade_quote(api_key, base_url, fee_payer):
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "params": {
            "fee_payer": fee_payer,
            "symbol": "SOL",
            "side": "Long",
            "size": 0.1,
            "collateral": 10,
            "size_denomination": "SOL",
            "adjustment_type": "Increase",
            "target_venues": ["Jupiter"],
            "slippage_bps": 100
        }
    }
    resp = httpx.post(f"{base_url}/tool/get_trade_quote", headers=headers, json=payload)
    print("get_trade_quote response:", resp.text)
    assert resp.status_code == 200
    data = resp.json()
    assert "average_price" in data or "price" in data

def test_increase_position(api_key, base_url, fee_payer):
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "params": {
            "fee_payer": fee_payer,
            "symbol": "SOL",
            "side": "Long",
            "size": 0.1,
            "collateral": 10,
            "size_denomination": "SOL",
            "adjustment_type": "Increase",
            "target_venues": ["Jupiter"],
            "slippage_bps": 100
        }
    }
    resp = httpx.post(f"{base_url}/tool/increase_position", headers=headers, json=payload)
    print("increase_position response:", resp.text)
    assert resp.status_code == 200
    data = resp.json()
    assert "message" in data

def test_decrease_position(api_key, base_url, fee_payer):
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "params": {
            "fee_payer": fee_payer,
            "symbol": "SOL",
            "side": "Long",
            "size": 0.1,
            "collateral": 0,
            "size_denomination": "SOL",
            "adjustment_type": "DecreaseJupiter",
            "target_venues": ["Jupiter"],
            "slippage_bps": 100
        }
    }
    resp = httpx.post(f"{base_url}/tool/decrease_position", headers=headers, json=payload)
    print("decrease_position response:", resp.text)
    assert resp.status_code == 200
    data = resp.json()
    assert "message" in data

def test_close_position(api_key, base_url, fee_payer):
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "params": {
            "fee_payer": fee_payer,
            "symbol": "SOL",
            "side": "Long",
            "adjustment_type": "CloseJupiter",
            "slippage_bps": 100
        }
    }
    resp = httpx.post(f"{base_url}/tool/close_position", headers=headers, json=payload)
    print("close_position response:", resp.text)
    assert resp.status_code == 200
    data = resp.json()
    assert "message" in data

def test_withdraw_balance_drift(api_key, base_url, fee_payer):
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "params": {
            "fee_payer": fee_payer,
            "symbol": "USDC",
            "amount": 1.0,
            "sub_account_id": 0
        }
    }
    resp = httpx.post(f"{base_url}/tool/withdraw_balance_drift", headers=headers, json=payload)
    print("withdraw_balance_drift response:", resp.text)
    assert resp.status_code == 200
    data = resp.json()
    assert "message" in data 