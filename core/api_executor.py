import requests
from core.auth_manager import save_token, get_token

def execute_api_test(test_case, base_url=""):
    print(f"\nRunning API Test: {test_case['test_name']}")

    response = None

    for step in test_case["steps"]:
        action = step["action"]

        # ---------- REQUEST ----------
        if action == "request":
            url = step["url"]

            if not url.startswith("http"):
                url = base_url + url

            headers = {}

            # attach auth token if needed
            if step.get("auth"):
                token = get_token(step["auth"])
                headers["Authorization"] = f"Bearer {token}"

            method = step["method"]

            if method == "GET":
                response = requests.get(url, headers=headers)

            elif method == "POST":
                response = requests.post(
                    url,
                    json=step.get("body", {}),
                    headers=headers
                )

            elif method == "PUT":
                response = requests.put(
                    url,
                    json=step.get("body", {}),
                    headers=headers
                )

            elif method == "DELETE":
                response = requests.delete(url, headers=headers)

        # ---------- ASSERT STATUS ----------
        elif action == "assert_status":
            assert response.status_code == step["value"]

        # ---------- SAVE TOKEN ----------
        elif action == "save_token":
            data = response.json()
            token = data.get(step["key"])
            save_token(step["name"], token)

    print("✅ API Test Passed")