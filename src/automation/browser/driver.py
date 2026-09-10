import logging

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from automation.browser.options import build_chrome_options
from automation.config import get_settings
from automation.exceptions import BrowserInitializationError

logger = logging.getLogger(__name__)


def create_driver() -> WebDriver:
    settings = get_settings()

    if settings.browser != "chrome":
        raise BrowserInitializationError(
            f"Navegador '{settings.browser}' ainda não suportado. Use BROWSER=chrome."
        )

    try:
        logger.info("Inicializando WebDriver para browser=%s", settings.browser)
        driver = webdriver.Chrome(options=build_chrome_options(settings))
        driver.set_page_load_timeout(settings.timeout)
        driver.implicitly_wait(0)
        return driver
    except Exception as exc:  # noqa: BLE001
        raise BrowserInitializationError("Falha ao inicializar o WebDriver") from exc


def quit_driver(driver: WebDriver | None) -> None:
    if driver is not None:
        logger.info("Encerrando WebDriver")
        driver.quit()
