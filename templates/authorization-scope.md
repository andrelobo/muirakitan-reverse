# Autorização de análise — <CLIENTE / PROJETO>

> Gate G0. Sem este documento assinado, nenhuma etapa do método pode iniciar.
> Salve como `evidence/authorization/<AAAA-MM-DD>-<cliente>-<escopo>.md`.

## 1. Partes

| Campo | Valor |
| --- | --- |
| Titular do sistema | |
| Signatário (nome, cargo) | |
| Documento / contrato de referência | |
| Executor | Muirakitan — <responsável> |
| Data de emissão | |

## 2. Alvos autorizados

Liste de forma exata. Domínio, IP, repositório, binário, dispositivo, versão.

| # | Alvo | Ambiente | Versão / commit | Observação |
| --- | --- | --- | --- | --- |
| 1 | | | | |

**Nenhum alvo fora desta tabela pode ser acessado.**

## 3. Ações permitidas

Marque o que está autorizado:

- [ ] Leitura de código-fonte / binário
- [ ] Navegação e captura de tráfego (Playwright, HAR)
- [ ] Chamadas a endpoints de API
- [ ] Análise estática de binário (Ghidra, Rizin)
- [ ] Análise de firmware (Binwalk)
- [ ] Instrumentação dinâmica (Frida)
- [ ] Teste de configuração de segurança
- [ ] Teste de exploração controlada (exige §5 preenchido)

## 4. Fora de escopo (explícito)

O que **não** pode ser tocado:

- ambientes de produção;
- dados de clientes reais;
- sistemas de terceiros alcançáveis a partir do alvo;
- infraestrutura de rede, DNS, firewall;
- outros: ______________________________________________

## 5. Teste de exploração (se aplicável)

| Campo | Valor |
| --- | --- |
| Técnicas autorizadas | |
| Ambiente | |
| Janela | |
| Profundidade máxima | |
| Interrupção por quem | |

Se esta seção estiver vazia, **explorar é proibido**. Encontrar e reportar não é
explorar.

## 6. Janela de execução

| Campo | Valor |
| --- | --- |
| Início | |
| Fim | |
| Horário permitido | |
| Fusos | |

## 7. Tratamento de dados

- [ ] Somente dados sintéticos
- [ ] Dados reais anonimizados antes de qualquer captura
- [ ] Dados pessoais: base legal e retenção acordadas
- [ ] Segredos encontrados: apenas registro (local, tipo, risco, rotação)

Retenção de evidência: ____ dias após entrega do relatório.

## 8. Contatos

| Papel | Nome | Canal | Disponibilidade |
| --- | --- | --- | --- |
| Contato técnico | | | |
| Contato de emergência | | | |
| Responsável pela autorização | | | |

## 9. Assinaturas

| Parte | Nome | Assinatura | Data |
| --- | --- | --- | --- |
| Titular | | | |
| Executor | | | |

---

## Uso interno

| Campo | Valor |
| --- | --- |
| Gate G0 aprovado em | |
| Aprovado por | |
| Registro no manifesto de hashes | |
