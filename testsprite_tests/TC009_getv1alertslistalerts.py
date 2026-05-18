import requests

BASE_URL = "http://localhost:8000"
TEST_EMAIL = "testuser@example.com"
TIMEOUT = 30

def get_session_token(email: str) -> str:
    # Step 1: POST /v1/auth/start
    start_resp = requests.post(
        f"{BASE_URL}/v1/auth/start",
        json={"email": email},
        timeout=TIMEOUT
    )
    assert start_resp.status_code == 202, f"Auth start failed: {start_resp.text}"

    # The /v1/auth/test-token endpoint does not exist per PRD, so token retrieval depends on out-of-band
    # For testing purposes, raise assertion that token retrieval is not implemented
    assert False, "Token retrieval step not implemented - cannot proceed without magic link token"

    # The following code is removed since the test-token endpoint does not exist
    # test_token_resp = requests.post(
    #     f"{BASE_URL}/v1/auth/test-token",
    #     json={"email": email},
    #     timeout=TIMEOUT
    # )
    # assert test_token_resp.status_code == 200, f"Test token retrieval failed: {test_token_resp.text}"
    # single_use_token = test_token_resp.json().get("token")
    # assert single_use_token, "No token received from test-token endpoint"

    # Step 3: POST /v1/auth/verify with the single-use token
    # verify_resp = requests.post(
    #     f"{BASE_URL}/v1/auth/verify",
    #     json={"token": single_use_token},
    #     timeout=TIMEOUT
    # )
    # assert verify_resp.status_code == 200, f"Auth verify failed: {verify_resp.text}"
    # session_token = verify_resp.json().get("session_token")
    # assert session_token, "No session_token received on verify"
    # return session_token

def test_get_v1_alerts_list_alerts():
    session_token = get_session_token(TEST_EMAIL)
    headers = {
        "Authorization": f"Bearer {session_token}"
    }

    # Call GET /v1/alerts with valid session token
    alerts_resp = requests.get(
        f"{BASE_URL}/v1/alerts",
        headers=headers,
        timeout=TIMEOUT
    )

    # Assert status code is 200
    assert alerts_resp.status_code == 200, f"Expected 200 OK, got {alerts_resp.status_code}: {alerts_resp.text}"

    # Validate response content structure
    json_data = alerts_resp.json()
    assert isinstance(json_data, dict), f"Response JSON is not a dict: {json_data}"
    assert "alerts" in json_data, "'alerts' field missing in response"
    assert isinstance(json_data["alerts"], list), "'alerts' should be a list"

    # Optionally validate each alert object if present (not required but good check)
    for alert in json_data["alerts"]:
        assert isinstance(alert, dict), "Alert item is not an object"

# Note: This test will fail intentionally at token retrieval step until token retrieval is implemented

test_get_v1_alerts_list_alerts()
