import requests

BASE_URL = "http://localhost:8000"

TEST_EMAIL = "test+tc010@thrifty.app"

def get_session_token(email: str) -> str:
    try:
        # Start auth flow
        resp_start = requests.post(
            f"{BASE_URL}/v1/auth/start",
            json={"email": email},
            timeout=30,
        )
        assert resp_start.status_code == 202, f"Auth start failed: {resp_start.status_code} {resp_start.text}"

        # Retrieve test token for the email
        resp_test_token = requests.post(
            f"{BASE_URL}/v1/auth/test-token",
            json={"email": email},
            timeout=30,
        )
        assert resp_test_token.status_code == 200, f"Fetch test token failed: {resp_test_token.status_code} {resp_test_token.text}"
        test_token = resp_test_token.json().get("token")
        assert test_token, "Test token missing in response"

        # Verify token to get session token
        resp_verify = requests.post(
            f"{BASE_URL}/v1/auth/verify",
            json={"token": test_token},
            timeout=30,
        )
        assert resp_verify.status_code == 200, f"Auth verify failed: {resp_verify.status_code} {resp_verify.text}"
        session_token = resp_verify.json().get("session_token")
        assert session_token, "Session token missing in verify response"

        return session_token
    except AssertionError:
        raise
    except Exception as e:
        raise RuntimeError(f"Authentication flow failed: {e}") from e


def test_post_v1_notifications_register_token():
    session_token = get_session_token(TEST_EMAIL)
    headers = {
        "Authorization": f"Bearer {session_token}",
        "Content-Type": "application/json",
    }

    payload = {
        "platform": "ios",
        "token": "sample_device_push_token_1234567890abcdef"
    }

    try:
        resp = requests.post(
            f"{BASE_URL}/v1/notifications/token",
            json=payload,
            headers=headers,
            timeout=30,
        )
        assert resp.status_code == 201, f"Expected 201 Created, got {resp.status_code}: {resp.text}"

        data = resp.json()
        assert "id" in data and isinstance(data["id"], str) and data["id"].strip() != "", "Response missing valid id"
        assert data.get("platform") == payload["platform"], f"Platform mismatch, expected {payload['platform']}, got {data.get('platform')}"
        assert data.get("active") is True, "Expected 'active' to be True"

    finally:
        # Cleanup: delete the registered notification token if created
        if 'data' in locals() and "id" in data:
            try:
                del_resp = requests.delete(
                    f"{BASE_URL}/v1/notifications/token/{data['id']}",
                    headers=headers,
                    timeout=30,
                )
                # Allow 204 or 404 if already deleted
                assert del_resp.status_code in (204, 404), f"Delete token failed: {del_resp.status_code} {del_resp.text}"
            except Exception as cleanup_err:
                # Log cleanup error but do not fail test here
                print(f"Cleanup failed deleting notification token {data['id']}: {cleanup_err}")


test_post_v1_notifications_register_token()