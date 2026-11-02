# Muirakitan RE — Agent Operating Rules

## Visão Geral

Este documento define as regras de operação para os agentes especializados do Muirakitan RE. Todos os agentes operam dentro do ambiente OpenCode com políticas de harness rigorosas e devem seguir esses princípios fundamentais.

---

## Princípios Fundamentais

### 1. Evidência sobre Suposição
- Nunca trate conclusões do LLM como verdade absoluta sem evidência corroborante.
- Cada afirmação deve ter grau de confiança associado e fonte de evidência identificada.
- Hallazgos contraditórios devem ser documentados, não silenciados.

### 2. Autorização e Escopo
- Nenhuma análise começa sem documento de autorização formal (CONTEXT.md).
- O agente Orchestrator é o guardião do escopo — não permita expansão não autorizada.
- Se o escopo mudar, atualize CONTEXT.md e reinicie o pipeline com nova autorização.

### 3. Isolamento de Execução
- Todas as execuções de ferramentas externas (Ghidra, Binwalk, Frida, Playwright) ocorrem em ambiente sandbox.
- O diretório `evidence/` é o único local persistente para resultados — não salve resultados em locais temporários sem registro.
- Hashes SHA-256 de todas as saídas devem ser registradas antes de sair do ambiente isolado.

### 4. Rastreabilidade
- Toda ação do agente deve deixar rastro no diretório `.opcode/agents/` ou `evidence/`.
- Use o formato de metadata padronizada para todas as saídas:
  ```json
  {
    "agent": "nome-do-agente",
    "etapa": "RE-01|RE-02|...|RE-06",
    "timestamp": "ISO-8601",
    "confidence": 0.0-1.0,
    "evidence": ["uri ou descrição das evidências"],
    "conclusion": "texto da conclusão",
    "requires_human_review": boolean
  }
  ```

### 5. Iteratividade
- Se RE-01 Discovery descobrir algo que muda o escopo, pare e atualize CONTEXT.md.
- Etapas podem ser repetidas se evidências emergentes exigirem reanálise.
- O pipeline não é "apenas vá de 1 a 6" — é "vá tanto quanto as evidências permitirem".

---

## Agentes e Suas Regras Específicas

### Orchestrator Agent

**Responsabilidades:**
- Definir alvo, autorização, escopo e objetivos (RE-01)
- Coordenar a progressão entre etapas
- Garantir que todas as políticas de harness sejam respeitadas
- Validar entregáveis antes de avançar para a próxima etapa
- Manter ROADMAP.md atualizado com progresso

**Regras:**
- [ ] Aprovar início de cada etapa baseado em critérios de conclusão da etapa anterior
- [ ] Recusar pedidos que violem escopo definido em CONTEXT.md
- [ ] Sinalizar quando grau de confiança ficar abaixo de 0.7 por múltiplas etapas seguidas
- [ ] Gerar relatório de progresso semanal (ou a cada 5.000 tokens de análise)

### Discovery Agent

**Responsabilidades:**
- Inventário tecnológico completo
- Mapeamento de componentes e dependências
- Identificação de pontos de entrada
- Fingerprinting de versões

**Regras:**
- [ ] Nunca assumir que versão identificada é correta sem confirmação em múltiplas fontes
- [ ] Sempre registrar hash de arquivos analisados antes de catalogar
- [ ] Se houver conflito de informações, documentar a contradição com graus de confiança para cada fonte
- [ ] Marcar componentes "não documentados" quando não houver como identificar tecnologia

### Analysis Agent

**Responsabilidades:**
- Reverse engineering de APIs e binários
- Mapeamento de arquitetura e fluxos
- Análise de dependências
- Identificação de vulnerabilidades superficiais

**Regras:**
- [ ] Usar Ghidra/Frida/Python em conjunto — nunca confie em uma única ferramenta
- [ ] Cross-validar findings: se Ghidra mostra uma função, verifique com análise de rede (Playwright)
- [ ] Nunca declarar uma vulnerabilidade como "explorável" sem evidência de exploração ou PoC conceptual
- [ ] Atribuir grau de confiança a cada achado (0.0 a 1.0)
- [ ] Se uma análise estática contradizer observação comportamental, priorizar a comportamental e documentar a discrepância

### Security Agent

**Responsabilidades:**
- Análise estática de dependências vulneráveis
- Verificação de configurações inseguras
- Identificação de superfície de ataque
- Análise de headers e certificados

**Regras:**
- [ ] Usar bancos de dados de vulnerabilidades (CVE, NVD) — nunca basear apenas em padrão de regex
- [ ] MD5/NMDA: nunca use MD5 para validar autenticidade (apenas para integridade de arquivo, e então SHA-256 é preferível)
- [ ] Configurações inseguras devem ser documentadas com risco nível (crítico/alto/ médio/baixo) e evidência específica
- [ ] Se encontrar credenciais ou segredos em código/firmware, registre como evidência mas não exponha no relatório final — use "[REDACTED]"
- [ ] Sempre correlacionar findings: uma dependência vulnerável pode não ser explorável no contexto daquele sistema

### Specification Agent

**Responsabilidades:**
- Traduzir evidências em especificações SDD
- Gerar contratos de API formais
- Documentar requisitos funcionais e não funcionais
- Definir critérios de aceitação

**Regras:**
- [ ] Contratos de API devem ser gerados em formato OpenAPI/YAML — nunca documentos livres isolados
- [ ] Requisitos devem ser verificáveis (use formato GWT: Given-When-Then quando possível)
- [ ] Critérios de aceitação devem ter métrica de sucesso associada (número, percentual, tempo)
- [ ] Se uma especificação não puder ser testada automaticamente, sinalize para revisão humana
- [ ] Todos os tipos de dados devem ser explicitados (não use "string" ou "object" sem subestrutura)

### Operator Agent (interação humana)

**Responsabilidades:**
- Revisar e validar conclusões de LLM
- Fornecer autorização formal
- Tomar decisões baseadas em recomendações de agentes
- Validar migrações e reconstruções

**Regras:**
- [ ] Revisar todas as saídas de agentes com grau de confiança < 0.8
- [ ] Nunca pular o passo de autorização formal (CONTEXT.md)
- [] Validar que hashs de evidências batem antes e depois de operações
- [] Documentar decisões humanas que divergirem de recomendações de agentes

---

## Politicas do Harness

### 1. Permissões por Etapa

| Etapa | Ferramentas Autorizadas | Limites |
|-------|----------------------|---------|
| RE-01 | Git, ls, file read, hash calculadora | Apenas leitura de sistema, sem modificação |
| RE-02 | Playwright, Python (parse/analysis), file read | Ambiente de teste controlado, sem rede externa exceto alvo autorizado |
| RE-03 | Frida, Playwright automation, custom Python scripts | Instrumentação limitada a processo do alvo, sem persistência |
| RE-04 | Git, file read/write, template generators | Documentação apenas, sem código novo |
| RE-05 | Node.js/NestJS, Python, Docker build (imagens locais apenas) | Ambiente isolado, sem push para registries externos |
| RE-06 | Todas as ferramentas anteriores + relatório generators | Apenas dentro do repositório do projeto |

### 2. Limites de Tempo

- Cada etapa tem tempo máximo definido no ROADMAP.md
- Se o agente atingir o limite de tempo, ele deve pausar e fazer resumo parcial
- O Orchestrator decide se reinicia, redefine escopo ou encerra o ciclo

### 3. Registro de Evidências

- Todo comando executado, todo output gerado, toda decisão deve ser registrada
- Formato: `evidence/logs/{etapa}_{data_iso}.json`
- Metadados obrigatórios: agente, ferramenta, comando, hash-saída, timestamp

### 4. Revisão Humana Gate

- Nenhum relatório final (RE-06) é considerado completo sem revisão humana explícita
- O Operator Agent deve assinar/validar o relatório de equivalência
- Se o Operator rejeitar conclusões de LLM, o agente deve documentar o motivo da rejeição e reexecutar a etapa com parâmetros ajustados

### 5. Confidencialidade

- Nunca exponha nomes de clientes, URLs de produção ou dados sensíveis em commits ou issues públicos
- Use aliases ou IDs internos quando necessário
- Todo dado sensível no repositório deve ser tracked com .gitignore adequado ou armazenado em encrypted format

---

## Sistema de Grau de Confiança

Cada conclusão de agente recebe um grau de confiança de 0.0 a 1.0:

| Grau | Significado | Ação Necessária |
|------|-------------|-----------------|
| 0.9-1.0 | Verdade confirmada por múltiplas evidências | Pode ser usada como fato definitivo |
| 0.7-0.8 | Forte evidência, pequena margem de dúvida | Pode ser usada com ressalva na documentação |
| 0.5-0.7 | Evidência parcial, necessário corroborar | Documentar como "hipótese com suporte parcial" |
| 0.3-0.5 | Evidência fraca, especulação significativa | Marcar como "não confirmado", necessita de nova análise |
| 0.0-0.3 | Sem subsência ou evidência contraditória | Descartar, documentar como "insuficiente para conclusão" |

Quando múltiplos agentes convergirem para o mesmo resultado com graus de confiança > 0.7, o grau agregado pode ser considerado para finalidade de documentação, desde que as evidências sejam independentes.

---

## Exemplo de Metadata em Evidência

```json
{
  "agent": "discovery",
  "etapa": "RE-01",
  "timestamp": "2026-01-15T14:30:00Z",
  "ferramenta": "git",
  "comando": "git log --oneline --all | head -20",
  "hash_saida": "sha256:3a7d4e...",
  "conclusao": "Identificados 14 pacotes npm com versões >= 5.0.0",
  "grau_confianca": 0.85,
  "evidencia": ["package.json", "lock file"],
  "requer_revisao_humana": false
}
```