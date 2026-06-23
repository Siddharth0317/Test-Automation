import time
import json
import re
from google import genai
from config.settings import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)

# -------- CACHE --------
cache = {}

# -------- RATE LIMIT CONTROL --------
LAST_CALL = 0

def wait_if_needed():
    global LAST_CALL
    now = time.time()

    if now - LAST_CALL < 10:
        time.sleep(10)

    LAST_CALL = time.time()


# -------- CLEAN JSON --------
def clean_json(text):
    match = re.search(r'\[.*\]', text, re.DOTALL)
    return match.group(0) if match else "[]"


# -------- OFFLINE GENERATOR --------
def offline_generator(user_story):
    story = user_story.lower()

    # LOGIN
    if "login" in story:
        return [
            {
                "test_name": "Login Test",
                "type": "ui",
                "steps": [
                    {"action": "open", "value": "/"},
                    {"action": "type", "selector": "input[name='username']", "value": "user"},
                    {"action": "type", "selector": "input[name='password']", "value": "pass"},
                    {"action": "click", "selector": "button[type='submit']"}
                ]
            }
        ]

    # SEARCH
    if "search" in story:
        return [
            {
                "test_name": "Search Test",
                "type": "ui",
                "steps": [
                    {"action": "open", "value": "/"},
                    {"action": "type", "selector": "input[type='text']", "value": "product"},
                    {"action": "click", "selector": "button[type='submit']"}
                ]
            }
        ]

    # DEFAULT
    return [
        {
            "test_name": "Basic Test",
            "type": "ui",
            "steps": [
                {"action": "open", "value": "/"}
            ]
        }
    ]


# -------- GEMINI CALL --------
def call_gemini(prompt, model):
    return client.models.generate_content(
        model=model,
        contents=prompt
    )


# -------- MAIN FUNCTION --------
def generate_testcases(user_story):

    # -------- CACHE CHECK --------
    if user_story in cache:
        print("✅ Using cached result")
        return cache[user_story]

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

    models = [
        "gemini-2.5-flash"
    ]

    # -------- GEMINI WITH RETRY --------
    for model in models:
        for attempt in range(2):
            try:
                wait_if_needed()

                print(f"Trying {model}, attempt {attempt+1}")

                response = call_gemini(prompt, model)

                text = response.text.strip()

                try:
                    result = json.loads(text)
                except:
                    result = json.loads(clean_json(text))

                cache[user_story] = result
                return result

            except Exception as e:
                print("⚠️ Retry:", e)
                time.sleep(2)

    # -------- FALLBACK --------
    print("⚠️ Using offline generator")

    result = offline_generator(user_story)
    cache[user_story] = result
    return result