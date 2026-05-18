import requests
import uuid

BASE_URL = "http://localhost:8000"
TIMEOUT = 30
TEST_EMAIL = "test@example.com"


def authenticate_get_session_token(email):
    # Start auth
    url_start = f"{BASE_URL}/v1/auth/start"
    resp_start = requests.post(url_start, json={"email": email}, timeout=TIMEOUT)
    assert resp_start.status_code == 202

    # Get test token
    url_test_token = f"{BASE_URL}/v1/auth/test-token"
    resp_test_token = requests.post(url_test_token, json={"email": email}, timeout=TIMEOUT)
    assert resp_test_token.status_code == 200
    token = resp_test_token.json().get("token")
    assert token

    # Verify token to get session_token
    url_verify = f"{BASE_URL}/v1/auth/verify"
    resp_verify = requests.post(url_verify, json={"token": token}, timeout=TIMEOUT)
    assert resp_verify.status_code == 200
    json_verify = resp_verify.json()
    session_token = json_verify.get("session_token")
    assert session_token

    return session_token


def create_subscription(session_token, service_name="test-service-deletev1subscriptions"):
    url = f"{BASE_URL}/v1/subscriptions"
    headers = {"Authorization": f"Bearer {session_token}"}
    data = {"service_name": service_name}
    resp = requests.post(url, json=data, headers=headers, timeout=TIMEOUT)
    assert resp.status_code == 201
    subscription = resp.json()
    subscription_id = subscription.get("id") or subscription.get("subscription_id") or subscription.get("subscriptionId")
    assert subscription_id
    return subscription_id


def delete_subscription(session_token, subscription_id):
    url = f"{BASE_URL}/v1/subscriptions/{subscription_id}"
    headers = {"Authorization": f"Bearer {session_token}"}
    resp = requests.delete(url, headers=headers, timeout=TIMEOUT)
    return resp


def get_subscriptions(session_token):
    url = f"{BASE_URL}/v1/subscriptions"
    headers = {"Authorization": f"Bearer {session_token}"}
    resp = requests.get(url, headers=headers, timeout=TIMEOUT)
    return resp


def test_delete_v1_subscriptions_deletesubscription():
    # Authenticate user and get session token
    session_token = authenticate_get_session_token(TEST_EMAIL)
    headers = {"Authorization": f"Bearer {session_token}"}

    subscription_id = None
    try:
        # Create a new subscription to delete
        subscription_id = create_subscription(session_token)

        # DELETE the subscription
        resp_delete = delete_subscription(session_token, subscription_id)
        assert resp_delete.status_code == 204

        # Verify subscription is not in active list anymore
        resp_list = get_subscriptions(session_token)
        assert resp_list.status_code == 200
        subs = resp_list.json().get("subscriptions", [])
        # Subscription should not be present
        assert all(sub.get("id", sub.get("subscription_id", sub.get("subscriptionId"))) != subscription_id for sub in subs)

    finally:
        # Cleanup: attempt to delete subscription again if exists
        if subscription_id is not None:
            # Delete might 404 if already deleted; ignore errors here
            delete_subscription(session_token, subscription_id)


test_delete_v1_subscriptions_deletesubscription()