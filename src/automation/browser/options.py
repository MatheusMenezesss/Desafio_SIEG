from selenium.webdriver import ChromeOptions

from automation.config import Settings


def build_chrome_options(settings: Settings) -> ChromeOptions:
    options = ChromeOptions()
    options.add_argument(f"--window-size={settings.window_width},{settings.window_height}")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    if settings.headless:
        options.add_argument("--headless=new")
    return options
