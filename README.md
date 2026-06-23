# 🤖 AI Test Automation Framework

An AI-powered testing tool that:
- Generates test cases from user stories
- Executes UI tests using Selenium
- Supports API testing
- Generates PDF reports
- Maintains test history

## 🚀 Features
- AI-based test generation (Gemini)
- UI automation (Selenium)
- API testing
- PDF reporting
- Streamlit dashboard

## 🛠️ Installation

```bash
pip install -r requirements.txt


python -m streamlit run dashboard.py

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