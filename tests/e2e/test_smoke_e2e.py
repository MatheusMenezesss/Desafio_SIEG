import pytest

from automation.config import get_settings
from automation.pages import ExamplePage


@pytest.mark.e2e
def test_example_page_loads_title(browser_driver):
    if browser_driver is None:
        pytest.skip("Driver não disponível sem --run-e2e")

    settings = get_settings()
    page = ExamplePage(browser_driver, timeout=settings.timeout)
    page.open(settings.base_url)

    assert page.read_title()
