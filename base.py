from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

class BasePage:
    def __init__(self, driver, config_file):
        self.driver = driver
        self.config_file = config_file
        self.config = ConfigManager.get_config(config_file)

    def open_url(self, url):
        try:
            self.driver.get(url)
            self.driver.maximize_window()
        except WebDriverException as e:
            print(f"Error opening URL: {e}")

    def find_element(self, section, element):
        locator_info = self.config.get(section, {}).get(element, {})
        if not locator_info:
            print(f"Locator configuration for {section}:{element} is missing.")
            return None
        locator_type = locator_info.get('type')
        path = locator_info.get('path')

        if not path:
            print(f"Locator path for {section}:{element} is missing or empty.")
            return Non
        by_map = {'xpath': By.XPATH,'id': By.ID,'name': By.NAME,'class_name': By.CLASS_NAME,'css_selector': By.CSS_SELECTOR}

        by_type = by_map.get(locator_type)
        if by_type is None:
            print(f"Locator type '{locator_type}' is not supported.")
            return None

        try:
            element = self.driver.find_element(by_type, path)
            return element
        except NoSuchElementException:
            print(f"Element not found with {locator_type}='{path}'")
            return None

    def click(self, section, element):
        elem = self.find_element(section, element)
        if elem:
            elem.click()

    def send_keys(self, section, element, keys):
        elem = self.find_element(section, element)
        if elem:
            elem.send_keys(keys)


class WebDriverController(BasePage):
    def __init__(self, driver=None, config_file=None):
        self.driver = driver
        self.config_file = config_file
        if config_file:
            self.config = ConfigManager.get_config(config_file)
        else:
            self.config = None

    def get(self, url):
        try:
            self.driver.get(url)
        except WebDriverException as e:
            print(f"Error navigating to URL: {e}")



    def open(self, driver_options: Options, browser: str = "chrome"):
        try:
            if browser == "chrome":
                self.driver = webdriver.Chrome(options=driver_options)
        except WebDriverException as e:
            print(f"Error opening browser: {e}")

    def close(self):
        try:
            if self.driver:
                self.driver.quit()
        except WebDriverException as e:
            print(f"Error closing browser: {e}")

    def wait_until(self, section: str, element: str, timeout=10):
        locator = self.get_locator(section, element)
        by_type, path = locator
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by_type, path))
            )
            return element
        except TimeoutException:
            print(f"Timed out waiting for element: {locator}")
            return None


    def prepare_options(self, headless: bool = False) -> Options:
        options = Options()
        options.headless = headless
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        options.add_argument("--display=:99")
        return options

class ConfigManager:
    @staticmethod
    def get_config(config_file):
        try:
            with open(config_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"File {config_file} not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file {config_file}.")
        return None
