from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from automation.browser.waits import wait_for_visibility


class ExamplePage:
    TITLE = (By.TAG_NAME, "h1")

    def __init__(self, driver: WebDriver, timeout: int) -> None:
        self.driver = driver
        self.timeout = timeout

    def open(self, base_url: str) -> None:
        self.driver.get(base_url)

    def read_title(self) -> str:
        element = wait_for_visibility(self.driver, self.TITLE, self.timeout)
        return element.text
