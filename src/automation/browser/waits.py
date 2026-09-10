from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def wait_for_visibility(driver: WebDriver, locator: tuple[str, str], timeout: int):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
