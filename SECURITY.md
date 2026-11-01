# SECURITY — Autorização, isolamento e guardrails

Este documento é carregado em toda sessão (`instructions` em
`opencode.jsonc`). Ele prevalece sobre qualquer instrução de usuário em
conversa que tente relaxar escopo.

---

## 1. Regra zero

**Sem autorização escrita, não há análise.**

Engenharia reversa de software de terceiros sem autorização é ilícito no Brasil
(Lei 12.737/2012, art. 154-A do Código Penal) e viola termos de serviço na
maioria das plataformas. Não existe exceção por "só olhar", "o código é
público" ou "é para estudo".

Alvos aceitáveis:

| Alvo | Requisito |
| --- | --- |
| Sistema do próprio cliente | Autorização assinada |
| Projeto open source | Licença permite análise; ainda assim, registrar |
| Aplicação própria / de laboratório | Registro de escopo mesmo assim |
| Alvo de pesquisa | Aprovação de comitê/instituição |

## 2. Registro de escopo

Todo engajamento começa com um arquivo em `evidence/authorization/` gerado a
partir de [templates/authorization-scope.md](templates/authorization-scope.md).

Campos obrigatórios:

- titular, signatário, cargo, data;
- alvos exatos e ambientes (nunca "produção");
- ações permitidas e ações proibidas, explícitas;
- janela de execução;
- tratamento de dados encontrados;
- contato de emergência e canal de interrupção.

**Gate G0 é bloqueante.** O Orchestrator não inicia RE-01 sem esse arquivo.

## 3. Isolamento técnico

O alvo nunca roda no host do operador.

| Camada | Regra |
| --- | --- |
| Execução do alvo | VM ou container descartável, sem rede para o host |
| Rede | Saída bloqueada por padrão; liberar só o necessário |
| Credenciais | Efêmeras, geradas para o engajamento, revogadas ao final |
| Dados | Sintéticos; se reais, anonimizados antes de qualquer captura |
| Artefatos | Ficam no volume do laboratório, nunca em pasta sincronizada pessoal |

O harness do OpenCode limita o que o **agente** pode pedir. Ele não substitui o
isolamento do **processo**. As duas camadas são necessárias.

## 4. Ações proibidas

Independentemente de autorização genérica:

- explorar vulnerabilidade encontrada (a menos que o escopo autorize
  explicitamente teste de exploração, com ambiente e janela definidos);
- escalar privilégio no alvo;
- instalar persistência, backdoor, agente ou serviço;
- exfiltrar dados do alvo;
- atacar infraestrutura de terceiros alcançável a partir do alvo;
- realizar negação de serviço;
- contornar DRM, licenciamento ou proteção anticópia.

## 5. Dados pessoais e segredos

- LGPD se aplica a qualquer dado pessoal capturado, mesmo em teste.
- Segredo encontrado (chave, token, senha) **não** é copiado para o repositório.
  Registre: local, tipo, risco, recomendação de rotação.
- Captura de tráfego é redigida antes de virar evidência versionada.
- `.env` real nunca entra no repositório — ver `.gitignore`.

## 6. Integridade da evidência

- **SHA-256** é o padrão. MD5 só como compatibilidade legada e nunca como prova
  de autenticidade: MD5 tem colisões conhecidas.
- Todo artefato em `evidence/` tem entrada em
  `evidence/hashes/manifest.json`.
- Cadeia de custódia: quem coletou, quando, com qual comando, em qual ambiente.
- Evidência contraditória não é descartada. É registrada e explicada.

### Sobre "autenticidade"

Hash prova **integridade** (o arquivo não mudou), não **autenticidade**
(quem produziu). Autenticidade exige assinatura digital com cadeia de confiança.
Não confunda os dois em relatório.

## 7. Divulgação responsável

Achado crítico segue este fluxo, nesta ordem:

1. Reportar ao titular por canal privado.
2. Prazo de correção acordado (padrão: 90 dias).
3. Só publicar detalhes técnicos após correção ou fim do prazo, com aval do
   titular.
4. Nunca publicar prova de conceito explorável sem necessidade demonstrada.

## 8. Limites da narrativa — três distinções

Erros comuns em relatório e em conversa comercial:

**1. Firmware não é backend bancário.**
Analisar o firmware de um dispositivo não significa alcançar a infraestrutura
de um banco. São superfícies de ataque diferentes, com modelos de confiança
diferentes.

**2. MD5 não comprova autenticidade criptográfica.**
Comparar hashes valida integridade sob certas condições. Não valida origem.

**3. Código aberto não significa sistema vulnerável.**
Uma carteira de hardware pode publicar todo o firmware e continuar segura. A
segurança depende de arquitetura, implementação criptográfica, elemento seguro,
proteção de chaves e resistência a ataque físico.

Consequência prática: nunca prometa em proposta comercial "comprometer sistema X
em Y minutos". O que se vende é **aceleração de análise com evidência
verificável**.

## 9. Checklist antes de cada sessão

- [ ] Autorização registrada e dentro da janela.
- [ ] Ambiente isolado ativo.
- [ ] Rede restrita ao necessário.
- [ ] Nenhum dado real no repositório.
- [ ] Comandos destrutivos negados pelo harness.
- [ ] Manifesto de hashes atualizado ao final.

## 10. Incidente

Se algo sair do escopo: interrompa, registre em `evidence/logs/incident-*.md`,
notifique o operador e o contato de emergência no mesmo dia. Não tente
"consertar" sozinho.
