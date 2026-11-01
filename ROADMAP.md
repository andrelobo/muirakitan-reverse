# ROADMAP — 30 dias

Objetivo do ciclo: sair de "laboratório vazio" para "primeiro serviço
estruturado com estudo de caso".

Regra do ciclo: cada fase termina com artefato em disco e critério de saída
verificado. Fase sem entrega não avança.

---

## Fase 1 — D1–D5 · Ambiente

**Entregas**
- Linux isolado (VM ou container) para alvos.
- Node.js, Python 3, Git, Docker no host de trabalho.
- Playwright MCP funcionando e apontando para alvo local.
- Ghidra e Binwalk instalados no ambiente de análise (não no host pessoal).
- `templates/authorization-scope.md` preenchido para o projeto-piloto.

**Critério de saída**
- [ ] `opencode mcp list` mostra Playwright conectado.
- [ ] Uma captura HAR de teste é gerada e hasheada em `evidence/`.
- [ ] Ambiente de alvo sobe e é destruído com um comando.

**Risco:** instalar Ghidra/Binwalk no host e perder o isolamento. Não faça.

---

## Fase 2 — D6–D10 · Agentes e harness

**Entregas**
- 5 agentes ativos: `orchestrator`, `discovery`, `analysis`, `security`,
  `specification`.
- Permissões por agente em `.opencode/agents/*.md`.
- `opencode.jsonc` com permissões globais, `default_agent` e MCP.
- Teste de fumaça: cada agente tenta escrever fora do seu diretório e é negado.

**Critério de saída**
- [ ] `default_agent` abre no orquestrador.
- [ ] Um agente especialista não consegue editar `src/`.
- [ ] Comando destrutivo (`sudo`, `dd`) é bloqueado.
- [ ] Handoff de uma etapa é gerado no formato de `AGENTS.md`.

**Risco:** permissões amplas demais "para não atrapalhar". É exatamente o que
o harness existe para evitar.

---

## Fase 3 — D11–D15 · SDD e templates

**Entregas**
- Templates RE-01 a RE-06 em `templates/`.
- Template de registro de escopo.
- `evidence/hashes/manifest.json` gerado por script.
- Skill `evidence-record` disponível.

**Critério de saída**
- [ ] É possível preencher um engajamento inteiro só com os templates.
- [ ] Manifesto de hashes é regenerado sem edição manual.
- [ ] Toda seção de afirmação tem os quatro campos obrigatórios.

---

## Fase 4 — D16–D23 · Projeto-piloto

**Alvo recomendado:** aplicação SaaS open source com frontend, backend e
documentação parcial. **Não** começar por firmware.

**Execução**
1. RE-01 — analisar interface com Playwright.
2. RE-02 — mapear componentes e dependências.
3. RE-03 — identificar fluxos e regras de negócio; mapear endpoints e contratos.
4. RE-04 — gerar especificação SDD.
5. RE-05 — implementar alternativa (NestJS + React + MongoDB).
6. RE-06 — comparar comportamento com testes automatizados.

**Critério de saída**
- [ ] ≥ 80% das funcionalidades mapeadas documentadas.
- [ ] ≥ 70% dos fluxos críticos cobertos por evidência.
- [ ] ≥ 90% dos testes de equivalência aprovados.
- [ ] Relatório de equivalência com divergências justificadas.

**Risco:** pular RE-03 e "implementar pelo que parece". Isso produz cópia de
suposição, não reconstrução.

---

## Fase 5 — D24–D30 · Comercialização

**Entregas**
- Demonstração de 10 minutos do pipeline.
- Relatório de diagnóstico do piloto (documento de cliente, não de engenheiro).
- Estudo de caso com números reais das métricas de `CONTEXT.md`.
- Proposta comercial das três ofertas, com escopo e preço.
- Página ou deck de apresentação.

**Critério de saída**
- [ ] Relatório legível por gestor não técnico.
- [ ] Métricas medidas, não estimadas.
- [ ] Proposta com escopo, prazo, entregáveis e limites explícitos.
- [ ] Nenhuma promessa de "comprometer sistema em X minutos".

---

## Depois de D30

| Ordem | Próximo passo |
| --- | --- |
| 1 | Wrapper MCP de Binwalk |
| 2 | Wrapper MCP de Ghidra |
| 3 | Segundo piloto em domínio diferente (API sem documentação) |
| 4 | Firmware Intelligence com hardware dedicado |
| 5 | Automação de relatório e versionamento de evidência |

## Indicadores do ciclo

| Indicador | Onde medir |
| --- | --- |
| Tempo até primeiro inventário útil | `docs/discovery/inventory.md` (data) |
| % funcionalidades documentadas | `docs/reconstruction/equivalence-report.md` |
| Cobertura de fluxos críticos | `docs/api-analysis/flows.md` |
| Inconsistências identificadas | `docs/security/findings.md` |
| % testes de equivalência | `tests/` |
| Tempo de reconstrução vs. convencional | `docs/reconstruction/plan.md` |
