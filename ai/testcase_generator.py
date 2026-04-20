from google import genai
import json
import re
from config.settings import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


# -------- CLEAN JSON --------
def clean_json(text):
    match = re.search(r'\[.*\]', text, re.DOTALL)
    return match.group(0) if match else "[]"


# -------- VALIDATE STRUCTURE --------
def normalize_testcases(testcases):
    fixed = []

    for i, test in enumerate(testcases):
        fixed_test = {
            "test_name": test.get("test_name", f"Test {i+1}"),
            "type": test.get("type", "ui"),
            "steps": []
        }

        for step in test.get("steps", []):
            fixed_step = {
                "action": step.get("action", "open"),
                "value": step.get("value", ""),
            }

            if "locator" in step:
                fixed_step["locator"] = step["locator"]

            if "selector" in step:
                fixed_step["selector"] = step["selector"]

            fixed_test["steps"].append(fixed_step)

        fixed.append(fixed_test)

    return fixed


# -------- MAIN GENERATOR --------
def generate_testcases(user_story):
    prompt = f"""
    Generate Selenium test cases in STRICT JSON.

    RULES:
    - Output ONLY JSON array
    - Each test must have:
      - test_name
      - type (ui or api)
      - steps

    UI step format:
    {{
      "action": "open/type/click/assert_title",
      "locator": "id=..." OR "selector": "css",
      "value": "text or url"
    }}

    IMPORTANT:
    - Always include locator or selector for type & click
    - Use real websites (NOT placeholders)
    - Keep steps simple

    Example:
    [
      {{
        "test_name": "Login Test",
        "type": "ui",
        "steps": [
          {{"action": "open", "value": "https://www.saucedemo.com"}},
          {{"action": "type", "locator": "id=user-name", "value": "standard_user"}},
          {{"action": "click", "locator": "id=login-button"}}
        ]
      }}
    ]

    User Story:
    {user_story}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    text = response.text.strip()

    try:
        parsed = json.loads(text)
    except:
        parsed = json.loads(clean_json(text))

    return normalize_testcases(parsed)