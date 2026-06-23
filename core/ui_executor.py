from core.driver import get_driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# -------- NORMALIZE ACTION --------
def normalize_action(action):
    mapping = {
        "open": "open",
        "open_url": "open",
        "type": "type",
        "enter_text": "type",
        "click": "click",
        "click_element": "click",
        "assert_title": "assert_title"
    }
    return mapping.get(action, action)


# -------- FIND ELEMENT WITH WAIT --------
def find_element(driver, step, timeout=10):
    wait = WebDriverWait(driver, timeout)

    # locator (id=username)
    if "locator" in step:
        by, value = step["locator"].split("=")
        return wait.until(
            EC.presence_of_element_located((getattr(By, by.upper()), value))
        )

    # selector (CSS)
    if "selector" in step:
        return wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, step["selector"]))
        )

    # fallback (text)
    if "value" in step:
        keyword = step["value"]
        return wait.until(
            EC.presence_of_element_located(
                (By.XPATH, f"//*[contains(text(),'{keyword}')]")
            )
        )

    raise Exception("Element not found")


# -------- MAIN EXECUTOR --------
def execute_ui_test(test_case, base_url=""):
    driver = get_driver()
    wait = WebDriverWait(driver, 10)

    print(f"\n🚀 Running: {test_case.get('test_name','Test')}")

    try:
        for step in test_case.get("steps", []):
            print("👉 STEP:", step)

            action = normalize_action(step.get("action"))

            # ---------- OPEN ----------
            if action == "open":
                url = step.get("value", "")

                if base_url:
                    if url.startswith("http"):
                        url = base_url
                    else:
                        url = base_url + url

                driver.get(url)

                # wait page load
                wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

            # ---------- TYPE ----------
            elif action == "type":
                element = find_element(driver, step)

                driver.execute_script("arguments[0].scrollIntoView();", element)

                element.clear()
                element.send_keys(step.get("value", ""))

            # ---------- CLICK ----------
            elif action == "click":
                element = find_element(driver, step)

                driver.execute_script("arguments[0].scrollIntoView();", element)

                wait.until(EC.element_to_be_clickable(element))
                element.click()

            # ---------- ASSERT ----------
            elif action == "assert_title":
                expected = step.get("value", "")
                wait.until(lambda d: expected in d.title)

            # ---------- WAIT ----------
            elif action == "wait":
                time.sleep(step.get("value", 2))

            else:
                print(f"⚠️ Unknown action: {action}")

        print("✅ Test Passed")

    except Exception as e:
        print("❌ Test Failed:", str(e))
        raise e

    finally:
        driver.quit()