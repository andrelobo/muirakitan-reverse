# STATUS — ponto de retomada

> Última atualização: **2026-11-01**
> Leia este arquivo primeiro ao abrir o projeto. Atualize-o ao fim de cada sessão.

---

## 1. Onde o projeto está

**Fase 0 (fundação) concluída.** Documentação, agentes e harness prontos e
validados. Nenhuma análise técnica foi executada ainda.

| Item | Estado |
| --- | --- |
| Repositório | `github.com/andrelobo/muirakitan-reverse` |
| Branch | `main`, sincronizada com `origin/main` |
| Último commit | `b051ed4` — estrutura inicial |
| Working tree | limpo |
| Engajamento ativo | nenhum |
| Autorização registrada | nenhuma (`evidence/authorization/` vazio) |

## 2. O que está pronto e verificado

Não é "escrito", é **verificado em execução**:

- [x] `opencode.jsonc` carrega sem erro.
- [x] `SECURITY.md` é injetado em toda sessão via `instructions`.
- [x] MCP `playwright` conectado — 25 ferramentas registradas.
- [x] Skill `evidence-record` visível no catálogo de skills.
- [x] 5 agentes com frontmatter YAML válido (`mode`, `steps`, `permissions`).
- [x] `scripts/hash-manifest.sh` testado com 0 e 1 arquivo — manifesto válido.
- [x] Permissões de shell: `sudo`, `dd`, `mkfs`, `iptables`, `git push --force`
      negados; reconhecimento liberado; push pede aprovação.
- [x] Árvore `docs/ specs/ evidence/ src/ tests/` criada.
- [x] 8 templates prontos (`templates/`).

## 3. O que NÃO está pronto

| Item | Bloqueia | Observação |
| --- | --- | --- |
| Ghidra | Fase 2+ (binário) | ausente |
| Binwalk | Firmware Intelligence | ausente |
| Frida | instrumentação dinâmica | ausente |
| Rizin / Cutter | análise estática complementar | ausente |
| Isolamento (VM) | gate de segurança §3 | `libvirtd` não configurado |
| Alvo piloto | RE-01 em diante | não escolhido |
| Wrappers MCP | autonomia de ferramentas | não iniciados |
| `src/` e `tests/` | RE-05/06 | vazios (correto nesta fase) |

## 4. Ambiente do host (verificado)

| Recurso | Estado |
| --- | --- |
| OpenCode | v2.2.1 |
| Node.js | v22.23.1 |
| npm / npx | 12.0.1 |
| Python | 3.12.3 |
| Git | 2.43.0 |
| Docker | 29.9.2 — daemon acessível |
| jq | 1.7 |
| bunx | ausente (não necessário) |
| podman | ausente |
| libvirt | não configurado |

### ⚠ Restrição real: disco

```
/dev/sda4   73G   65G   4,2G   94%   /
```

**4,2 GB livres.** Ghidra + JDK + imagem de análise não cabem com folga.

Recuperável no Docker: ~6,5 GB (3,7 GB de imagens + 2,8 GB de build cache).
Antes de instalar qualquer ferramenta de binário:

```sh
docker system df                 # confira o que é reclamável
docker builder prune             # ~2,8 GB
docker image prune -a            # ~3,7 GB — remove imagens sem container ativo
```

Confirme o que está em uso antes de remover imagem.

## 5. Próxima ação (Fase 1, D1–D5)

Ordem exata. Não pule para Ghidra antes de resolver disco e isolamento.

1. **Liberar disco** — alvo: ≥ 15 GB livres. (ver §4)
2. **Criar ambiente isolado** — Docker é o caminho mais curto aqui, já que o
   daemon funciona e libvirt não está configurado.
   - imagem base Linux, sem `--privileged`, sem `--network host`;
   - volume separado para artefatos do engajamento;
   - comando único de subir e destruir.
3. **Escolher o alvo piloto** — aplicação SaaS open source com frontend, backend
   e documentação parcial. **Não** firmware.
4. **Preencher `templates/authorization-scope.md`** e salvar em
   `evidence/authorization/` — mesmo sendo projeto próprio ou open source.
5. **Teste de fumaça do harness:**
   - rodar `./scripts/hash-manifest.sh`;
   - gerar um HAR de teste e verificar entrada no manifesto;
   - tentar editar `src/` como `discovery` e confirmar a negação.

**Critério de saída da Fase 1** (de `ROADMAP.md`):
- [ ] `opencode mcp list` mostra Playwright conectado.
- [ ] Uma captura HAR de teste é gerada e hasheada em `evidence/`.
- [ ] Ambiente de alvo sobe e é destruído com um comando.

## 6. Decisões abertas

| # | Decisão | Opções | Padrão atual |
| --- | --- | --- | --- |
| D1 | Agente padrão | `orchestrator` (bloqueia sem autorização) · `build` (direto) | `orchestrator` |
| D2 | Isolamento | Docker (disponível) · VM com libvirt (não configurada) | a definir |
| D3 | Alvo piloto | open source SaaS · API própria · sistema do cliente | não escolhido |
| D4 | Modelo por agente | herdar do pai · modelo próprio por especialista | herda |
| D5 | Onde Ghidra roda | container de análise · host (não recomendado) | a definir |

D5 depende de D2. D3 depende de liberar disco.

## 7. Verificação rápida de saúde

```sh
cd "/home/lobo/Área de trabalho/KODE/muirakitan-reverse"
git status --short --branch          # deve estar limpo e sincronizado
opencode mcp list                    # playwright deve aparecer conectado
./scripts/hash-manifest.sh           # manifesto deve regenerar sem erro
ls .opencode/agents/                 # 5 agentes
```

## 8. Como retomar

```sh
cd "/home/lobo/Área de trabalho/KODE/muirakitan-reverse" && opencode
```

Cai no `orchestrator`. Primeira mensagem sugerida:

```text
Leia STATUS.md e retome a Fase 1 a partir do item 1 (liberar disco).
Não inicie RE-01 sem autorização registrada.
```

## 9. Convenção para as próximas sessões

Ao final de cada sessão, atualize **este arquivo**:

1. Nova data no topo.
2. Mova o que foi concluído para §2 e remova de §5.
3. Registre decisões tomadas em §6 (marcando a escolhida).
4. Atualize §3 com o que continua pendente.
5. Commit com mensagem `chore: status <data>`.

O histórico fica no Git; o estado corrente fica aqui.
