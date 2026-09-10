# Estratégia de testes

## Unit
Valida componentes isolados sem navegador real.

## Integration
Valida integração entre camadas (ex.: flow + page mockada).

## E2E
Valida fluxo completo com navegador real e ambiente controlado.

## Fixtures
`tests/conftest.py` centraliza:
- criação opcional de driver;
- teardown automático;
- sinalizador `--run-e2e` para evitar execução acidental de E2E.
