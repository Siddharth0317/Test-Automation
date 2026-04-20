import os
from datetime import datetime

def capture_screenshot(driver, name):
    if not os.path.exists("reports"):
        os.makedirs("reports")

    file = f"reports/{name}_{datetime.now().timestamp()}.png"
    driver.save_screenshot(file)
    return file