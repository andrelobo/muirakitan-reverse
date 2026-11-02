# Muirakitan RE — Engine Architecture

## Visão Geral

A arquitetura do Muirakitan RE baseia-se na composição de agentes especializados conectados por uma camada MCP (Model Control Protocol), operando dentro do ambiente OpenCode com políticas de harness rigorosas.

### Camadas Tecnológicas

| Camada | Responsabilidade |
|--------|-------------------|
| **OpenCode** | Coordenar agentes e execução, gerenciar contexto e permissões |
| **MCP** | Conectar modelos a ferramentas especializadas (Ghidra, Binwalk, Playwright, Frida, Python, Git, filesystem controlado) |
| **SDD** | Formalizar requisitos, decisões de arquitetura e contratos de especificação |
| **Harness** | Controlar permissões, contexto, ferramentas e execução em ambiente isolado |
| **RAG** | Recuperar documentação técnica e conhecimento do conhecimento interno |
| **Python** | Automatizar análises, validações e transformações de dados |
| **Playwright** | Inspeção comportamental de aplicações web, automação de fluxos e regressão funcional |

### Agentes Especializados

#### 1. Orchestrator Agent
- **Papel**: Coordenador geral do pipeline de engenharia reversa.
- **Responsabilidades**: Planejamento de etapas, alocação de recursos, integração de resultados parciais, garantia de fluxo metodológico.
- **Ferramentas**: OpenCode harness, MCP layer, ROADMAP.md tracking.

#### 2. Discovery Agent
- **Papel**: Mapeamento inicial do sistema.
- **Responsabilidades**: Inventário tecnológico, identificação de componentes, mapeamento de dependências, extração de entradas/saídas, fingerprinting de versões.
- **Ferramentas**: Binwalk (firmware), Playwright (web), análise de arquivos de configuração, Git history.

#### 3. Analysis Agent
- **Papel**: Análise técnica profunda.
- **Responsabilidades**: Reverse engineering de APIs, desassemblagem com Ghidra, instrumentação dinâmica com Frida, mapeamento de arquitetura, identificação de padrões de negocio.
- **Ferramentas**: Ghidra, Frida, Python scripts, Rizen/Cutter, APIspec analysis.

#### 4. Security Agent
- **Papel**: Identificação de vulnerabilidades e riscos.
- **Responsabilidades**: Análise estática de dependências, verificação de configurações inseguras, análise de superfície de ataque, identificação de hardcoded secrets, verification de cabeçalhos de segurança.
- **Ferramentas**: Python seguridad tools, dependency checkers, pattern matching, hash comparison.

#### 5. Specification Agent
- **Papel**: Traduzir evidências em especificações técnicas.
- **Responsabilidades**: Gerar requisitos formais, contratos de API, especificações de banco de dados, definição de aceitação de testes, documentação de arquitetura.
- **Ferramentas**: SDD templates, OpenAPI/Swagger generation, Markdown documentation, test specification frameworks.

#### 6. Orchestrator Agent (re-listado para ênfase)
- **Papel**: Definir alvo, autorização, escopo e objetivos antes do início da análise.
- **Responsabilidades**: Validar autorização formal, definir escopo de análise, estabelecer métricas de sucesso, aprovar entregáveis em cada etapa.

### Fluxo de Trabalho

```
RE-01 Discovery → RE-02 Inspection → RE-03 Behavioral Analysis
      ↓                      ↓                      ↓
  Inventário            Mapa de componentes    Fluxos e comportamentos
      ↓                      ↓                      ↓
   RE-04 Specification → RE-05 Reconstruction → RE-06 Validation
      ↓                      ↓                      ↓
  Especificação         Implementação         Relatório de equivalência
  SDD                   independente           e segurança
```

### MCP Tool Layer — Integrações Disponíveis

| Ferramenta | Caso de Uso | Integração |
|------------|-------------|------------|
| **Ghidra** | Desassemblagem, decompilação, análise de funções | Python scripts → Ghidra scripting API |
| **Binwalk** | Identificação e extração de componentes de firmware | Python subprocess, hash validation |
| **Frida** | Instrumentação dinâmica, observação de comportamento | JavaScript payloads, runtime analysis |
| **Rizin/Cutter** | Análise estática e exploração de binários | Command-line interface, script output |
| **Playwright** | Inspeção comportamental de aplicações web | DOM analysis, network interception, screenshots |
| **Python** | Automação, validação, transformação de dados | Glue code, data processing, report generation |
| **Git** | Controle de evidências, versionamento de artefatos | Commit-based evidence tracking |
| **Filesystem controlado** | Ambiente de teste isolado | Sandbox execution, hash verification |

### Estrutura de Diretórios do Repositório

```
muirakitan-reverse-engineering/
├── .opencode/
│   ├── agents/
│   │   ├── discovery.md
│   │   ├── analysis.md
│   │   ├── security.md
│   │   └── specification.md
│   └── skills/
├── docs/
│   ├── discovery/
│   ├── architecture/
│   ├── api-analysis/
│   ├── security/
│   └── reconstruction/
├── specs/
│   ├── requirements/
│   ├── contracts/
│   └── acceptance/
├── evidence/
│   ├── screenshots/
│   ├── logs/
│   └── hashes/
├── src/
│   ├── agents/
│   ├── tools/
│   └── utils/
└── tests/
    ├── unit/
    ├── integration/
    └── behavioral/
```

### Políticas do Harness

1. **Isolamento de Ambiente**: Todas as execuções de engenharia reversa ocorrem em ambiente sandbox ou container isolado.
2. **Controle de Ferramentas**: O agente só tem acesso às ferramentas explicitamente autorizadas para a etapa corrente.
3. **Registro de Evidências**: Toda entrada, saída e operação deve ser registrada no diretório `evidence/`.
4. **Validação de Hash**: Hashes SHA-256 (não MD5) são usados para validar integridade de arquivos e resultados.
5. **Autorização Formal**: Nenhuma análise começa sem documento de escopo e autorização assinado (CONTEXT.md).
6. **Limite de Tempo**: Etapas com tempo máximo definido para evitar exploração prolongada de alvos.
7. **Revisão Humana**: Conclusões geradas por LLM passam por validação humana antes de serem consideradas definitivas.