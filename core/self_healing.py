from selenium.webdriver.common.by import By

def find_with_fallback(driver, locator):
    try:
        by, value = locator.split("=")
        return driver.find_element(getattr(By, by.upper()), value)
    except:
        return None