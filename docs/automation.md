# Como adicionar nova automação

## Passo a passo
1. Criar Page Object em `src/automation/pages`.
2. Criar Flow em `src/automation/flows` orquestrando as páginas.
3. Adicionar testes em `tests/unit`, `tests/integration` e, se necessário, `tests/e2e`.
4. Incluir novas configurações em `.env.example` e `settings.py`.
5. Atualizar documentação relevante.

## Fluxo recomendado

Nova automação
│
├── Page Object
├── Flow
├── Service (se necessário)
├── Testes
└── Documentação

## Exemplo mínimo

```python
# pages/search_page.py
class SearchPage:
    def __init__(self, driver):
        self.driver = driver

    def open(self, base_url: str) -> None:
        self.driver.get(f"{base_url}/search")
```

```python
# flows/search_flow.py
class SearchFlow:
    def __init__(self, page):
        self.page = page

    def execute(self, base_url: str) -> None:
        self.page.open(base_url)
```
