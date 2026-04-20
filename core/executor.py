from core.ui_executor import execute_ui_test
from core.api_executor import execute_api_test

def execute_test(test_case, base_url=""):
    test_type = test_case.get("type", "ui")

    if test_type == "api":
        execute_api_test(test_case, base_url)
    else:
        execute_ui_test(test_case, base_url)