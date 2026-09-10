from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Desafio_SIEG.config import PAGE_TIMEOUT

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
            self.wait.until(EC.element_to_be_clickable(locator)).click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def fill_input(self, locator, text):
        element = self.wait.until(EC.presence_of_element_located(locator))
        element.clear()
        element.send_keys(text)



