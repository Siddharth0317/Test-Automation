from core.driver import get_driver
from selenium.webdriver.common.by import By
import time


# -------- HELPER: NORMALIZE ACTION --------
def normalize_action(action):
    mapping = {
        "open": "open",
        "open_url": "open",

        "type": "type",
        "enter_text": "type",
        "input": "type",

        "click": "click",
        "click_element": "click",

        "assert_title": "assert_title",
        "assert_url_contains": "assert_title"
    }
    return mapping.get(action, action)


# -------- HELPER: FIND ELEMENT --------
def find_element(driver, step):
    # 1. locator (id=username)
    if "locator" in step:
        try:
            by, value = step["locator"].split("=")
            return driver.find_element(getattr(By, by.upper()), value)
        except:
            pass

    # 2. selector (CSS)
    if "selector" in step:
        return driver.find_element(By.CSS_SELECTOR, step["selector"])

    # 3. fallback using text
    if "value" in step:
        keyword = step["value"]
        try:
            return driver.find_element(By.XPATH, f"//*[contains(text(),'{keyword}')]")
        except:
            pass

    raise Exception("Element not found")


# -------- MAIN EXECUTOR --------
def execute_ui_test(test_case, base_url=""):
    driver = get_driver()

    print(f"\n🚀 Running UI Test: {test_case.get('test_name', 'Unnamed Test')}")

    try:
        for step in test_case.get("steps", []):
            print("👉 STEP:", step)

            action = normalize_action(step.get("action"))

            # ---------- OPEN ----------
            if action == "open":
                url = step.get("value", "")

                if not url:
                    raise Exception("Missing URL")

                if not url.startswith("http"):
                    url = base_url + url

                driver.get(url)
                time.sleep(2)

            # ---------- TYPE ----------
            elif action == "type":
                element = find_element(driver, step)

                text = step.get("value", "")
                element.clear()
                element.send_keys(text)

                time.sleep(1)

            # ---------- CLICK ----------
            elif action == "click":
                element = find_element(driver, step)
                element.click()
                time.sleep(2)

            # ---------- ASSERT ----------
            elif action == "assert_title":
                expected = step.get("value", "")
                if expected not in driver.title:
                    raise Exception(f"Assertion failed: {driver.title}")

            # ---------- WAIT ----------
            elif action == "wait":
                time.sleep(step.get("value", 2))

            else:
                print(f"⚠️ Unknown action skipped: {action}")

        print("✅ UI Test Passed")

    except Exception as e:
        print("❌ UI Test Failed:", str(e))
        raise e

    finally:
        driver.quit()