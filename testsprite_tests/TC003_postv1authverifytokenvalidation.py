import requests

BASE_URL = "http://localhost:8000"

def test_post_v1_auth_verify_token_validation():
    email = "testuser@example.com"
    timeout = 30

    # Step 1: Start auth to issue magic link
    start_resp = requests.post(
        f"{BASE_URL}/v1/auth/start",
        json={"email": email},
        timeout=timeout
    )
    assert start_resp.status_code == 202, f"Expected 202 on auth start but got {start_resp.status_code}"

    # Step 2: Obtain test token for the email from /v1/auth/test-token
    test_token_resp = requests.post(
        f"{BASE_URL}/v1/auth/test-token",
        json={"email": email},
        timeout=timeout
    )
    assert test_token_resp.status_code == 200, f"Expected 200 getting test token but got {test_token_resp.status_code}"
    test_token_data = test_token_resp.json()
    token = test_token_data.get("token")
    assert isinstance(token, str) and token, "Token must be a non-empty string"

    # Step 3: Verify token to get session token and user profile
    verify_resp = requests.post(
        f"{BASE_URL}/v1/auth/verify",
        json={"token": token},
        timeout=timeout
    )
    assert verify_resp.status_code == 200, f"Expected 200 on auth verify but got {verify_resp.status_code}"

    verify_data = verify_resp.json()
    session_token = verify_data.get("session_token")
    user = verify_data.get("user")

    assert isinstance(session_token, str) and session_token, "Session token must be a non-empty string"
    assert isinstance(user, dict), "User profile must be a dictionary"
    assert "id" in user and isinstance(user["id"], str) and user["id"], "User id must be a non-empty string"
    assert "email" in user and user["email"] == email, "User email should match the authenticated email"
    assert "tier" in user and isinstance(user["tier"], str), "User tier must be a string"

test_post_v1_auth_verify_token_validation()