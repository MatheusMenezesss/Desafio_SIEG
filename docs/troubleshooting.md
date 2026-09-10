# Troubleshooting

## WebDriver não inicia
- Verifique versão do navegador.
- Confirme acesso à internet para o Selenium Manager baixar/resolver o driver.

## Elemento não encontrado
- Revise seletor no Page Object.
- Use waits explícitos em vez de `time.sleep()`.

## Timeout excessivo
- Ajuste `TIMEOUT` no `.env`.
- Verifique latência e estado do ambiente alvo.

## Variáveis de ambiente não carregam
- Confirme existência do arquivo `.env` na raiz.
- Verifique se os nomes estão corretos.

## Problemas de permissão
- Em Linux/macOS, confirme permissões do ambiente virtual.
- Em Windows, execute PowerShell com política de execução adequada para ativar venv.
