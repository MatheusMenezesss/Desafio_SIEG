import logging

from automation.config import Settings
from automation.pages import ExamplePage

logger = logging.getLogger(__name__)


class ExampleFlow:
    def __init__(self, page: ExamplePage, settings: Settings) -> None:
        self.page = page
        self.settings = settings

    def execute(self) -> str:
        logger.info("Executando flow de exemplo")
        self.page.open(self.settings.base_url)
        title = self.page.read_title()
        logger.info("Título coletado: %s", title)
        return title
