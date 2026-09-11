from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config import BASE_URL, PORTAL_PASSWORD, TEAM_TOKEN
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

class LoginPage(BasePage):
    # Seletores flexíveis (buscam por id, name ou atributos parciais)
    INPUT_TOKEN = (By.XPATH, "//input[@name='teamToken' or @name='token' or contains(@id, 'token')]")
    INPUT_SENHA = (By.XPATH, "//input[@type='password']")
    BTN_SUBMIT = (By.XPATH, "//button[@type='submit' or contains(., 'Entrar') or contains(., 'Acessar')]")

    def logar(self):
        self.driver.get(BASE_URL)
        self.fill_input(self.INPUT_TOKEN, TEAM_TOKEN)
        self.fill_input(self.INPUT_SENHA, PORTAL_PASSWORD)
        self.click_element(self.BTN_SUBMIT)