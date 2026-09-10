# Arquitetura

## Objetivo
Fornecer uma base de automação Selenium simples para começar, mas robusta para crescer.

## Camadas
- **main**: ponto de entrada da execução.
- **flows**: orquestração de casos de uso.
- **pages (POM)**: interações e localizadores por página.
- **browser**: criação do WebDriver, opções e waits.
- **config**: leitura centralizada de variáveis de ambiente.
- **utils**: logging e recursos compartilhados.
- **exceptions**: erros de domínio da automação.

## Fluxo de execução
`main -> flow -> page object -> browser -> selenium`

## Decisões arquiteturais
1. **POM** para reduzir duplicação de localizadores/interações.
2. **Flows separados** para concentrar regras de processo e evitar regra de negócio em páginas.
3. **WebDriver centralizado** para garantir consistência e facilitar múltiplos navegadores no futuro.
4. **Waits explícitos reutilizáveis** para evitar `time.sleep()` e reduzir flaky tests.

## Separação Flow x Page Object x Browser
- Page Object: só conhece sua página.
- Flow: conhece a jornada.
- Browser: conhece o Selenium/WebDriver.
