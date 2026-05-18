import requests
import time

BASE_URL = "http://localhost:8000"
EMAIL = "testuser@example.com"
TIMEOUT = 30

def test_post_v1_subscriptions_create_subscription():
    session = requests.Session()

    try:
        # Check health endpoint first
        health_resp = session.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        assert health_resp.status_code == 200
        health_json = health_resp.json()
        assert "status" in health_json and "db" in health_json and "version" in health_json

        # Step 1: POST /v1/auth/start with test email
        auth_start_resp = session.post(
            f"{BASE_URL}/v1/auth/start",
            json={"email": EMAIL},
            timeout=TIMEOUT
        )
        assert auth_start_resp.status_code == 202

        # Step 2: POST /v1/auth/test-token with the same email to retrieve the issued single-use token
        # This endpoint isn't documented in the PRD but described in instructions; implement request:
        test_token_resp = session.post(
            f"{BASE_URL}/v1/auth/test-token",
            json={"email": EMAIL},
            timeout=TIMEOUT
        )
        assert test_token_resp.status_code == 200
        token_data = test_token_resp.json()
        assert "token" in token_data
        magic_link_token = token_data["token"]

        # Step 3: POST /v1/auth/verify with that token
        auth_verify_resp = session.post(
            f"{BASE_URL}/v1/auth/verify",
            json={"token": magic_link_token},
            timeout=TIMEOUT
        )
        assert auth_verify_resp.status_code == 200
        verify_json = auth_verify_resp.json()
        assert "session_token" in verify_json
        session_token = verify_json["session_token"]

        # Prepare headers with Bearer session_token
        headers = {
            "Authorization": f"Bearer {session_token}",
            "Content-Type": "application/json"
        }

        # Step 4: POST /v1/subscriptions with required fields to create a subscription
        subscription_payload = {
            "service_name": f"Test Service {int(time.time())}"
        }

        create_sub_resp = session.post(
            f"{BASE_URL}/v1/subscriptions",
            json=subscription_payload,
            headers=headers,
            timeout=TIMEOUT
        )
        assert create_sub_resp.status_code == 201
        created_sub = create_sub_resp.json()

        # Validate returned subscription response contains at least the service_name and an id
        assert "service_name" in created_sub and created_sub["service_name"] == subscription_payload["service_name"]
        assert "id" in created_sub and isinstance(created_sub["id"], str) and created_sub["id"].strip() != ""

    finally:
        # Cleanup: delete the created subscription if it exists
        if 'created_sub' in locals() and "id" in created_sub:
            subscription_id = created_sub["id"]
            try:
                del_resp = session.delete(
                    f"{BASE_URL}/v1/subscriptions/{subscription_id}",
                    headers={"Authorization": f"Bearer {session_token}"},
                    timeout=TIMEOUT
                )
                # deletion might be 204 or 404 if already deleted, accept both as cleanup success
                assert del_resp.status_code in (204, 404)
            except Exception:
                pass

test_post_v1_subscriptions_create_subscription()