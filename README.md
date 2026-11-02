# muirakitan-reverse

Laboratório de **engenharia reversa assistida por IA** da Muirakitan.

Conduz investigação técnica reproduzível sobre sistemas existentes — com ou sem
documentação — e entrega resultados verificáveis. O diferencial não é usar IA
para desmontar binário; é **separar fato de hipótese, registrar evidência,
validar conclusão e reconstruir de forma independente**.

## Documentos canônicos

| Arquivo | Responde |
| --- | --- |
| [CONTEXT.md](CONTEXT.md) | Por que existe, para quem, com quais indicadores |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Como o engine é montado |
| [METHODOLOGY.md](METHODOLOGY.md) | Como a investigação é conduzida (RE-01…RE-06) |
| [AGENTS.md](AGENTS.md) | Regras de operação dos agentes |
| [MCP.md](MCP.md) | Ferramentas e integrações |
| [SECURITY.md](SECURITY.md) | Autorização, isolamento e guardrails |
| [ROADMAP.md](ROADMAP.md) | Implementação em 30 dias |
| [STATUS.md](STATUS.md) | **Ponto de retomada** — estado atual e próxima ação |

## Como usar

```sh
opencode
```

O agente padrão é o `orchestrator`. Ele valida a autorização (gate G0) e delega
as etapas aos especialistas.

```text
> analise o repositório em /caminho/do/alvo — autorização em evidence/authorization/
```

| Agente | Papel |
| --- | --- |
| `orchestrator` | Conduz o pipeline, aplica gates, delega |
| `discovery` | RE-01 — inventário de superfícies e atores |
| `analysis` | RE-02/03 — componentes, dependências, fluxos, contratos |
| `security` | Avaliação de segurança e achados |
| `specification` | RE-04 — requisitos, contratos, aceitação |

## Estrutura

```text
.
├── .opencode/
│   ├── agents/           # 5 agentes especializados
│   ├── skills/           # skills do laboratório
│   ├── config/           # compose + Dockerfiles (Fase 2, a adaptar)
│   └── harness/          # política por etapa (referência v1)
├── docs/                 # saída por etapa
│   ├── discovery/        # RE-01
│   ├── architecture/     # RE-02
│   ├── api-analysis/     # RE-03
│   ├── security/         # transversal
│   └── reconstruction/   # RE-05/06
├── specs/                # RE-04
│   ├── requirements/
│   ├── contracts/
│   └── acceptance/
├── evidence/             # prova, não opinião
│   ├── authorization/    # gate G0
│   ├── screenshots/
│   ├── logs/
│   └── hashes/
├── templates/            # formulários da metodologia
├── src/                  # RE-05
└── tests/                # RE-06
```

`docs/` é por engajamento. Se o laboratório rodar vários projetos, cada um ganha
um subdiretório com o nome do alvo.

`archive/v1-draft/` guarda os documentos da primeira versão do projeto. Não é
normativo; em caso de divergência, vale a raiz do repositório.

## Pré-requisitos

| Ferramenta | Estado | Uso |
| --- | --- | --- |
| Node.js ≥ 20 | necessário | Playwright MCP |
| Python 3 | necessário | automação de análise |
| Git | necessário | artefatos versionados |
| Docker | recomendado | isolamento do alvo |
| Ghidra / Binwalk | fase 2 | binário e firmware |
| Frida / Rizin | fase 3 | instrumentação e análise estática |

Ver [ROADMAP.md](ROADMAP.md) para a ordem de instalação.

## Regra que não se negocia

Sem autorização escrita em `evidence/authorization/`, nada é analisado. O harness
bloqueia o resto; o gate G0 bloqueia o começo.

## Estado

Fase 0 — fundação. Documentação e agentes prontos; laboratório de binário ainda
não instalado.
