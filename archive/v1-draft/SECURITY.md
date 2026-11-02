# Muirakitan RE — Security & Guardrails

## Visão Geral

Este documento estabelece as políticas de segurança, autorização e isolamento para todas as atividades de engenharia reversa no framework Muirakitan RE. O objetivo é permitir investigações técnicas profundas mantendo controle rigoroso sobre ambiente, dados e responsabilidade.

### 1. Autorização Formal

Nenhuma atividade de engenharia reversa pode iniciar sem os seguintes documentos:

| Documento | Conteúdo Mínimo | Validade |
|-----------|-----------------|----------|
| **CONTEXT.md** | Visão do projeto, objetivos, escopo delimitado, identidade do cliente/solicitante, ativos a serem analisados, limitações conhecidas | Válido por ciclo completo (RE-01 a RE-06), deve ser reassinado se escopo mudar |
| **Letter of Authorization** | Assinatura legalmente responsável da empresa, data de início e fim, escapa específico (sistemas, redes, dispositivos), tipos de análise permitidas | Válido pelas datas especificadas, renovável por acordo mútuo |
| **Scope Document** | Lista detalhada de: URLs/IPs/hosts permitidos, contas de teste permitidas, operações permitidas (tipo de ferramenta, profundidade), dados que podem ser exportados | Válido por etapa, pode ser atualizado entre etapas se novo discover exigir ampliação |

### 2. Isolamento de Ambiente

Todas as execuções devem ocorrer em um dos seguintes ambientes:

#### A. Container Docker Isolado

```dockerfile
# Exemplo de configuração de container sandbox
docker run --rm \
  --name muirakitan-sandbox \
  --network isolated-network \
  --pid namespace:container \
  --userns keep-id \
  -v /home/lobo/Área\ de\ trabalho/KODE/muirakitan-reverse-engineering/evidence:/evidence:ro \
  -v /home/lobo/Área\ de\ trabalho/KODE/muirakitan-reverse-engineering/sandbox:/sandbox:rw \
  -e MUIRAKITAN_REQUIRE_HASH=true \
  muirakitan/mcp-base:latest
```

Políticas:
- **Filesystem**: Apenas leitura para evidence, escrita apenas em /sandbox/temp
- **Rede**: Sem acesso à rede host, exceto domínios explicitamente autorizados em CONTEXT.md
- **Processos**: Isolamento de PID namespace, sem processos filho não autorizados
- **Usuário**: Usuário não-root dentro do container, mapeamento de usuário keep-id

#### B. Ambiente de Máquina Virtual

- Usado quando análise exigir nível de acesso maior (firmware, binários de sistema operacional)
- VM deve estar em rede host-only ou NAT com firewall restrito
- Snapshots antes e após cada análise para possibilidade de rollback
- Logs de todas as operações dentro da VM

#### C. Ambiente Local com Limites (Último Recurso)

- Apenas quando sandbox e VM não são viáveis
- Deve ter aprovação explícita do Orchestrator + Operator humano
- Logs completos obrigatórios
- Hash validation de tudo que sai do ambiente

### 3. Hash Validation (Integridade de Evidências)

#### 3.1. SHA-256 é o padrão ouro

- MD5 é **proibido** para validação de autenticidade de resultados (apenas permitido para checksums de integridade de arquivo non-security, e mesmo assim deve ser marcado como such).
- SHA-256 deve ser calculado para:
  - Arquivos de entrada antes da análise
  - Arquivos de saída após análise
  - Qualquer dado transferido entre ferramentas
  - Commits no repositório Git a cada etapa concluída

#### 3.2. Procedimento de Hash

```bash
# Exemplo de cálculo de hash SHA-256
sha256sum /caminho/para/arquivo > /evidence/hash-registros/arquivo.sha256

# Verificação posterior
sha256sum -c /evidence/hash-registros/arquivo.sha256
```

#### 3.3. Registro de Hash

Cada hash deve ser registrado no formato metadata JSON:

```json
{
  "sha256": "3a7d4e...",
  "caminho_original": "/sandbox/binaries/target.exe",
  "caminho_hash": "/evidence/hash-registros/target.exe.sha256",
  "calculado_por": "discovery_agent",
  "etapa": "RE-01",
  "timestamp": "2026-01-15T14:30:00Z",
  "finalidade": "integridade-dos-dados-de-entrada"
}
```

### 4. Classificação de Risco

Todos os findings devem ser classificados quanto ao nível de risco:

| Nível | Critério | Ação Necessária |
|-------|----------|-----------------|
| **Crítico** | Vulnerabilidade explotável que compromete confidencialidade, integridade ou disponibilidade do sistema; acesso não autorizado a dados sensíveis; execução remota de código | Imediata notificação ao cliente, recomendação de mitigação urgente, não incluir em repositório público sem anonimização completa |
| **Alto** | Vulnerabilidade que requer condições específicas para exploração, mas impacto significativo; configurações inseguras que expõem dados; dependências com CVEs críticos | Notificação ao cliente dentro de 48 horas, documentação de workarounds |
| **Médio** | Vulnerabilidade com exploração difícil ou impacto limitado; versões de software fora de suporte sem exploits conhecidos documentados | Documentação no relatório, recomendação de atualização em próxima janela de manutenção |
| **Baixo** | Problemas de qualidade de código, depreciações, práticas não-otimizadas, aviso de configurações que não representam risco imediato | Documentação geral, incluído no relatório como "observações" |

### 5. Dados Sensíveis — Redaction Policy

#### 5.1. O que DEVE ser redigido (nunca aparecer em relatórios públicos ou commits):

- Senhas, tokens, chaves de API em texto puro
- Chaves privadas RSA/ECDSA
- Endereços IP de produção (exceto quando necessários para identificação de rede, caso em que usar "[REDACTED]" ou máscara parcial)
- Nomes de usuários de produção
- Caminhos de arquivo absolutos de sistemas de produção
- Dados pessoais de clientes (GDPR/LGPD compliance)

#### 5.2. Como redigir:

- Substituir por `[REDACTED]`
- Para IP addresses: usar máscara de rede (ex: `192.168.[REDACTED].[REDACTED]`)
- Para nomes de arquivos: use apenas o nome base, sem caminho absoluto (ex: `config.js` em vez de `/var/www/prod/config.js`)
- Para versões de software: manter se for conhecimento público, senão usar `[VERSION_REDACTED]`

#### 5.3. Exceções

- Se a exposição de um dado sensível for essencial para a compreensão do findings e o cliente autorizou por escrito, pode aparecer com nota de redaction.
- Todas as exceções devem ter justificativa documentada em `evidence/redaction-exceptions/`.

### 6. Política de Dados do Cliente

| Tipo de Dado | Período de Retenção | Destino Final |
|--------------|---------------------|---------------|
| Evidências de análise (logs, capturas, outputs de ferramentas) | 90 dias após entrega do relatório final | Destruição segura (shredding) ou devolução ao cliente |
| Relatórios finais | 2 anos após entrega | Arquivamento criptografado |
| Metadados e metadata | 2 anos após entrega | Arquivamento no repositório do projeto (anonimizado) |
| Documentos de autorização | 5 anos após término do contrato | Arquivamento legal |
| Commits e versionamento do repositório Muirakitan RE | Indefinido (parte do repositório) | Repositório público (após anonimização) ou privado (consoante acordado) |

### 7. Revisão Humana Gate (Human-in-the-Loop)

**Nenhum relatório final (RE-06) é considerado completo sem:**

1. **Revisão de todas as conclusões de LLM** com grau de confiança < 0.8 pelo Operator Agent (humano)
2. **Validação manual** de pelo menos 20% dos hallazgos críticos (aleatórios, não seleção confirmatória)
3. **Assinatura do Operator** no relatório de equivalência (seção `executive/summary.md`)
4. **Validação de hash** de todas as evidências críticas antes da publicação do relatório

#### Sinalização de Divergência

Se o Operator humano divergir de uma conclusão de agente:

```json
{
  "agent_conclusion": "X sistema possui vulnerabilidade crítica em função login()",
  "operator_decision": "não_confirmado",
  "operator_justificativa": "Análise manual não conseguiu reproduzir a vulnerabilidade em ambiente de teste; pode ser falso positivo da análise estática",
  "novo_grau_confianca": 0.2,
  "requer_nova_analise": true
}
```

### 8. Relatórios e Publicação

#### 7.1. Níveis de Relatório

| Nível | Público | Conteúdo | Aprovação Necessária |
|-------|---------|----------|---------------------|
| **Executive Summary** | Stakeholders não-técnicos | Resumo alto nível, riscos principais, recomendações gerais | Operator humano |
| **Technical Report** | Equipe técnica/segurança | Hallazgos detalhados, evidências, configurações, comandos executados | Operator humano + Security Agent |
| **Full Evidence** | Cliente autorizado | Todas as evidências brutas, logs completos, outputs de ferramentas | Cliente + Operator humano |
| **Academic/Research** | Comunidade de segurança | Hallaznovos generalizados, patterns identificados, recomendações de indústria | Revisão por pares + cliente |

#### 7.2. O que NÃO deve ser incluído em relatórios públicos:

- Nome do cliente (usar "Cliente do Setor X" ou alias)
- URLs de produção do cliente
- Dados sensíveis identificados (ver Política de Redaction)
- Tool-specific commands that could be used for attacks (resumir, não reproduzir integralmente)
- Hashts originais de arquivos do cliente (apenas formatos genéricos)

### 8. Responsabilidade Legal

O framework Muirakitan RE opera sob o princípio de:

- **Análise somente com autorização expressa**: Sem CONTEXT.md + Letter of Authorization = nenhuma execução
- **Limites geográficos e de rede**: Apenas alvos dentro do escopo autorizado podem ser analisados
- **Destruição de evidências**: Após período de retenção, todas as evidências devem ser destruídas ou devolvidas
- **Não responsabilidade por uso indevido**: O framework e seus agentes são ferramentas de apoio — a responsabilidade pelas decisões baseadas nas análises recai sobre o operador humano e contratante

### 9. Incident Response (Dentro do Escopo)

Se durante a análise ocorrer um incidente (ex: descobrimento de dado sensível não planejado, travamento de sistema, comportamento inesperado):

1. **Pausar imediatamente** todas as operações
2. **Registrar o incidente** em `evidence/incidents/{{timestamp}}.md` com:
   - O que aconteceu
   - Quais ferramentas estavam sendo usadas
   - Dados sensíveis potencialmente expostos
   - Ações imediatas tomadas
3. **Notificar o Orchestrator** dentro de 1 hora (tempo máximo)
4. **Decisão do Orchestrator**:continuar, modificar escopo ou encerrar ciclo
5. **Se houver vazamento de dados sensíveis**: Ativar política de redaction emergencial e notificar cliente

### 10. Checklist de Segurança Pré-Análise

Antes de iniciar qualquer etapa, o Orchestrator deve verificar:

- [ ] CONTEXT.md preenchido e assinado por todas as partes
- [ ] Letter of Authorization válido (verificar datas)
- [ ] Scope Document aprovado com todos os ativos listados
- [ ] Ambiente de sandbox configurado e testado
- [ ] Chaves de hash validation disponíveis e testadas
- [ ] Política de redaction compreendida pela equipe
- [ ] Operador humano disponível para gate de revisão durante o ciclo
- [ ] Rota de escape de emergência documentada
- [ ] Modelos de relatório disponíveis
- [ ] Backup dos metadados críticos realizados

**Se qualquer item estiver em "Não", a análise NÃO deve iniciar até que o item seja resolvido.**