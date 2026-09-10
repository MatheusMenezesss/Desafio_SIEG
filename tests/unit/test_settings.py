from automation.config import settings


def test_to_bool_accepts_truthy_values():
    assert settings._to_bool("true") is True
    assert settings._to_bool("YES") is True
    assert settings._to_bool("1") is True


def test_get_settings_has_defaults(monkeypatch):
    settings.get_settings.cache_clear()
    monkeypatch.delenv("BROWSER", raising=False)
    cfg = settings.get_settings()
    assert cfg.browser == "chrome"
    assert cfg.timeout == 10
