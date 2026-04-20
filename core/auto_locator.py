from selenium.webdriver.common.by import By

def find_element_smart(driver, keyword):
    keyword = keyword.lower()

    strategies = [
        f"//*[contains(@id,'{keyword}')]",
        f"//*[contains(@name,'{keyword}')]",
        f"//*[contains(@placeholder,'{keyword}')]",
        f"//input[contains(@type,'search')]",
        f"//button[contains(text(),'{keyword}')]",
        f"//*[contains(text(),'{keyword}')]"
    ]

    for xpath in strategies:
        elements = driver.find_elements(By.XPATH, xpath)
        if elements:
            return elements[0]

    raise Exception(f"Element not found: {keyword}")