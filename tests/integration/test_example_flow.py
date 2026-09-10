from automation.config import Settings
from automation.flows import ExampleFlow


class DummyPage:
    def __init__(self):
        self.opened_with = None

    def open(self, base_url: str) -> None:
        self.opened_with = base_url

    def read_title(self) -> str:
        return "Example Domain"


def test_example_flow_orchestrates_page_calls():
    page = DummyPage()
    settings = Settings(
        browser="chrome",
        headless=True,
        base_url="https://example.com",
        timeout=10,
        window_width=1366,
        window_height=768,
        log_level="INFO",
    )

    flow = ExampleFlow(page=page, settings=settings)
    result = flow.execute()

    assert page.opened_with == "https://example.com"
    assert result == "Example Domain"
