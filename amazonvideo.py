from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from base import  WebDriverController, ConfigManager
import time

class AmazonVideoPage(WebDriverController):
    def __init__(self, driver, config_file):
        super().__init__(driver, config_file)
        self.url = 'https://www.primevideo.com'
        self.ui_controller = WebDriverController(driver, config_file)

    def play_first_video(self, duration: int, email: str, password: str) -> bool:
        result = True
        self.open_url(self.url)
        time.sleep(2)
        self.login_without_login(self.ui_controller)

        if self.ui_controller.wait_until("login", "login_button", timeout=10):
            ui_controller.find_element("login", "login_button").click()

        else:
            print("log-in button is not found")
            return False

        result &= self.login_(self.ui_controller ,email, password)
        time.sleep(3)

        try:
            result &= self.play_video(duration, self.video_locator, self.play_button_locator)
        except NoSuchElementException as e:
            print(f"Error: {e}")
            result = False

        return result

    def play_video(self, duration: int, video_locator, play_button_locator) -> bool:
        result = True
        try:
            if self.ui_controller.wait_until("video", "video_element", timeout=10):
                self.ui_controller.find_element("video", "video_element").click()
                self.ui_controller.find_element("video", "play_button").click()

                time.sleep(duration)
            else:
                print("Video element or play button not found.")
                result = False
        except NoSuchElementException as e:
            print(f"Error: {e}")
            result = False
        return result
    def login_without_login(self, ui_controller: WebDriverController,  )-> bool:
        result=False
        if ui_controller.wait_until("login", "accept_cookies", timeout=10):
            ui_controller.find_element("login", "accept_cookies").click()
            result=True

        return result
    def login_(self, ui_controller: WebDriverController, email: str,password: str) -> bool:  # Performs the login process using provided email and password

        ui_controller.find_element("login", "email").send_keys(email)

        if ui_controller.wait_until("login", "continue_button", timeout=10):
            ui_controller.find_element("login", "continue_button").click()

        if ui_controller.wait_until("login", "password", timeout=10):
            ui_controller.find_element("login", "password").send_keys(password)

        if ui_controller.wait_until("login", "login_button2", timeout=5):
            ui_controller.find_element("login", "login_button2").click()









