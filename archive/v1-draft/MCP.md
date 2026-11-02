# Muirakitan RE — MCP Tool Layer

## Visão Geral

O **MCP (Model Control Protocol)** é a camada de integração entre os agentes especializados e as ferramentas de engenharia reversa. O MCP não é um agente e nem o motor de engenharia reversa — ele é o puente controlado que conecta modelos de linguagem a ferramentas especializadas com políticas de execução, limites e registro de evidências.

### Princípios Fundamentais

1. **MCP não decide — ele executa**: O MCP recebe comandos estruturados dos agentes e os encamina para as ferramentas apropriadas. As decisões estratégicas continuam a cargo dos agentes e do operador humano.

2. **Isolamento total**: Nenhuma ferramenta MCP tem acesso irrestrito ao ambiente host. Todas as execuções ocorrem em sandbox ou container isolado.

3. **Evidência em primeiro lugar**: Todo output de ferramenta MCP deve ser registrado no diretório `evidence/` com metadados completos antes de ser apresentado ao agente.

4. **Hash validation**: SHA-256 hashes são calculados para todo output significativo. MD5 é proibido para validação de autenticidade (apenas permitido para checksums de non-security purposes, e mesmo assim marcado como such).

5. **Timeout e límites**: Cada chamada MCP tem timeout definido no ROADMAP.md. Se expirar, o agente deve decidir por retry, skip ou redefinição de escopo.

---

## Ferramentas MCP Disponíveis

### 1. Ghidra Integration

| Campo | Especificação |
|-------|---------------|
| **Nome** | Ghidra |
| **Propósito** | Desassemblagem, decompilação, análise de funções, referências cruzadas e estrutura de binários |
| **Integração** | Python Scripts via Ghidra Scripting API |
| **Entrada** | Caminho para binário, endereço de entrada, nome de função alvo |
| **Saída** | Lista de funções desassembladas, decompilação C, grafo de referências cruzadas, strings extraídas |
| **Hash da Saída** | SHA-256 do arquivo de decompilação gerado |
| **Limites** | - Análise limitada a 20.000 funções por chamada<br>- Timeout máximo de 30 minutos por binário<br>- Sem acesso direto ao filesystem host (somente via volumes montados temporários) |
| **Políticas** | - Todas as funções analisadas devem ser catalogadas em `evidence/analysis/ghidra_{função}.c`<br>- Referências cruzadas devem ser validadas contra análise comportamental (Playwright/Frida)<br>- MD5 NÃO deve ser usado para autenticidade de resultados — usar SHA-256 |

#### Exemplo de Chamada MCP

```json
{
  "tool": "ghidra",
  "action": "analyze_binary",
  "parameters": {
    "binary_path": "/sandbox/binaries/firmware.img",
    "target_function": "sub_401000",
    "max_functions": 500
  },
  "sandbox": "mcp-ghidra-sandbox-01",
  "timeout_minutes": 30,
  "metadata": {
    "agent": "analysis",
    "etapa": "RE-02",
    "requires_hash_validation": true
  }
}
```

---

### 2. Binwalk Integration

| Campo | Especification |
|-------|----------------|
| **Nome** | Binwalk |
| **Propósito** | Identificação e extração de componentes de imagens de firmware |
| **Integração** | Python subprocess, parser de output |
| **Entrada** | Caminho para imagem de firmware |
| **Saída** | Lista de componentes extraídos, tipos de squashfs, ext4, etc., hash de componentes, offsets |
| **Hash da Saída** | SHA-256 do relatório de extração |
| **Limites** | - Extração limitada a 50 componentes por chamada<br>- Timeout máximo de 10 minutos<br>- Componentes extraídos vão para `evidence/firmware/extracted/` |
| **Políticas** | - Hashs SHA-256 de todos os componentes extraídos devem ser salvos<br>- Identificar assinaturas de firmware conhecido vs. proprietário<br>- Cruzar com informações de versões identificadas na Etapa RE-01 |

#### Exemplo de Chamada MCP

```json
{
  "tool": "binwalk",
  "action": "extract_firmware_components",
  "parameters": {
    "firmware_path": "/sandbox/firmware/router_fw.bin",
    "extract": true
  },
  "sandbox": "mcp-binwalk-sandbox-01",
  "timeout_minutes": 10,
  "metadata": {
    "agent": "discovery",
    "etapa": "RE-01",
    "requires_hash_validation": true
  }
}
```

---

### 3. Frida Integration

| Campo | Especificação |
|-------|----------------|
| **Nome** | Frida |
| **Propósito** | Instrumentação dinâmica para observar comportamento de aplicações em ambientes autorizados |
| **Integração** | JavaScript payloads, Node.js runtime |
| **Entrada** | PID ou nome de processo alvo, payload JavaScript |
| **Saída** | Logs de tempo real, traces de função, valores de variáveis em tempo real, hooks de retorno |
| **Hash da Saída** | SHA-256 dos logs capturados |
| **Limites** | - Instrumentação limitada a processo autorizado<br>- Timeout máximo de 15 minutos por sessão<br>- Nenhum payload que modifique fluxo de controle para fins maliciosos<br>- Todas as sessões devem ser registradas em `evidence/frida/{timestamp}.log` |
| **Políticas** | - Somente payloads de observação (print, hook return, trace)<br>- Nenhum attempt de bypass de segurança ou criptografia<br>- Se processo alvo encerrar anormalmente, registrar hash do estado no momento do crash |

#### Exemplo de Chamada MCP

```json
{
  "tool": "frida",
  "action": "observe_behavior",
  "parameters": {
    "target_process": "web-application",
    "payload": "console.log.interceptor.js"
  },
  "sandbox": "mcp-frida-sandbox-01",
  "timeout_minutes": 15,
  "metadata": {
    "agent": "analysis",
    "etapa": "RE-03",
    "requires_hash_validation": true
  }
}
```

---

### 4. Rizin / Cutter Integration

| Campo | Especificação |
|-------|----------------|
| **Nome** | Rizin / Cutter |
| **Propósito** | Análise estática e exploração de binários com interface gráfica e ferramentas complementares |
| **Integração** | Command-line interface (rizin), interface gráfica (cutter) |
| **Entrada** | Caminho para binário, comandos rizin |
| **Saída** | Resultados de análise estática, grafo de controle de fluxo, strings, hex dumps |
| **Hash da Saída** | SHA-256 do output de análise |
| **Limites** | - Análise limitada a binários de interesse do escopo<br>- Sem operações de escrita no binário original<br>- Timeout máximo de 20 minutos |
| **Políticas** | - Usar rizin para confirmação de findings do Ghidra (cross-validation)<br>- Resultados devem ser salvos em `evidence/rizin/{analysis_type}.txt`<br>- Cross-reference com Frida outputs quando possível |

#### Exemplo de Chamada MCP

```json
{
  "tool": "rizin",
  "action": "analyze statically",
  "parameters": {
    "binary_path": "/sandbox/binaries/app",
    "commands": ["aa", "axt", "Izj"]
  },
  "sandbox": "mcp-rizin-sandbox-01",
  "timeout_minutes": 20,
  "metadata": {
    "agent": "analysis",
    "etapa": "RE-02",
    "requires_hash_validation": true
  }
}
```

---

### 5. Playwright Integration

| Campo | Especificação |
|-------|----------------|
| **Nome** | Playwright |
| **Propósito** | Inspeção comportamental de aplicações web, automação de fluxos e regressão funcional |
| **Integração** | Node.js API, browser automation |
| **Entrada** | URL, seletores CSS/XPATH, ações de teclado/mouse |
| **Saída** | Capturas de tela, logs de rede, DOM após interações, vídeos de sessão, traces de performance |
| **Hash da Saída** | SHA-256 de captures e logs |
| **Limites** | - Apenas URLs e ações autorizadas no escopo<br>- Timeout por ação definido no ROADMAP.md<br>- Capturas vão para `evidence/playwright/{timestamp}/`<br>- GDPR/privacy compliance: mascarar dados pessoais em captures |
| **Políticas** | - Playwright é a ferramenta prioritária para validação comportamental (RE-03, RE-06)<br>- Todos os fluxos de teste devem ser idênticos entre original e reconstrução<br>- Se o Playwright encontrar comportamento inconsistente, documentar com grau de confiança e evidência |

#### Exemplo de Chamada MCP

```json
{
  "tool": "playwright",
  "action": "run_flow",
  "parameters": {
    "url": "https://example-saas.com/login",
    "actions": [
      {"type": "click", "selector": "#username"},
      {"type": "type", "selector": "#username", "value": "testuser"},
      {"type": "click", "selector": "#password"},
      {"type": "type", "selector": "#password", "value": "pass123"},
      {"type": "click", "selector": "//button[@type='submit']"}
    ]
  },
  "sandbox": "mcp-playwright-sandbox-01",
  "timeout_minutes": 10,
  "metadata": {
    "agent": "security",
    "etapa": "RE-03",
    "requires_hash_validation": true
  }
}
```

---

### 6. Python Integration

| Campo | Especificação |
|-------|----------------|
| **Nome** | Python |
| **Propósito** | Automação, validação, transformação de dados, scripts de apoio para todas as outras ferramentas |
| **Integração** | Python 3.11+ runtime, bibliotecas científicas e de análise |
| **Entrada** | Dados de entrada (JSON, arquivos, outputs de outras ferramentas) |
| **Saída** | Dados processados, relatórios, validações, transformações, gráficos |
| **Hash da Saída** | SHA-256 de arquivos de output generados |
| **Limites** | - Bibliotecas somente da whitelist aprovada pelo Orchestrator<br>- Sem acesso a redes externas exceto APIs documentadas<br>- Todo script Python deve ter metadados no header (autor, etapa, confianca) |
| **Políticas** | - Python é o "cola" que conecta todas as ferramentas MCP<br>- Scripts devem ser salvos em `src/utils/python/` com documentação inline<br>- Outputs que serão usados para conclusões de agente devem passar por validação cruzada com pelo menos uma outra ferramenta |

#### Exemplo de Chamada MCP

```json
{
  "tool": "python",
  "action": "process_evidence",
  "parameters": {
    "input": "evidence/discovery/tech-inventory.md",
    "operation": "extract_versions_and_hashes",
    "framework": "pandas"
  },
  "sandbox": "mcp-python-sandbox-01",
  "timeout_minutes": 5,
  "metadata": {
    "agent": "discovery",
    "etapa": "RE-01",
    "requires_hash_validation": true
  }
}
```

---

### 7. Git Integration

| Campo | Especificação |
|-------|----------------|
| **Nome** | Git |
| **Propósito** | Controle de evidências, versionamento de artefatos, rastreamento de mudanças |
| **Integração** | Comandos git padrão, porcelain scripts |
| **Entrada** | Repositório do projeto Muirakitan RE |
| **Saída** | Histórico de commits, diffs, tags, branches |
| **Hash da Saída** | SHA-256 do HEAD em cada commit |
| **Limites** | - Apenas o repositório do projeto muirakitan-reverse-engineering<br>- Tags de release para versões de methodology<br>- Nunca commit de dados sensíveis (usar .gitignore adequado) |
| **Políticas** | - Cada etapa concluída deve ter um commit associado na branch `etapas-re/{etapa}`<br>- Tags semanais `muirakitan-re-v{YYYYMMDD}`<br>- CHANGELOG automático a partir dos metadados dos commits |

#### Exemplo de Chamada MCP

```json
{
  "tool": "git",
  "action": "commit_evidence",
  "parameters": {
    "message": "RE-01 Discovery complete: tech inventory, 23 components identified, auth scope documented",
    "author": "orchestrator@muirakitan-re",
    "allow_empty": false
  },
  "sandbox": "mcp-git-sandbox-01",
  "metadata": {
    "agent": "orchestrator",
    "etapa": "RE-01",
    "requires_hash_validation": true
  }
}
```

---

## MCP Workflow Example

### Cenário: Análise de API REST

1. **Orchestrator** define objetivo em CONTEXT.md e inicia pipeline
2. **Discovery Agent** usa MCP-Git para versionamento e MCP-Python para parser de arquivos de configuração
3. **Analysis Agent** usa MCP-Ghidra para análise de implementação server-side e MCP-Playwright para comportamento de cliente
4. **Security Agent** usa MCP-Python com bancos CVE e MCP-Frida para observação de runtime
5. **Specification Agent** usa MCP-Python para gerar OpenAPI specs a partir de findings
6. **Orchestrator** valida todos os entregáveis e aprofunda para próxima etapa

Em cada etapa, o MCP garante:
- O agente solicita → MCP valida escopo → Ferramenta executa em sandbox → Output registrado com hash → Agente consome output → MCP registra metadata

### Erros e Exceptions

Se uma ferramenta MCP falhar:

1. **Timeout**: Agente decide retry (com backoff) ou skip para próxima sub-tarefa. Registrar motivo do timeout.
2. **Access Denied**: Agente documenta como "acesso restrito" e segue para abordagem alternativa. Não tentar contornar sandbox.
3. **Output Corrupto**: Hash validation falha → Descartar output, tentar novamente com parâmetros ajustados. Se persistir, sinalizar para revisão humana.
4. **Conflito de Findings**: Múltiplos agentes com graus de confiança diferentes → Documentar todas as perspectivas, atribuir grau de confiança individual, deixar conclusão final para operador humano.

### MCP e RAG (Retrieval-Augmented Generation)

O MCP também se integra ao RAG para:

1. **Recuperar documentação técnica** antes de iniciar análise (conhecimento prévio do domínio)
2. **Buscar patterns conhecidos** de vulnerabilidades ou arquiteturas antes de analisar alvo novo
3. **Validar findings** contra conhecimento documentado no repositório `docs/`
4. **Reduzir alucinações** do LLM usando evidências recuperadas do conhecimento institucional

O RACK (Retrieval-Augmented Code Knowledge) funciona assim:
- Antes de cada etapa principal, o Orchestrator consulta RAG para "patterns de análise de API REST" ou "patterns de desassemblagem de funções JavaScript"
- Os patterns recuperados são passados como contexto para os agentes
- Os agentes ainda devem validar contra evidências reais do alvo — patterns são auxiliares, não decisões

---

## Configuração de Segurança do MCP

### Variáveis de Ambiente Obrigatórias

```bash
# Diretórios sandbox
MUIRAKITAN_SANDBOX_DIR=/tmp/muirakitan-sandbox
MUIRAKITAN_EVIDENCE_DIR=/home/lobo/Área de trabalho/KODE/muirakitan-reverse-engineering/evidence

# Whitelist de ferramentas por agente
MUIRAKITAN_TOOLS_ALLOWED=ghidra,binwalk,frida,rizin,playwright,python,git

# Timeouts por etapa (minutos)
MUIRAKITAN_TIMEOUT_RE01=60
MUIRAKITAN_TIMEOUT_RE02=120
MUIRAKITAN_TIMEOUT_RE03=90
MUIRAKITAN_TIMEOUT_RE04=30
MUIRAKITAN_TIMEOUT_RE05=180
MUIRAKITAN_TIMEOUT_RE06=60

# Hash validation
MUIRAKITAN_REQUIRE_HASH=true
MUIRAKITAN_HASH_ALGO=sha256
```

### Políticas de Sandbox

- Cada ferramenta roda em container Docker com filesystem read-only exceto diretórios temporários designados
- Rede somente para domínios autorizados (definidos em CONTEXT.md)
- Processos filho não permitidos exceto aqueles necessários para a ferramenta
- Limite de memória: 2GB por ferramenta (configurável por etapa)
- Limite de CPU: 50% do núcleo disponível

### Rota de Escape de Emergência

Se uma ferramenta precisar de acesso que não está na whitelist:

1. Orchestrator avalia risco vs. benefício
2. Se crítico para conclusão da etapa, solicitar exceção por escrito (documento no repo)
3. Exceção só concedida se: (a) sem risco de danos ao ambiente host, (b) tempo limitado, (c) hash validation obrigatória antes e depois
4. Exceções são raras e devem ser documentadas em `evidence/exceptions/`