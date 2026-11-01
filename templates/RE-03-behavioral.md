# RE-03 — Behavioral Analysis: <ALVO>

| Campo | Valor |
| --- | --- |
| Entrada | `docs/architecture/*` |
| Ambiente | <container/VM — nunca produção> |
| Data | |
| Executado por | `analysis` |

## 1. Inventário de endpoints

| Método | Caminho | Auth | Nível | Efeito colateral | Evidência |
| --- | --- | --- | --- | --- | --- |

Nível: `Observado` · `Inferido` · `Desconhecido`.

## 2. Contratos observados

### <MÉTODO> <caminho>

**Requisição**

```http
<exemplo real, redigido>
```

**Resposta de sucesso** — `<status>`

```json
<resposta real, redigida>
```

**Respostas de erro observadas**

| Status | Condição | Corpo | Evidência |
| --- | --- | --- | --- |

**Campos**

| Campo | Tipo observado | Obrigatório | Observação | Confiança |
| --- | --- | --- | --- | --- |

## 3. Fluxos

### FLOW-001 — <nome>

| Campo | Valor |
| --- | --- |
| Ator | |
| Pré-condição | |
| Passos | |
| Pós-condição | |
| Caminho de erro | |
| Evidência | |

```mermaid
<sequência>
```

## 4. Máquinas de estado

### <entidade>

| Estado | Evento | Próximo estado | Observação |
| --- | --- | --- | --- |

## 5. Regras de negócio observadas

| # | Regra | Onde foi observada | Confiança | Evidência |
| --- | --- | --- | --- | --- |

> Inclua as que parecem bug. Comportamento estranho é requisito do sistema real.

## 6. Comportamento inconsistente

| # | O que se esperava | O que aconteceu | Reproduzível? | Evidência |
| --- | --- | --- | --- | --- |

## 7. Critério de saída

- [ ] Cada fluxo documentado é reproduzível a partir deste documento.
- [ ] Todo endpoint tem nível declarado.
- [ ] Campos desconhecidos estão marcados, não preenchidos.

## 8. Handoff

```md
## Handoff RE-03 → RE-04
**Produzido:**
**Critério de saída:**
**Confiança geral:**
**Pendências:**
**Próximo passo sugerido:**
```
