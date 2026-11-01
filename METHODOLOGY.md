# METHODOLOGY — Muirakitan RE

Seis etapas. Cada uma produz artefato persistente, tem critério de saída e pode
ser interrompida sem perda de trabalho.

## 0. Regra de evidência

Toda afirmação técnica é escrita neste formato:

```md
- **Afirmação:** o endpoint `POST /v1/orders` aceita `payment_method` como string livre.
- **Evidência:** `evidence/logs/2026-11-01-orders-422.json` (linha 12), SHA-256 `ab12…`
- **Confiança:** Confirmado
- **Como validar:** repetir a chamada com valor inválido e observar 422.
```

### Escala de confiança

| Nível | Significado | Exigência |
| --- | --- | --- |
| **Confirmado** | Observado diretamente ou provado por teste | Evidência reproduzível anexada |
| **Provável** | Inferido de evidência forte, sem observação direta | Pelo menos 2 evidências convergentes |
| **Hipótese** | Plausível, não verificado | Deve constar na lista de pendências |

Hipótese **nunca** entra em especificação de contrato nem em relatório de
segurança como se fosse fato. Ela entra como risco a investigar.

### Anti-padrões proibidos

- "Provavelmente usa JWT" sem capturar token.
- "A arquitetura é de microserviços" sem mapear processos/rede.
- "Vulnerável a SQL injection" sem payload e resposta.
- Descrever comportamento de tela sem screenshot ou trace.
- Preencher lacuna com conhecimento genérico de framework.

---

## RE-01 — Discovery

**Objetivo:** saber o que existe antes de opinar sobre como funciona.

| Item | Conteúdo |
| --- | --- |
| Entrada | Autorização assinada, alvo definido |
| Atividades | Inventário de superfícies, tecnologias, pontos de entrada, atores, dados |
| Artefatos | `docs/discovery/inventory.md`, `docs/discovery/surface-map.md`, `docs/discovery/actors.md` |
| Ferramentas | Playwright (web), leitura de repositório, `file`/`strings` (binário) |
| Saída | Toda superfície tem dono, tecnologia e nível de acesso declarados |

**Critério de saída:** é possível responder "quais são as entradas do sistema e
quem pode usá-las?" sem consultar o alvo.

**Perguntas obrigatórias:** O que é público? O que exige autenticação? O que é
interno? O que é desconhecido? (Desconhecido é resposta válida e deve ser
listado.)

---

## RE-02 — Inspection

**Objetivo:** mapa estrutural. Como as peças se conectam.

| Item | Conteúdo |
| --- | --- |
| Entrada | `docs/discovery/*` |
| Atividades | Mapear componentes, dependências, camadas, contratos implícitos, pontos de acoplamento |
| Artefatos | `docs/architecture/component-map.md`, `docs/architecture/dependency-graph.md`, `docs/architecture/decisions/ADR-*.md` |
| Ferramentas | Análise estática, leitura de manifesto (`package.json`, `pom.xml`, `requirements.txt`), Ghidra/Rizin quando binário |
| Saída | Diagrama de componentes + grafo de dependências com versões |

**Critério de saída:** toda dependência crítica tem versão, origem e status de
manutenção declarados.

**Sinal de alerta:** dependência sem versão fixada, fork não rastreado, biblioteca
abandonada. Isso vai para `docs/security/`.

---

## RE-03 — Behavioral Analysis

**Objetivo:** observar o que o sistema **faz**, não o que ele diz que faz.

| Item | Conteúdo |
| --- | --- |
| Entrada | `docs/architecture/*` |
| Atividades | Exercitar fluxos, capturar requisições/respostas, mapear regras de negócio, estados e erros |
| Artefatos | `docs/api-analysis/endpoints.md`, `docs/api-analysis/flows.md`, `docs/api-analysis/state-machines.md`, `evidence/logs/`, `evidence/screenshots/` |
| Ferramentas | Playwright (trace + HAR), cliente HTTP, Frida (processo local autorizado) |
| Saída | Cada fluxo tem caminho felizes, caminhos de erro e pré-condições |

**Critério de saída:** um fluxo só é "documentado" quando é possível reproduzi-lo
a partir da documentação, sem olhar o sistema.

**Regra:** nunca testar em produção. Alvo em ambiente isolado, com dados
sintéticos.

---

## RE-04 — Specification

**Objetivo:** transformar observação em requisito formal (SDD).

| Item | Conteúdo |
| --- | --- |
| Entrada | `docs/discovery/*`, `docs/architecture/*`, `docs/api-analysis/*` |
| Atividades | Derivar requisitos, contratos, critérios de aceitação, decisões |
| Artefatos | `specs/requirements/*.md`, `specs/contracts/*.yaml`, `specs/acceptance/*.feature` |
| Ferramentas | Nenhuma externa; trabalho de síntese |
| Saída | Especificação que uma equipe que nunca viu o sistema consegue implementar |

**Critério de saída:** todo requisito é rastreável a uma evidência de RE-01/02/03.
Requisito sem rastreabilidade é marcado como **novo**, não como reconstruído.

**Distinção obrigatória:**
- `REQUISITO RECONSTRUÍDO` — comportamento observado no sistema original.
- `REQUISITO NOVO` — decisão do cliente, sem lastro no original.

Misturar os dois é o erro mais caro da reconstrução.

---

## RE-05 — Reconstruction

**Objetivo:** implementar uma alternativa independente a partir da especificação.

| Item | Conteúdo |
| --- | --- |
| Entrada | `specs/**` |
| Atividades | Nova arquitetura, implementação, testes unitários e de contrato |
| Artefatos | `src/**`, `tests/**`, `docs/reconstruction/plan.md` |
| Ferramentas | Stack do cliente (padrão Muirakitan: NestJS, React, MongoDB) |
| Saída | Sistema que satisfaz os contratos de RE-04 |

**Critério de saída:** todos os critérios de aceitação têm teste automatizado
associado.

**Regra:** a implementação **não** consulta o código original. Consultar o
original durante a reconstrução reintroduz as mesmas decisões e invalida o
exercício de independência.

---

## RE-06 — Validation

**Objetivo:** provar equivalência e reportar risco.

| Item | Conteúdo |
| --- | --- |
| Entrada | `specs/acceptance/*`, `src/**`, `tests/**` |
| Atividades | Testes de equivalência funcional, comparação de respostas, revisão de segurança, registro de divergências |
| Artefatos | `docs/reconstruction/equivalence-report.md`, `docs/security/findings.md`, `evidence/hashes/manifest.json` |
| Ferramentas | Playwright (regressão de fluxo), testes de contrato, análise de dependências |
| Saída | Relatório com % de equivalência, divergências justificadas, riscos residuais |

**Critério de saída:** toda divergência tem decisão registrada: aceita,
corrigida ou fora de escopo.

---

## Gates entre etapas

| Gate | Pergunta | Quem aprova |
| --- | --- | --- |
| G0 | Existe autorização escrita e escopo? | Operador |
| G1 | O inventário cobre todas as superfícies conhecidas? | Operador |
| G2 | O mapa estrutural tem dependências críticas resolvidas? | Orchestrator |
| G3 | Os fluxos críticos foram observados, não presumidos? | Operador |
| G4 | A especificação é rastreável e distingue novo de reconstruído? | Operador |
| G5 | A reconstrução tem teste para cada critério de aceitação? | Orchestrator |
| G6 | O relatório declara o que ficou fora do escopo? | Operador |

**G0 é bloqueante e não negociável.**

## Regras de parada

O agente interrompe e escala ao operador quando:

1. O alvo se comporta de forma inconsistente com a autorização.
2. Aparece dado pessoal, credencial ou segredo real.
3. A análise exigiria ação fora do ambiente isolado.
4. Duas evidências conflitam e não há como resolver sem decisão humana.
5. O escopo declarado se mostra insuficiente para responder à pergunta.

## Artefatos por etapa

```
evidence/authorization/  ← G0
docs/discovery/          ← RE-01
docs/architecture/       ← RE-02
docs/api-analysis/       ← RE-03
specs/                   ← RE-04
src/                     ← RE-05
tests/                   ← RE-06
docs/security/           ← transversal
evidence/hashes/         ← transversal
```
