import logging

from automation.browser import create_driver, quit_driver
from automation.config import get_settings
from automation.flows import ExampleFlow
from automation.pages import ExamplePage
from automation.utils import configure_logging

logger = logging.getLogger(__name__)


def run() -> str:
    settings = get_settings()
    configure_logging(settings.log_level)

    driver = create_driver()
    try:
        page = ExamplePage(driver=driver, timeout=settings.timeout)
        flow = ExampleFlow(page=page, settings=settings)
        return flow.execute()
    finally:
        quit_driver(driver)


if __name__ == "__main__":
    result = run()
    logger.info("Execução finalizada com resultado: %s", result)
