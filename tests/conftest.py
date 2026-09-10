import pytest

from automation.browser import create_driver, quit_driver


def pytest_addoption(parser):
    parser.addoption("--run-e2e", action="store_true", default=False, help="Executa testes e2e")


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-e2e"):
        return
    skip_e2e = pytest.mark.skip(reason="Use --run-e2e para executar testes e2e")
    for item in items:
        if "e2e" in item.keywords:
            item.add_marker(skip_e2e)


@pytest.fixture
def browser_driver(request):
    if "e2e" not in request.keywords:
        return None
    driver = create_driver()
    yield driver
    quit_driver(driver)
