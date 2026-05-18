import requests
import uuid

BASE_URL = "http://localhost:8000"
TEST_EMAIL = "testuser@example.com"
TIMEOUT = 30

def get_session_token(email: str) -> str:
    # Start auth
    start_resp = requests.post(
        f"{BASE_URL}/v1/auth/start",
        json={"email": email},
        timeout=TIMEOUT,
    )
    assert start_resp.status_code == 202, f"Auth start failed: {start_resp.text}"

    # Get test token
    test_token_resp = requests.post(
        f"{BASE_URL}/v1/auth/test-token",
        json={"email": email},
        timeout=TIMEOUT,
    )
    assert test_token_resp.status_code == 200, f"Test token retrieval failed: {test_token_resp.text}"
    token = test_token_resp.json().get("token")
    assert token, "Test token missing in response"

    # Verify token to get session token
    verify_resp = requests.post(
        f"{BASE_URL}/v1/auth/verify",
        json={"token": token},
        timeout=TIMEOUT,
    )
    assert verify_resp.status_code == 200, f"Auth verify failed: {verify_resp.text}"
    session_token = verify_resp.json().get("session_token")
    assert session_token, "Session token missing in auth verify response"
    return session_token

def create_subscription(session_token: str, service_name: str) -> dict:
    headers = {"Authorization": f"Bearer {session_token}"}
    payload = {"service_name": service_name}
    resp = requests.post(
        f"{BASE_URL}/v1/subscriptions",
        json=payload,
        headers=headers,
        timeout=TIMEOUT,
    )
    assert resp.status_code == 201, f"Subscription creation failed: {resp.text}"
    return resp.json()

def delete_subscription(session_token: str, subscription_id: str) -> None:
    headers = {"Authorization": f"Bearer {session_token}"}
    resp = requests.delete(
        f"{BASE_URL}/v1/subscriptions/{subscription_id}",
        headers=headers,
        timeout=TIMEOUT,
    )
    assert resp.status_code == 204, f"Subscription deletion failed: {resp.text}"

def patchv1subscriptionsupdatesubscription():
    session_token = get_session_token(TEST_EMAIL)
    headers = {"Authorization": f"Bearer {session_token}"}
    subscription = None
    try:
        # Create a subscription to update
        unique_service_name = f"TestService-{uuid.uuid4()}"
        subscription = create_subscription(session_token, unique_service_name)
        subscription_id = subscription.get("id")
        assert subscription_id, "Created subscription missing id"

        # Prepare patch payload with updated fields
        patch_payload = {
            "service_name": f"{unique_service_name}-Updated",
            "notes": "Updated subscription notes"
        }

        patch_resp = requests.patch(
            f"{BASE_URL}/v1/subscriptions/{subscription_id}",
            json=patch_payload,
            headers=headers,
            timeout=TIMEOUT,
        )
        assert patch_resp.status_code == 200, f"Patch failed: {patch_resp.text}"
        patched_data = patch_resp.json()
        # Validate updated fields are reflected
        assert patched_data.get("service_name") == patch_payload["service_name"], "Service name not updated"
        assert patched_data.get("notes") == patch_payload["notes"], "Notes not updated"
        # Validate id is same
        assert patched_data.get("id") == subscription_id, "Subscription ID mismatch after patch"
    finally:
        if subscription and "id" in subscription:
            delete_subscription(session_token, subscription["id"])

patchv1subscriptionsupdatesubscription()