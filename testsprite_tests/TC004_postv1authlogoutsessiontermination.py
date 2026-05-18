import requests
import time

BASE_URL = "http://localhost:8000"
TEST_EMAIL = "testuser@example.com"
TIMEOUT = 30

def test_post_v1_auth_logout_session_termination():
    session = requests.Session()
    # Step 1: POST /v1/auth/start with test email
    start_url = f"{BASE_URL}/v1/auth/start"
    start_payload = {"email": TEST_EMAIL}
    start_resp = session.post(start_url, json=start_payload, timeout=TIMEOUT)
    assert start_resp.status_code == 202, f"Unexpected status code on auth start: {start_resp.status_code}"

    # Step 2: POST /v1/auth/test-token with same email to retrieve issued single-use token (local test-only)
    test_token_url = f"{BASE_URL}/v1/auth/test-token"
    token_payload = {"email": TEST_EMAIL}
    token_resp = session.post(test_token_url, json=token_payload, timeout=TIMEOUT)
    assert token_resp.status_code == 200, f"Unexpected status code on test-token: {token_resp.status_code}"
    token_data = token_resp.json()
    assert "token" in token_data, "No token in test-token response"
    magic_token = token_data["token"]

    # Step 3: POST /v1/auth/verify with that token
    verify_url = f"{BASE_URL}/v1/auth/verify"
    verify_payload = {"token": magic_token}
    verify_resp = session.post(verify_url, json=verify_payload, timeout=TIMEOUT)
    assert verify_resp.status_code == 200, f"Unexpected status code on auth verify: {verify_resp.status_code}"
    verify_data = verify_resp.json()
    assert "session_token" in verify_data, "No session_token in auth verify response"
    assert "user" in verify_data and "email" in verify_data["user"], "User info missing or incomplete in auth verify response"
    assert verify_data["user"]["email"].lower() == TEST_EMAIL.lower(), "User email mismatch"
    session_token = verify_data["session_token"]

    headers = {"Authorization": f"Bearer {session_token}"}

    # Step 4: POST /v1/auth/logout with active session token
    logout_url = f"{BASE_URL}/v1/auth/logout"
    logout_resp = session.post(logout_url, headers=headers, timeout=TIMEOUT)
    assert logout_resp.status_code == 204, f"Unexpected status code on logout: {logout_resp.status_code}"
    assert logout_resp.text == "", "Logout response body should be empty"

    # Step 5: Confirm session is ended by making an authenticated request that requires session token (e.g., GET /v1/subscriptions)
    subscriptions_url = f"{BASE_URL}/v1/subscriptions"
    subs_resp = session.get(subscriptions_url, headers=headers, timeout=TIMEOUT)
    # Expect 401 unauthorized indicating the session ended successfully
    assert subs_resp.status_code == 401, f"Expected 401 after logout but got {subs_resp.status_code}"

test_post_v1_auth_logout_session_termination()