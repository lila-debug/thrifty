import requests

BASE_URL = "http://localhost:8000"
TEST_EMAIL = "testuser@example.com"
TIMEOUT = 30


def test_post_v1_auth_start_magic_link_issuance():
    # Step 1: Health check to confirm backend is up
    health_resp = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
    assert health_resp.status_code == 200
    health_data = health_resp.json()
    assert "status" in health_data and isinstance(health_data["status"], str)
    assert "db" in health_data and isinstance(health_data["db"], str)
    assert "version" in health_data and isinstance(health_data["version"], str)

    # Step 2: POST /v1/auth/start with valid email
    start_url = f"{BASE_URL}/v1/auth/start"
    start_payload = {"email": TEST_EMAIL}
    start_resp = requests.post(start_url, json=start_payload, timeout=TIMEOUT)
    assert start_resp.status_code == 202
    start_data = start_resp.json()
    assert "status" in start_data and isinstance(start_data["status"], str)

    # Step 3: POST /v1/auth/test-token to retrieve issued token (test harness only)
    test_token_url = f"{BASE_URL}/v1/auth/test-token"
    test_token_resp = requests.post(test_token_url, json={"email": TEST_EMAIL}, timeout=TIMEOUT)
    assert test_token_resp.status_code == 200
    test_token_data = test_token_resp.json()
    assert "token" in test_token_data and isinstance(test_token_data["token"], str)
    magic_token = test_token_data["token"]

    # Step 4: POST /v1/auth/verify with that token
    verify_url = f"{BASE_URL}/v1/auth/verify"
    verify_resp = requests.post(verify_url, json={"token": magic_token}, timeout=TIMEOUT)
    assert verify_resp.status_code == 200
    verify_data = verify_resp.json()
    assert "session_token" in verify_data and isinstance(verify_data["session_token"], str)
    assert "user" in verify_data and isinstance(verify_data["user"], dict)
    user = verify_data["user"]
    assert "id" in user and isinstance(user["id"], str)
    assert "email" in user and user["email"] == TEST_EMAIL
    assert "tier" in user and isinstance(user["tier"], str)


test_post_v1_auth_start_magic_link_issuance()