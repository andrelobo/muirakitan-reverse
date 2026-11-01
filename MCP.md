# MCP — Camada de ferramentas

## 1. Papel do MCP aqui

MCP é a **camada de integração** entre o modelo e as ferramentas.

- MCP **não** é o agente.
- MCP **não** é o motor de engenharia reversa.
- MCP **não** decide o que analisar.

Quem decide é o agente; quem executa é o servidor MCP; quem autoriza é o
operador. Misturar esses papéis produz automação sem controle.

## 2. Ferramentas priorizadas

| Ferramenta | Responsabilidade | Prioridade | Estado |
| --- | --- | --- | --- |
| Playwright | Inspeção comportamental de web/API, trace, HAR, regressão | muito alta | servidor oficial disponível |
| Python | Automação de análise, parsing, validação | alta | via shell, não precisa MCP |
| Git | Versionamento de artefatos | alta | via shell |
| Ghidra | Desassemblagem, decompilação, xrefs, estrutura de binário | alta | requer wrapper próprio |
| Binwalk | Identificação e extração de componentes de firmware | alta | requer wrapper próprio |
| Frida | Instrumentação dinâmica em ambiente autorizado | alta | requer wrapper próprio |
| Rizin / Cutter | Análise estática complementar, interface gráfica | média | requer wrapper próprio |
| filesystem | Leitura/escrita controlada | alta | nativo do harness |

**Observação honesta:** apenas Playwright tem servidor MCP oficial e mantido.
Ghidra, Binwalk, Frida e Rizin não têm MCP oficial. Para eles existem duas
opções:

1. **Fase 1 — shell:** o agente chama o CLI via shell com permissões restritas.
   Simples, funciona hoje, menos estruturado.
2. **Fase 2 — wrapper MCP:** servidor próprio expondo operações específicas
   (`analyze_function`, `extract_firmware`, `list_imports`). Melhor ergonomia e
   melhor controle de superfície.

O roadmap adota 1 → 2. Não construa wrapper antes de saber quais operações você
realmente repete.

## 3. Configuração

Em `opencode.jsonc` (formato V2, `mcp.servers`):

```jsonc
{
  "mcp": {
    "servers": {
      "playwright": {
        "type": "local",
        "command": ["npx", "-y", "@playwright/mcp@latest", "--headless", "--isolated"]
      }
    }
  }
}
```

Servidor remoto (exemplo de forma):

```jsonc
{
  "mcp": {
    "servers": {
      "nome": { "type": "remote", "url": "https://exemplo/mcp" }
    }
  }
}
```

Servidores remotos usam OAuth por padrão. Prefira OAuth a API key em texto.
Quando precisar de header, use substituição de ambiente: `{env:CHAVE}`.

### Adicionar pela CLI

```sh
opencode mcp add playwright --url https://exemplo/mcp
opencode mcp list
```

`mcp list` mostra o estado. Se indicar que precisa de autenticação, use `/mcps`
na interface — não rode `opencode mcp auth` por shell, o link de autorização pode
ficar oculto.

## 4. Uso por etapa

| Etapa | Ferramenta principal | O que se registra |
| --- | --- | --- |
| RE-01 Discovery | Playwright, `file`, `strings` | superfícies, tecnologias, entradas |
| RE-02 Inspection | leitura de manifesto, Ghidra/Rizin | componentes, dependências, versões |
| RE-03 Behavioral | Playwright (trace + HAR), cliente HTTP, Frida | fluxos, contratos observados, erros |
| RE-04 Specification | — | requisitos, contratos, aceitação |
| RE-05 Reconstruction | stack do cliente | implementação independente |
| RE-06 Validation | Playwright (regressão), testes de contrato | equivalência, divergências |

## 5. Regras de uso da camada MCP

1. **Uma ferramenta, um propósito.** Não exponha shell arbitrário como MCP.
2. **Menor superfície.** Habilite só os servidores da etapa atual.
3. **Toda saída vira evidência.** Resultado de ferramenta sem arquivo salvo e
   hash não conta.
4. **Nenhuma ferramenta fala com a internet sem necessidade.** Playwright aponta
   para o alvo isolado, não para o mundo.
5. **Nada de credencial em config.** Use `{env:...}` ou OAuth.
6. **Timeouts explícitos.** Ferramenta travada não pode travar a investigação.

## 6. Roadmap de integração

| Fase | Entrega |
| --- | --- |
| 1 | Playwright MCP ativo + Python/Git via shell |
| 2 | Wrapper MCP de Binwalk (`scan`, `extract`, `list`) |
| 3 | Wrapper MCP de Ghidra (`import`, `list_functions`, `decompile`, `xrefs`) |
| 4 | Wrapper MCP de Frida (`attach`, `list_modules`, `trace_call`) com alvo restrito a processo local autorizado |
| 5 | Rizin/Cutter sob demanda |

Cada wrapper deve recusar operação fora do diretório de trabalho do engajamento.
