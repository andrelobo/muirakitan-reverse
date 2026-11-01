# ARCHITECTURE — Muirakitan Reverse Engineering Engine

## 1. Princípios

**P1. Um agente não faz tudo.**
Um agente monolítico acumula contexto, perde foco e confunde descoberta com
conclusão. O engine usa um orquestrador e especialistas com contexto fresco.

**P2. Estado vive em arquivos, não em conversa.**
Cada etapa lê artefatos da etapa anterior e escreve os seus. O pipeline é
retomável, auditável e revisável por humano.

**P3. Ferramenta é MCP; raciocínio é agente.**
MCP não é o agente e não é o motor de engenharia reversa. É a camada de
integração entre o modelo e as ferramentas.

**P4. O harness é a fronteira de segurança.**
Permissões, isolamento e escopo são impostos pelo harness do OpenCode, não pela
boa vontade do prompt.

**P5. Evidência ou não existe.**
Toda afirmação técnica carrega `evidência` + `confiança` + `como validar`.

## 2. Visão geral

```
                        ┌──────────────────────────┐
                        │  Engenheiro / Operador   │
                        │  alvo · autorização ·    │
                        │  escopo · objetivos      │
                        └────────────┬─────────────┘
                                     │
                        ┌────────────▼─────────────┐
                        │   Orchestrator Agent     │
                        │   OpenCode · SDD ·       │
                        │   gates · handoff        │
                        └────────────┬─────────────┘
                                     │ subagent
        ┌───────────────┬────────────┼────────────┬────────────────┐
        │               │            │            │                │
┌───────▼──────┐ ┌──────▼───────┐ ┌──▼─────────┐ ┌▼──────────────┐
│  Discovery   │ │   Analysis   │ │  Security  │ │ Specification │
│  inventário  │ │  arquitetura │ │  riscos    │ │  requisitos   │
│  superfície  │ │  dependências│ │  configs   │ │  contratos    │
└───────┬──────┘ └──────┬───────┘ └──┬─────────┘ └┬──────────────┘
        │               │            │            │
        └───────────────┴────────────┴────────────┘
                                     │
                        ┌────────────▼─────────────┐
                        │      MCP Tool Layer      │
                        │ Playwright · Ghidra ·    │
                        │ Binwalk · Frida · Rizin  │
                        │ Python · Git · fs        │
                        └────────────┬─────────────┘
                                     │
                        ┌────────────▼─────────────┐
                        │  Evidence & Validation   │
                        │ testes · hashes · logs · │
                        │ relatórios · revisão     │
                        └──────────────────────────┘
```

## 3. Componentes

### 3.1 Operador
Humano. Define alvo, confirma autorização, aprova escopo e assina o relatório.
Nenhuma etapa avança sem decisão humana explícita nos gates.

### 3.2 Orchestrator (`orchestrator`)
- Valida que existe autorização registrada em `evidence/authorization/`.
- Decompõe o objetivo em etapas RE-01…RE-06.
- Escolhe qual especialista acionar e com qual contexto.
- Mantém o registro de decisões em `docs/architecture/decisions/`.
- Não executa análise técnica diretamente.

### 3.3 Especialistas

| Agente | Pergunta que responde | Escreve em |
| --- | --- | --- |
| `discovery` | O que existe aqui? | `docs/discovery/` |
| `analysis` | Como isso funciona e do que depende? | `docs/architecture/`, `docs/api-analysis/` |
| `security` | O que está exposto, frágil ou mal configurado? | `docs/security/` |
| `specification` | O que o sistema precisa ser, formalmente? | `specs/` |

Cada especialista recebe contexto **fresco** (não herda a conversa do
orquestrador) e lê os artefatos das etapas anteriores do disco. Isso evita
contaminação de hipótese entre etapas.

### 3.4 MCP Tool Layer
Detalhado em [MCP.md](MCP.md). Resumo de responsabilidades:

| Ferramenta | Papel | Prioridade |
| --- | --- | --- |
| Playwright | Inspeção comportamental de web/API | muito alta |
| Ghidra | Desassemblagem e decompilação | alta |
| Binwalk | Identificação e extração de firmware | alta |
| Frida | Instrumentação dinâmica | alta |
| Rizin / Cutter | Análise estática complementar | média |
| Python | Automação e validação | alta |
| Git | Versionamento de artefatos | alta |
| filesystem | Leitura/escrita controlada | alta |

### 3.5 Evidence & Validation
Camada transversal, não um agente. Regras:
- Todo artefato gerado tem registro em `evidence/` com SHA-256.
- Toda conclusão tem um teste ou observação que a sustente.
- Divergência entre hipótese e evidência é registrada, não apagada.

## 4. Fluxo de dados

```
RE-01 Discovery ──► docs/discovery/inventory.md
                          │
RE-02 Inspection ──► docs/architecture/component-map.md
                     docs/architecture/dependency-graph.md
                          │
RE-03 Behavioral ──► docs/api-analysis/endpoints.md
                     docs/api-analysis/flows.md
                     evidence/logs/*.har, *.json
                          │
RE-04 Specification ─► specs/requirements/*.md
                       specs/contracts/*.yaml
                       specs/acceptance/*.feature
                          │
RE-05 Reconstruction ─► src/**
                          │
RE-06 Validation ─────► tests/**
                        docs/reconstruction/equivalence-report.md
```

Regra de handoff: uma etapa só começa quando o **critério de saída** da anterior
está satisfeito ([METHODOLOGY.md](METHODOLOGY.md)). Artefato ausente = etapa
incompleta, mesmo que o agente "ache" que terminou.

## 5. O harness

O que o OpenCode efetivamente controla neste laboratório:

| Controle | Onde | Efeito |
| --- | --- | --- |
| Modelo por agente | `.opencode/agents/*.md` (`model`) | Especialista caro só onde compensa |
| Permissões | `opencode.jsonc` + frontmatter | Impede escrita indevida, comando destrutivo |
| Limite de passos | `steps` | Evita loop improdutivo |
| Isolamento de contexto | modo `subagent` | Sem contaminação entre etapas |
| Ferramentas | `mcp.servers` | Superfície mínima exposta ao modelo |
| Instruções | `AGENTS.md`, `instructions` | Regras sempre carregadas |

O harness não substitui isolamento de máquina. Ele limita o que o **agente**
pode pedir; a VM/container limita o que o **processo** pode alcançar.

## 6. Decisões arquiteturais

### ADR-001 — Especialistas em vez de agente único
**Contexto:** um agente único tem contexto limitado e tende a tratar hipótese
como fato após muitas etapas.
**Decisão:** orquestrador + 4 especialistas com contexto fresco.
**Consequência:** mais chamadas de modelo; artefatos em disco passam a ser
obrigatórios.

### ADR-002 — Artefatos Markdown + YAML, não banco
**Contexto:** precisamos de diff, revisão e portabilidade.
**Decisão:** tudo em arquivo versionado no Git.
**Consequência:** sem consulta relacional; busca é por `grep`.

### ADR-003 — Evidência bruta fora do Git
**Contexto:** HARs, dumps e imagens de firmware são grandes.
**Decisão:** binários ficam em `evidence/` local, com hash e metadados
versionados.
**Consequência:** reprodutibilidade exige reobtenção do artefato; o hash prova
que é o mesmo.

### ADR-004 — SHA-256 como padrão de integridade
**Contexto:** MD5 tem colisões conhecidas e não comprova autenticidade.
**Decisão:** SHA-256 obrigatório; MD5 só como compatibilidade legada.
**Consequência:** nenhuma cadeia de confiança sem assinatura digital.

### ADR-005 — OpenCode como harness, não como produto
**Contexto:** o engine precisa ser auditável e substituível.
**Decisão:** toda a lógica de metodologia está em documentos; o OpenCode é a
camada de execução.
**Consequência:** trocar de harness não invalida a metodologia.
