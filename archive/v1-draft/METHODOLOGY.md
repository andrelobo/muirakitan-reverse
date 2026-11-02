# Muirakitan RE — Metodologia Operacional

A metodologia Muirakitan RE define seis etapas operacionais, cada uma com entregáveis específicos e requisitos de evidência. A progressão é sequencial, mas etapas podem ser iterativas quando descobertas exigem reanálise.

---

## Etapa RE-01: Discovery

### Objetivo
Inventário completo do sistema alvo — tecnologia stack, componentes, versões, dependências e pontos de entrada.

### Entregáveis

| Artefato | Descrição |
|----------|-----------|
| `tech-inventory.md` | Lista completa de tecnologias identificadas (linguagem, framework, banco de dados, servidor, bibliotecas) |
| `component-map.md` | Mapa hierárquico de componentes do sistema (frontend, backend, serviços auxiliares, integrações externas) |
| `dependency-graph.md` | Grafo de dependências entre módulos, bibliotecas e serviços externos |
| `entry-points.md` | Todos os pontos de entrada identificados (rotas API, endpoints, interfaces, interfaces de linha de comando) |
| `version-fingerprint.md` | Fingerprints de versão de cada componente (headers de resposta, mensagens de erro, números de versão expostos) |
| `authorizacao-scope.md` | Documento de escopo e autorização formal (assinado pelo cliente/solicitante) |

### Ferramentas e Técnicas

- Análise de arquivos de configuração (package.json, requirements.txt, pom.xml, etc.)
- HEAD requests e headers de resposta
- Git history analysis (se tiver acesso público/acesso controlado)
- Verificação de endpoints famosos /well-known
- Digital fingerprint de serviços conhecidos

### Critérios de Conclusão

- [ ] Pelo menos 90% dos componentes identificados e catalogados
- [ ] Pelo menos 80% dos pontos de entrada mapeados
- [ ] Documento de autorização e escopo preenchido e assinado
- [ ] Grafo de dependências preliminar gerado

---

## Etapa RE-02: Inspection

### Objetivo
Mapear componentes individuais, interfaces e fluxos de dados entre eles.

### Entregáveis

| Artefato | Descrição |
|----------|-----------|
| `api-contracts.md` | Contratos de API identificados (métodos, parâmetros, tipos de retorno, códigos de status) |
| `data-model.md` | Modelos de dados em uso (tabelas, esqumas, estruturas de mensagem) |
| `interface-map.md` | Mapeamento de todas as interfaces (APIs, bancos de dados, mensageries, arquivos) |
| `flow-diagrams.md` | Diagramas de fluxo de dados principais (processos de negócio, solicitações, respostas) |
| `configuration-map.md` | Mapeamento de configurações críticas (rotas, segredos, certificados, timeouts) |
| `error-handling-map.md` | Como o sistema lida com erros, exceções e casos de borda |

### Ferramentas e Técnicas

- Playwright: interceptação de rede, captura de payloads/respostas
- Ghidra: desassemblagem de funções relevantes, análise de strings
- Frida: instrumentação dinâmica para observar comportamento em tempo real
- Python: extração e transformação de dados de logs e respostas
- Análise de documentos de API (OpenAPI, Swagger, Postman collections) — se existirem

### Critérios de Conclusão

- [ ] Contratos de API documentados para pelo menos 80% dos endpoints identificados
- [ ] Modelo de dados completo ou maioritário documentado
- [ ] Diagramas de fluxo de dados dos processos principais de negócio
- [ ] Mapa de configurações críticas preenchido

---

## Etapa RE-03: Behavioral Analysis

### Objetivo
Observar e documentar comportamentos do sistema — fluxos de negócio, regra de negócio, estados de transição.

### Entregáveis

| Artefato | Descrição |
|----------|-----------|
| `business-rules.md` | Regras de negócio identificadas (validações, cálculos, condições, aprovações) |
| `state-machines.md` | Máquinas de estado do sistema (estados, transições, gatilhos) |
| `workflow-specs.md` | Especificações de workflows (ordenação de passos, responsáveis, condições de conclusão) |
| `integration-flows.md` | Como o sistema interage com serviços externos (pagamentos, autenticação, terceiros) |
| `performance-characteristics.md` | Características de performance observadas (tempos de resposta, tamanhos de lote, limites de taxa) |
| `test-scenarios.md` | Cenários de teste que cobrem fluxos principais e de borda |

### Ferramentas e Técnicas

- Playwright: automação de fluxos completos, captura de comportamento
- Testes de integração automatizados
- Instrumentação com Frida para observar pontos específicos de execução
- Análise de logs de produção (se disponível em ambiente de teste)
- Scenarios de fuzzing para descobrir comportamentos inesperados

### Critérios de Conclusão

- [ ] Regras de negócio principais documentadas
- [ ] Máquinas de estado dos fluxos críticos mapeadas
- [ ] Pelo menos 3 cenários de teste por fluxo principal gerados
- [ ] Características de performance documentadas para fluxos principais

---

## Etapa RE-04: Specification

### Objetivo
Traduzir todas as evidências em especificações técnicas formais usando o framework SDD (Software Design Documents).

### Entregáveis

| Artefato | Descrição |
|----------|-----------|
| `requirements/requirements.md` | Requisitos funcionais e não funcionais (últimos, claros, verificáveis) |
| `contracts/api-contracts.md` | Contratos de API formais (OpenAPI/Specification format) |
| `architectural/architecture.md` | Documentação de arquitetura geral (padrões, estruturas, componentes) |
| `specs/database-specs.md` | Especificação do modelo de banco de dados (esquemas, relações, migrações) |
| `specs/acceptance-criteria.md` | Critérios de aceitação para reconstrução (o que deve ser idêntico ao original) |
| `specs/technical-specifications.md` | Especificações técnicas detalhadas (endpoints, formatos, protocolos) |

### Ferramentas e Técnicas

- Templates SDD pré-definidos
- OpenAPI/Swagger specification generation
- Modelos de requisitos (Given-When-Then, user stories, casos de uso)
- Documentação de arquitetura baseada em componentes
- Validação cruzada entre múltiplas fontes de evidência

### Critérios de Conclusão

- [ ] Todos os artefatos SDD gerados e revisados
- [ ] Contratos de API em formato máquina-leitur (OpenAPI/YAML) disponíveis
- [ ] Critérios de aceitação definidos com nível de confiança atribuído
- [ ] Documentação pronta para ser usada como base para reconstrução

---

## Etapa RE-05: Reconstruction

### Objetivo
Implementar uma versão independente do sistema com base nas especificações geradas, sem copiar código do original.

### Entregáveis

| Artefato | Descrição |
|----------|-----------|
| `src/application/` | Código-fonte da reconstrução (arquitetura escolhida: NestJS/React/MongoDB ou stack similar) |
| `tests/behavioral-tests.md` | Testes de comportamento que validam equivalência com o original |
| `tests/integration-tests.md` | Testes de integração que verificam funcionalidades completas |
| `docs/reconstruction-guide.md` | Guia de como a reconstrução foi feita (decisões de arquitetura, mapeamentos) |
| `specs/migration-plan.md` | Plano de migração do original para a reconstrução (se aplicável) |
| `evidence/reconstruction-comparison.md` | Comparação detalhada entre original e reconstrução |

### Decisões de Arquitetura

- **Backend**: NestJS (TypeScript) — aproveita experiência do escopo, tipagem segura, modularidade
- **Frontend**: React — ecossistema amplo, compatibilidade com Playwright tests
- **Banco de Dados**: MongoDB — flexibilidade para modelos de dados descobertos durante análise
- **API Gateway**: Portas padrão, middleware de autenticação e validação
- **Deploy**: Docker containers — isolamento consistente com política de harness

### Critérios de Conclusão

- [ ] Aplicação funcional executando localmente
- [ ] Pelo menos 70% dos fluxos de negócio principais operando identicamente
- [ ] Testes automatizados passando para os cenários críticos
- [ ] Documentação de decisões de arquitetura documentada

---

## Etapa RE-06: Validation

### Objetivo
Produzir relatório final de equivalência e segurança, comparando comportamento da reconstrução com o sistema original.

### Entregáveis

| Artefato | Descrição |
|----------|-----------|
| `reports/equivalence-report.md` | Relatório de equivalência comportamental (o que foi validado, grau de confiança) |
| `reports/security-audit.md` | Relatório de auditoria de vulnerabilidades na reconstrução |
| `evidence/hash-comparison.md` | Comparação de hashes (SHA-256) de inputs/outputs críticos |
| `reports/gaps-identification.md` | Inconsistências e gaps identificados entre original e reconstrução |
| `reports/recommendations.md` | Recomendações para produção, migração ou novos ciclos de engenharia reversa |
| `executive/summary.md` | Resumo executivo para stakeholders não-técnicos |

### Métricas de Validação

| Métrica | Descrição | Meta |
|---------|-----------|------|
| `cobertura-functional` | Percentual de funcionalidades principais que se comportam idêntico | >= 80% |
| `taxa-de-sucesso-testes` | Percentual de testes automatizados que aprovam | >= 85% |
| `grau-de-confiança` | Avaliação agregada de confiança nas conclusões | Documentado por agente |
| `inconsistencias-count` | Número de inconsistências identificadas | Quantificado com explicação |
| `tempos-reconstrucao` | Tempo gasto na reconstrução comparado ao desenvolvimento convencional | Relativo, com benchmark |

### Critérios de Conclusão

- [ ] Relatório de equivalência completo com todas as métricas preenchidas
- [ ] Auditoría de segurança realizada (pelo menos análise estática de dependências)
- [ ] Recomendações documentadas para próximos passos (manutenção, migração, novo ciclo)
- [ ] Revisão humana de todas as conclusões de LLM concluída

### Fechamento de Ciclo

- [ ] Todos os artefatos persistentes salvos no repositório
- [ ] Levantamento de lições aprendidas documentado
- [ ] Próximo ciclo de engenharia reversa planejado (se aplicável)
- [ ] Repositório arquivado ou transferido conforme acordado com cliente/stakeholders