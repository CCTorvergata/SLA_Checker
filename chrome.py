from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Imposta Chrome in modalità headless
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

def start_chrome():
    # Inizializza il driver Chrome
    driver = webdriver.Chrome(options=options)
    return driver

def stop_chrome(driver):
    # Chiude il driver Chrome
    driver.quit()
    return