# Infra de sandbox (herdada do rascunho v1)

Origem: `muirakitan-reverse-engineering/.opencode/config/` (rascunho de 2026-11-01,
preservado em `archive/v1-draft/`). Copiado em 2026-11-02.

## Antes de usar, adaptar

- `docker-compose.yml` espera o layout antigo: `../evidence` e `../sandbox`
  relativos a este diretório. Aqui `evidence/` fica na raiz do repositório
  (`../../evidence`) e `sandbox/` não existe.
- `mcp-base` monta `/var/run/docker.sock` — conflita com `SECURITY.md` §3
  (isolamento). Remover salvo decisão explícita do operador.
- Imagens referenciam `muirakitan/mcp-*:latest`; nenhuma foi construída ainda.
- Isto é andaime para a Fase 2 (Ghidra, Binwalk, Frida, Rizin), não parte do
  harness atual do OpenCode. O gate efetivo hoje é `opencode.jsonc` + `SECURITY.md`.

`../harness/permissions.yaml` é do mesmo rascunho e usa schema próprio, não lido
pelo OpenCode v2. Serve como referência de políticas por etapa RE.
