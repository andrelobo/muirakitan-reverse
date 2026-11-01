---
name: Registrar evidência
description: Registra um artefato de evidência com hash SHA-256, cadeia de custódia e entrada no manifesto
---

# Registrar evidência

Use sempre que produzir um artefato que sustenta uma afirmação técnica:
captura de tela, HAR, log, dump, saída de ferramenta, resposta de API.

## Workflow

1. **Nomeie pelo conteúdo, não pelo desejo.** Formato:
   `evidence/<tipo>/<AAAA-MM-DD>-<alvo>-<descricao>.<ext>`
   Exemplo: `evidence/logs/2026-11-01-orders-422-invalid-payment.json`

2. **Grave o artefato** no diretório do tipo correto:
   - `evidence/screenshots/` — captura visual
   - `evidence/logs/` — texto, JSON, HAR, saída de ferramenta
   - `evidence/hashes/` — manifestos (não é artefato bruto)

3. **Calcule o hash** e registre no manifesto:

   ```sh
   ./scripts/hash-manifest.sh
   ```

   O script recalcula SHA-256 de tudo em `evidence/` e reescreve
   `evidence/hashes/manifest.json`. Não edite o manifesto à mão.

4. **Registre a cadeia de custódia** em `evidence/logs/<arquivo>.meta.md`:

   ```md
   # Metadados de evidência

   - **Artefato:** evidence/logs/2026-11-01-orders-422-invalid-payment.json
   - **SHA-256:** <hash>
   - **Coletado por:** <agente | operador>
   - **Data/hora (UTC):** 2026-11-01T14:22:03Z
   - **Ambiente:** <container/VM, imagem, hash da imagem>
   - **Comando:** <comando exato que gerou>
   - **Alvo:** <identificador do alvo, dentro do escopo>
   - **Autorização:** evidence/authorization/<arquivo>
   ```

5. **Cite na afirmação**:

   ```md
   - **Evidência:** `evidence/logs/2026-11-01-orders-422-invalid-payment.json`
     (SHA-256 `ab12…`)
   ```

## Regras

- SHA-256 é o padrão. MD5 só como compatibilidade legada e nunca como prova de
  autenticidade.
- Hash prova integridade, não origem. Autenticidade exige assinatura digital.
- Nunca sobrescreva artefato existente. Gere novo arquivo com sufixo `-v2`.
- Evidência que contradiz a conclusão não é apagada: é registrada e explicada.
- Redija segredo, token e dado pessoal antes de versionar.
- Artefato binário grande fica fora do Git (`.gitignore`); o hash fica.

## Referências

- `templates/evidence-record.md`
- `SECURITY.md` §6 — integridade da evidência
