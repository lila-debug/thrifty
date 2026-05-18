import requests
import time


BASE_URL = "http://localhost:8000"
AUTH_START_PATH = "/v1/auth/start"
AUTH_TEST_TOKEN_PATH = "/v1/auth/test-token"
AUTH_VERIFY_PATH = "/v1/auth/verify"
SUBSCRIPTIONS_PATH = "/v1/subscriptions"


def get_test_token(email: str) -> str:
    # Step 1: Start auth to trigger token issuance
    start_resp = requests.post(
        BASE_URL + AUTH_START_PATH,
        json={"email": email},
        timeout=30,
    )
    assert start_resp.status_code == 202, f"Auth start failed: {start_resp.text}"

    # Step 2: Use local test-only endpoint to get the issued token
    test_token_resp = requests.post(
        BASE_URL + AUTH_TEST_TOKEN_PATH,
        json={"email": email},
        timeout=30,
    )
    assert test_token_resp.status_code == 200, f"Test token retrieval failed: {test_token_resp.text}"
    token_json = test_token_resp.json()
    token = token_json.get("token")
    assert isinstance(token, str) and token, "Invalid test token received"
    return token


def verify_token_return_session(email: str, token: str) -> str:
    # Step 3: Verify token to get session token
    verify_resp = requests.post(
        BASE_URL + AUTH_VERIFY_PATH,
        json={"token": token},
        timeout=30,
    )
    assert verify_resp.status_code == 200, f"Auth verify failed: {verify_resp.text}"
    verify_json = verify_resp.json()
    session_token = verify_json.get("session_token")
    assert isinstance(session_token, str) and session_token, "No session_token in verify response"
    return session_token


def create_subscription(session_token: str) -> str:
    # Create a manual subscription to ensure user has at least one subscription for listing
    headers = {"Authorization": f"Bearer {session_token}"}
    payload = {
        "service_name": "Test Service TC006",
    }
    create_resp = requests.post(
        BASE_URL + SUBSCRIPTIONS_PATH,
        json=payload,
        headers=headers,
        timeout=30,
    )
    assert create_resp.status_code == 201, f"Subscription creation failed: {create_resp.text}"
    created_json = create_resp.json()
    subscription_id = created_json.get("id") or created_json.get("subscription_id")
    assert subscription_id, "No subscription ID returned on creation"
    return subscription_id


def delete_subscription(session_token: str, subscription_id: str) -> None:
    headers = {"Authorization": f"Bearer {session_token}"}
    delete_resp = requests.delete(
        f"{BASE_URL}{SUBSCRIPTIONS_PATH}/{subscription_id}",
        headers=headers,
        timeout=30,
    )
    assert delete_resp.status_code == 204 or delete_resp.status_code == 404, f"Subscription deletion failed: {delete_resp.text}"


def test_get_v1_subscriptions_list_subscriptions():
    email = "testuser@example.com"

    # Authenticate user and get session token
    token = get_test_token(email)
    session_token = verify_token_return_session(email, token)

    headers = {"Authorization": f"Bearer {session_token}"}

    subscription_id = None
    try:
        # Create a subscription to ensure the list is not empty
        subscription_id = create_subscription(session_token)

        # Step: Call GET /v1/subscriptions with valid session token
        list_resp = requests.get(
            BASE_URL + SUBSCRIPTIONS_PATH,
            headers=headers,
            timeout=30,
        )
        assert list_resp.status_code == 200, f"Subscriptions list failed: {list_resp.text}"
        list_json = list_resp.json()
        assert "subscriptions" in list_json, "Response missing 'subscriptions' key"
        assert isinstance(list_json["subscriptions"], list), "'subscriptions' is not a list"

        # Assert that the created subscription is in the list
        found = any(
            (sub.get("id") == subscription_id or sub.get("subscription_id") == subscription_id)
            for sub in list_json["subscriptions"]
        )
        assert found, "Created subscription not found in subscriptions list"

    finally:
        # Cleanup: delete created subscription
        if subscription_id:
            delete_subscription(session_token, subscription_id)


test_get_v1_subscriptions_list_subscriptions()