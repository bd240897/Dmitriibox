from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
import time
import pickle
from selenium.webdriver.common.by import By
import random

# https://www.youtube.com/watch?v=Myl8Br5aRf4&list=PLqGS6O1-DZLp1kgiQNpueIMCHRNzgHa1r
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


# курс который сомтрел
# https://www.youtube.com/watch?v=cInWsj199Kk&list=PLqGS6O1-DZLp1kgiQNpueIMCHRNzgHa1r&index=5

class TestGame:

    # https://docs.djangoproject.com/en/4.1/topics/testing/tools/
    room_code = random.choices(['A', "B", "C", "D", "E", "F"]*3, k=4)

    def __init__(self):
        print(self.room_code)

    def enter_main_room(self):
        url = "http://127.0.0.1:8000/room/main/"
        driver.get(url)
        time.sleep(1)
        print("Вошли на главную страницу")

    def enter_to_room(self, room_code=room_code):
        # Входим в комнату 1й раз
        # ввели код комнаты в окошко и нашали войти
        input_room_code = driver.find_element(By.CSS_SELECTOR, "[name='room_code']")
        input_room_code.clear()
        input_room_code.send_keys(room_code)
        time.sleep(1)

        btn_enter_game = driver.find_element(By.CSS_SELECTOR, "#btn-enter-game")
        btn_enter_game.click()
        time.sleep(1)
        print("Входим в комнату 1й раз")

    def login(self):
        # логин
        input_username = driver.find_element(By.CSS_SELECTOR, "#id_username")
        input_username.clear()
        input_username.send_keys('user1')

        input_password = driver.find_element(By.CSS_SELECTOR, "#id_password")
        input_password.clear()
        input_password.send_keys('1234qwerS')

        btn_submit = driver.find_element(By.CSS_SELECTOR, "[type='submit']")
        btn_submit.click()
        time.sleep(1)
        print("Логин в игру")

    def start_game(self):
        # начать игру
        # driver.implicitly_wait(10)
        btn_start_game = driver.find_element(By.CSS_SELECTOR, "#pop-start-game")
        btn_start_game.click()
        time.sleep(1)
        print("Начали игру")

    def type_answer(self):
        # пишем ответы
        # driver.implicitly_wait(10)
        textarea_answer = driver.find_element(By.CSS_SELECTOR, "textarea")
        textarea_answer.clear()
        textarea_answer.send_keys('1111111111111')
        time.sleep(2)

        btn_submit = driver.find_element(By.CSS_SELECTOR, "[type='submit']")
        btn_submit.send_keys("\n")
        time.sleep(1)
        print("Ввели и отправили ответ")

    def wait_answer(self):
        btn_submit = driver.find_element(By.CSS_SELECTOR, ".waiting-typing-done a")
        btn_submit.click()
        time.sleep(1)
        print("Дождались всех игроков")

    def look_list_results(self):
        btn_submit = driver.find_element(By.CSS_SELECTOR, ".results_to_end a")
        btn_submit.send_keys("\n")
        time.sleep(1)
        print("Посмотрели все ответы игры")

    def game_over(self):
        btn_submit = driver.find_element(By.CSS_SELECTOR, ".results_to_end a")
        btn_submit.click()
        time.sleep(1)
        print("Перешли на окно закончить игру")

    def delete_room(self):
        btn_submit = driver.find_element(By.CSS_SELECTOR, ".waiting-typing-done a:last-child")
        btn_submit.click()
        time.sleep(1)
        print("Удалили комнату")


    def run_one_game(self):
        self.enter_main_room()
        self.enter_to_room()
        self.login()
        self.enter_to_room()
        self.start_game()
        self.type_answer()
        self.wait_answer()
        self.look_list_results()
        self.game_over()
        self.delete_room()
try:
    test1 = TestGame()
    test1.run_one_game()

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()