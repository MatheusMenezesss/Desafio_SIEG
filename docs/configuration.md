# Configuração

As variáveis de ambiente são carregadas de `.env`.

- `BROWSER`: navegador alvo (`chrome` inicialmente).
- `HEADLESS`: `true`/`false` para execução sem interface.
- `BASE_URL`: URL base da aplicação.
- `TIMEOUT`: timeout padrão para waits explícitos.
- `WINDOW_WIDTH`: largura da janela.
- `WINDOW_HEIGHT`: altura da janela.
- `LOG_LEVEL`: nível de log (`DEBUG`, `INFO`, etc).

Boas práticas:
- nunca versionar `.env`;
- usar placeholders em `.env.example`;
- manter segredos em ambientes seguros (CI secrets, vault, etc).
