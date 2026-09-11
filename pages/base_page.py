from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config import PAGE_TIMEOUT

import time
class BasePage:

    def __init__(self, driver:WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, PAGE_TIMEOUT)
    
    def click_element(self, locator):
        """Tenta o clique padrão; se interceptado, faz via JavaScript"""
        element = self.wait.until(EC.presence_of_element_located(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            self.wait.until(EC.element_to_be_clickable(locator)).click()
        except TimeoutException:
            print(f"[ERROR] Timeout ao tentar localizar o elemento: {locator}")
            raise

    def fill_input(self, locator, text):
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            element.clear()
            element.send_keys(text)
        except TimeoutException:
            print(f"[ERROR] Timeout ao tentar localizar o campo de entrada: {locator}")
            raise



