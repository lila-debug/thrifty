import requests

BASE_URL = "http://localhost:8000"
TIMEOUT = 30

def test_gethealthapiavailability():
    url = f"{BASE_URL}/health"
    try:
        response = requests.get(url, timeout=TIMEOUT)
    except requests.RequestException as e:
        assert False, f"Request to /health failed: {e}"

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    # Validate required fields exist and are strings
    for field in ["status", "db", "version"]:
        assert field in data, f"Missing '{field}' field in response"
        assert isinstance(data[field], str), f"Field '{field}' should be string"

test_gethealthapiavailability()