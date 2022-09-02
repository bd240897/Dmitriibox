from selenium import webdriver
from selenium.webdriver.chrome.service import Service


service = Service("chromedriver\\chromedriver.exe")
driver = webdriver.Chrome(service=service)

url = "https://stackoverflow.com/questions/47264281/then-is-not-a-function"

try:
    driver.get(url)
except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()