class AutomationError(Exception):
    """Erro base da aplicação de automação."""


class BrowserInitializationError(AutomationError):
    """Falha ao inicializar o navegador."""
