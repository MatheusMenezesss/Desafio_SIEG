# Contribuindo

## Fluxo de branches
- `main`: branch estável.
- `feature/<descricao-curta>`: novas funcionalidades.
- `fix/<descricao-curta>`: correções.

## Commits
- Use mensagens claras no imperativo.
- Preferencialmente siga Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`).

## Pull Requests
1. Mantenha o escopo pequeno e focado.
2. Descreva o contexto, a solução e o impacto.
3. Referencie issue(s) relacionada(s).

## Qualidade antes de abrir PR
Execute localmente:

```bash
ruff check .
black --check .
pytest
```

## Documentação
Sempre que alterar arquitetura, configuração, fluxo ou testes, atualize:
- `README.md`
- Arquivos relevantes em `docs/`
