# RE-02 — Inspection: <ALVO>

| Campo | Valor |
| --- | --- |
| Entrada | `docs/discovery/*` |
| Data | |
| Executado por | `analysis` |

## 1. Mapa de componentes

```
<diagrama em texto ou Mermaid>
```

| # | Componente | Tipo | Responsabilidade | Fronteira de confiança |
| --- | --- | --- | --- | --- |
| 1 | | serviço / módulo / biblioteca / processo | | |

## 2. Dependências

| Pacote | Versão | Origem | Mantida? | Risco | Evidência |
| --- | --- | --- | --- | --- | --- |

Classificação: `mantida` · `desatualizada` · `abandonada` · `fork não rastreado`.

## 3. Acoplamentos

| De | Para | Tipo | Contrato | Observação |
| --- | --- | --- | --- | --- |
| | | HTTP / fila / banco / import | explícito / implícito | |

## 4. Dados e persistência

| Store | Tecnologia | Entidades | Acesso | Observação |
| --- | --- | --- | --- | --- |

## 5. Configuração e ambiente

| Item | Onde | Observação |
| --- | --- | --- |

> Não copie valores de segredo. Registre a existência e o risco.

## 6. Pontos frágeis (para handoff ao `security`)

| # | Ponto | Por que é frágil | Evidência |
| --- | --- | --- | --- |

## 7. Decisões registradas

| ADR | Título | Status |
| --- | --- | --- |

## 8. Critério de saída

- [ ] Toda dependência crítica tem versão, origem e status.
- [ ] Componentes e fronteiras estão mapeados.
- [ ] Pontos frágeis encaminhados ao agente de segurança.

## 9. Handoff

```md
## Handoff RE-02 → RE-03
**Produzido:**
**Critério de saída:**
**Confiança geral:**
**Pendências:**
**Próximo passo sugerido:**
```
