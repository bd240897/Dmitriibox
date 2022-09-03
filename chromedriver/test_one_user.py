from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import pickle
from selenium.webdriver.common.by import By

# options
options = webdriver.ChromeOptions()

# user-agent
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")

# for ChromeDriver version 79.0.3945.16 or over
options.add_argument("--disable-blink-features=AutomationControlled")

# headless mode
# options.add_argument("--headless")
# options.headless = True

path_driver = ".\\chromedriver.exe"
service = Service(path_driver)
driver = webdriver.Chrome(
    service=service,
    options=options
)

url = "http://127.0.0.1:8000/room/main/"

try:
    # вошли на главную страницы
    driver.get(url)
    time.sleep(1)

    # ввели код комнаты в окошко и нашали войти
    input_room_code = driver.find_element(By.CSS_SELECTOR, "[name='room_code']")
    time.sleep(1)

    btn_enter_game = driver.find_element(By.CSS_SELECTOR, "#btn-enter-game")
    btn_enter_game.click()
    time.sleep(4)

    # room_code_input.clear()
    # room_code_input.send_keys("SQPQ")
    #
    # print("Passing authentication...")
    # email_input = driver.find_element_by_id("index_email")
    # email_input.clear()
    # email_input.send_keys(vk_phone)
    # time.sleep(5)
    #
    # password_input = driver.find_element_by_id("index_pass")
    # password_input.clear()
    # password_input.send_keys(vk_password)
    # time.sleep(3)
    # password_input.send_keys(Keys.ENTER)
    #
    # # login_button = driver.find_element_by_id("index_login_button").click()
    # time.sleep(10)
    #
    # print("Going to the profile page...")
    # profile_page = driver.find_element_by_id("l_pr").click()
    # time.sleep(5)
    #
    # print("Start watching the video...")
    # video_block = driver.find_element_by_class_name("VideoPreview__thumbWrap").click()
    # time.sleep(5)
    # print("Finish watching the video...")

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()