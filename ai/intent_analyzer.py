def analyze_intent(text):
    text = text.lower()

    return {
        "login": "login" in text,
        "register": "register" in text,
        "crud": "create" in text or "update" in text,
        "validation": "invalid" in text or "error" in text
    }