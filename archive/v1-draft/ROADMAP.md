# Muirakitan RE — Roadmap de Implementação

## Visão Geral

Este roadmap define a implementação incremental do motor Muirakitan RE em 30 dias, dividido em 5 fases de 1 semana cada. O foco é construir capacidades funcionais a partir de projetos-piloto, não teoria abstrata.

---

## Fase 1: Dias 1–5 — Ambiente e Ferramentas

### Objetivo
Instalar, configurar e testar todas as ferramentas de engenharia reversa em ambiente Linux isolado.

### Tarefas Principais

| Dia | Tarefa | Resultado Esperado |
|-----|--------|-------------------|
| 1-2 | Instalar Linux (Ubuntu 22.04 ou Debian 12) em máquina virtual ou hardware dedicado | Sistema base operacional |
| 3 | Instalar e configurar Ghidra (última versão estável) | Ghidra funcionando, scripting API testado |
| 4 | Instalar e configurar Binwalk | Extração de componentes de firmware testada |
| 5 | Instalar Frida, Rizin/Cutter, Playwright | Todas as ferramentas instaladas e comunicação verificada |

### Critérios de Conclusão da Fase 1

- [ ] Ambiente Linux isolado operacional
- [ ] Ghidra consegue analisar um binário de teste e gerar decompilação
- [ ] Binwalk consegue extrair componentes de uma imagem de firmware de teste
- [ ] Frida pode instrumentar um processo de teste e capturar traces
- [ ] Playwright pode abrir um navegador e navegar a uma URL
- [ ] Docker sandbox configurado com políticas de isolation básicas
- [ ] Pipeline de hash validation (SHA-256) funcionando

### Entregáveis

- `.opcode/config/` com configurações de sandbox
- `evidence/hashes/` com exemplos de cálculo de hash
- `sandbox/test-binary/` com binários de teste
- `sandbox/firmware-test/` com imagens de firmware de teste

---

## Fase 2: Dias 6–10 — MCP Integração

### Objetivo
Integrar ferramentas ao OpenCode, definir agentes especializados e políticas de execução.

### Tarefas Principais

| Dia | Tarefa | Resultado Esperado |
|-----|--------|-------------------|
| 6 | Definir schema MCP no formato JSON (definido em MCP.md) | Schema versionado e salvo |
| 7 | Integrar ferramentas básicas (Ghidra, Binwalk) ao OpenCode harness | Chamadas MCP funcionando dentro de sandbox |
| 8 | Definir políticas do harness (permissões por etapa, timeouts) | Arquitetura de permissões operacional |
| 9 | Implementar middleware de hash validation entre ferramentas | Hash calculation e verification automática |
| 10 | Testar pipeline end-to-end: Discovery Agent → MCP → Output → Hash | Pipeline funcional de ponta a ponta |

### Critérios de Conclusão da Fase 2

- [ ] Schema MCP versionado e armazenado
- [ ] OpenCode consegue chamar ferramentas via protocolo MCP
- [ ] Politicas de permissões por etapa definidas e testadas
- [ ] Hash validation automática entre stages funcionando
- [ ] Pipeline básico Discovery → Output → Hash salvo em evidence
- [ ] Documentação das chamadas MCP executadas

### Entregáveis

- `MCP.md` (já criado — versões iterativas)
- `.opcode/harness/` com políticas de execução
- `evidence/mcp-tests/` com logs de chamadas MCP de teste
- `scripts/mcp-wrapper.sh` wrapper que valida hash antes/after

---

## Fase 3: Dias 11–15 — SDD Templates

### Objetivo
Criar templates de discovery, arquitetura, contratos, requisitos e evidências.

### Tarefas Principais

| Dia | Tarefa | Resultado Esperado |
|-----|--------|-------------------|
| 11 | Criar template `CONTEXT.md` (visão e objetivos) | Template padronizado |
| 12 | Criar template `ARCHITECTURE.md` (arquitetura do engine) | Template de arquitetura com camadas tecnológicas |
| 13 | Criar template `METHODOLOGY.md` (metodologia Muirakitan RE) | Etapas RE-01 a RE-06 definidas |
| 14 | Criar template `AGENTS.md` (regras de operação dos agentes) | Regras e graus de confiança definidos |
| 15 | Criar templates `MCP.md` e `SECURITY.md` | Integrações e guardrails definidos |

### Critérios de Conclusão da Fase 3

- [ ] Todos os 7 templates SDD criados e testados com dados de exemplo
- [ ] Templates validados por Operator humano (pelo menos 1 revisão cada)
- [ ] Templates versionados no Git com mensagens claras
- [ ] Exemplos populados com dados de um projeto-piloto (próxima fase)
- [ ] Templates conseguem ser preenchidos por agentes em formato JSON consistente

### Entregáveis

- `specs/requirements/` com templates preenchidos
- `specs/contracts/` com contratos de API de exemplo
- `specs/acceptance/` com critérios de aceitação definidos
- `.opcode/agents/` com arquivos de definição de agentes

---

## Fase 4: Dias 16–23 — Projeto-Piloto

### Objetivo
Escolher uma aplicação própria ou um projeto open source e executar o pipeline completo da metodologia Muirakitan RE.

### Projeto-Piloto Recomendado

Uma aplicação SaaS open source com:
- Frontend (React/Vue/Angular)
- Backend (Node.js/Python/Go)
- Documentação parcial (alguns endpoints documentados)
- Deploy testável localmente

### Exemplos Sugeridos

1. **TodoList API** — simplista, mas cobre CRUD, autenticação, banco de dados
2. **WordPress (versão recente)** — cobertura de CMS, plugins, API REST
3. **GitList ou Gitea** — ferramentas de código com APIs complexas
4. **Generic open source SaaS** — escolha da comunidade

### Tarefas Principais

| Etapa | Atividade | Métricas |
|-------|-----------|----------|
| RE-01 Discovery | Inventário tecnológico, pontos de entrada, versões | 30+ componentes identificados, fingerprint de versões |
| RE-02 Inspection | Contratos API, modelo de dados, interfaces | 80%+ endpoints com contrato OpenAPI, modelo de dados > 80% documentado |
| RE-03 Behavioral Analysis | Fluxos de negócio, máquinas de estado, workflows | 5+ fluxos principais documentados, 3+ cenários de teste por fluxo |
| RE-04 Specification | SDD templates preenchidos, contratos formais | Todos os templates preenchidos, OpenAPI spec gerada |
| RE-05 Reconstruction | Implementação alternativa (NestJS/React/MongoDB) | Aplicação funcional, 70%+ fluxos principais operando |
| RE-06 Validation | Relatório de equivalência, métricas de confiança | Relatório completo com todas as métricas preenchidas |

### Critérios de Conclusão da Fase 4

- [ ] Pipeline completo RE-01 a RE-06 executado em projeto-piloto
- [ ] Pelo menos 50% das funcionalidades principais documentadas (RE-01 a RE-04)
- [ ] Reconstrução funcional executando (RE-05)
- [ ] Relatório de equivalência com métricas preenchidas (RE-06)
- [ ] Pelo menos 3 inconsistências identificadas entre original e reconstrução
- [ ] Pelo menos 70% dos testes de comportamento aprovados

### Entregáveis

- `evidence/discovery/` - resultados da etapa Discovery
- `evidence/inspection/` - resultados da etapa Inspection
- `evidence/behavioral/` - resultados da etapa Behavioral Analysis
- `specs/` - todos os SDDs preenchidos
- `src/` - código da reconstrução
- `tests/` - testes automatizados
- `reports/equivalence-report.md` - relatório final
- `reports/security-audit.md` - auditoria de segurança

---

## Fase 5: Dias 24–30 — Commercialização

### Objetivo
Produzir demonstração, relatório de diagnóstico, estudo de caso e proposta comercial.

### Tarefas Principais

| Dia | Tarefa | Resultado Esperado |
|-----|--------|-------------------|
| 24-25 | Consolidar todos os artefatos do projeto-piloto | Repositório completo, consistente e documentado |
| 26 | Produzir demonstração guiada do motor Muirakitan RE | Demo script funcional (15-20 min) |
| 27 | Gerar relatório de diagnóstico do projeto-piloto | Diagnóstico técnico completo com métricas |
| 28 | Estudar caso de uso (case study) — what worked, what didn't | Lições aprendidas documentadas |
| 29 | Desenvolver proposta comercial (3 ofertas) | Estrutura de pricing e posicionamento |
| 30 | Revisão final e preparação para primeira venda/engajamento | Materiais prontos para prospectar |

### Ofertas para Commercialização (definidas no texto original)

1. **Legacy System Intelligence** — Diagnóstico técnico de sistemas existentes
   - Inventário tecnológico
   - Mapeamento de dependências
   - Documentação de APIs
   - Identificação de riscos
   - Plano de modernização

2. **AI-Assisted Software Reconstruction** — Reconstrução de aplicações com base em requisitos e comportamentos observados
   - Reverse engineering funcional
   - Especificação SDD
   - Nova arquitetura
   - Desenvolvimento e testes
   - Migração gradual

3. **AI Security Assessment** — Avaliação de segurança assistida por agentes
   - Análise estática
   - Dependências vulneráveis
   - Configurações inseguras
   - Análise de APIs
   - Relatório técnico e recomendações

### Critérios de Conclusão da Fase 5

- [ ] Demo funcional pronto (pode ser apresentado a potenciais clientes)
- [ ] Relatório de diagnóstico completo com todas as métricas
- [ ] Case study com resultados mensuráveis (tempo, cobertura, taxa de sucesso de testes)
- [ ] Proposta comercial estruturada com 3 ofertas progressivas
- [ ] Preço definido por oferta (baseado em esforço-horas e complexidade)
- [ ] Primeiros materiais de prospectagem prontos

### Entregáveis Finais

- `CONTEXT.md` - visão e objetivos do negócio
- `ARCHITECTURE.md` - arquitetura do engine (para incluir na proposta)
- `METHODOLOGY.md` - metodologia comprovada pelo projeto-piloto
- `AGENTS.md` - regras de operação (transparência para cliente)
- `MCP.md` - ferramentas e integrações (quais se usam, por quê)
- `SECURITY.md` - autorização, isolamento e guardrails (reassurance para cliente)
- `ROADMAP.md` - implementação incremental (planejamento de próximos ciclos)
- `DEMO_SCRIPT.md` - script da demonstração guiada
- `PROPOSAL.md` - proposta comercial estruturada
- `CASE_STUDY.md` - estudo de caso do projeto-piloto

---

## Visão Completa do Roadmap

```
Dias 1-5:   Ambiente e Ferramentas (infraestrutura)
Dias 6-10:  MCP Integração (conectar modelo a ferramentas)
Dias 11-15: SDD Templates (formalizar conhecimento)
Dias 16-23: Projeto-Piloto (aplicar em caso real)
Dias 24-30: Commercialização (embalhar e oferecer)
```

### Marco de Sucesso a 30 Dias

| Métrica | Meta | Como Medir |
|---------|------|------------|
| Tempo de setup do ambiente | < 5 dias | Data do primeiro commit do ambiente |
| Cobertura de ferramentas | 100% (Ghidra, Binwalk, Frida, Playwright) | Checklist de funcionalidades mínimas |
| Pipeline MCP funcional | 100% das chamadas básicas funcionando | Testes automatizados de MCP |
| SDD templates prontos | 100% (7 templates) | Validação por Operator humano |
| Projeto-piloto completado | Pelo menos 50% das métricas de sucesso | Relatório RE-06 preenchido |
| Materiais de comercialização | 100% (7 documents + demo) | Todos os arquivos no lugar |
| Proposta comercial | 3 ofertas definidas com precos | Documentos assinados/preenchidos |

### Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Ferramenta não compatível com ambiente | Média | Alta | Ter containers Docker como isolamento; usar versões estáveis |
| Projeto-piloto muito complexo para 8 dias | Alta | Média | Escolher projeto com escopo controlado (TodoList API ou similar) |
| LLM alucina conclusões sem evidência | Alta | Alta | Politica de "evidência sobre suposição" + graus de confiança + revisão humana gate |
| Falta de autorização do "cliente" (mesmo que interno) | Média | Alta | Criar CONTEXT.md interno com escopo definido antes de começar |
| Hash validation falha repetidamente | Baixa | Média | Scripts de teste antes de iniciar; usar ferramentas padrão SHA-256 |
| Operador humano não disponível para gate | Média | Alta | Agendar revisões com antecedência; documentar blocos que exigem revisão |