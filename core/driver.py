from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from config.settings import HEADLESS

def get_driver():
    options = webdriver.ChromeOptions()

    if HEADLESS:
        options.add_argument("--headless")

    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    return driver