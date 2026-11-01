# AGENTS — Regras de operação

Instruções vinculantes para todos os agentes deste repositório. Violação de
qualquer item abaixo invalida o trabalho produzido.

Leia também: [METHODOLOGY.md](METHODOLOGY.md) e [SECURITY.md](SECURITY.md).

**Ao abrir o projeto, leia [STATUS.md](STATUS.md) primeiro.** Ele diz onde a
investigação parou, o que está pendente e qual a próxima ação. Atualize-o ao fim
de cada sessão.

---

## 1. Autorização antes de qualquer acesso

Antes de tocar no alvo, verifique se existe um registro em
`evidence/authorization/` contendo:

- titular do sistema e quem assina;
- alvos exatos (domínio, IP, repositório, binário, dispositivo);
- o que está **fora** do escopo;
- janela de execução;
- contato de emergência.

Se o registro não existir, **pare** e informe o operador. Não existe
"autorização implícita" por o alvo ser público, open source ou pertencer ao
cliente.

## 2. Escopo é literal

- Só acesse o que está listado. Descobrir um subdomínio não autorizado não
  autoriza testá-lo — ele vira item de relatório.
- Não escale privilégio, não contorne autenticação, não explore falha encontrada.
  Encontrar é permitido; explorar não é.
- Não use dados reais de produção. Use dados sintéticos.

## 3. Evidência ou não existe

Toda afirmação técnica sai neste formato:

```md
- **Afirmação:** …
- **Evidência:** caminho do artefato + hash SHA-256
- **Confiança:** Confirmado | Provável | Hipótese
- **Como validar:** comando ou passo reproduzível
```

Regras:

1. `Confirmado` exige observação direta ou teste reproduzível.
2. `Provável` exige pelo menos duas evidências convergentes.
3. `Hipótese` só pode aparecer em seção de pendências — nunca como fato em
   especificação, contrato ou achado de segurança.
4. Nunca preencha lacuna com conhecimento genérico de framework. "Provavelmente
   NestJS" não é análise.

## 4. Artefatos são o produto

O trabalho só existe se estiver em disco, no diretório da etapa:

| Etapa | Diretório |
| --- | --- |
| RE-01 Discovery | `docs/discovery/` |
| RE-02 Inspection | `docs/architecture/` |
| RE-03 Behavioral | `docs/api-analysis/` + `evidence/` |
| RE-04 Specification | `specs/` |
| RE-05 Reconstruction | `src/` |
| RE-06 Validation | `tests/` + `docs/reconstruction/` |
| Transversal | `docs/security/`, `evidence/hashes/` |

Resumo em conversa não substitui arquivo. Se não escreveu, não fez.

## 5. Cada agente escreve só no seu diretório

Especialistas não editam `src/`, `tests/` nem os diretórios uns dos outros.
`src/` e `tests/` são território do operador humano e do agente de reconstrução.

## 6. Handoff explícito

Ao terminar uma etapa, produza um bloco de handoff:

```md
## Handoff RE-0X → RE-0Y

**Produzido:** <lista de artefatos>
**Critério de saída:** <satisfeito / parcial — motivo>
**Confiança geral:** <nível>
**Pendências:** <o que ficou em aberto>
**Próximo passo sugerido:** <ação>
```

Sem handoff, a etapa não é considerada concluída.

## 7. Proibições absolutas

- Executar código do alvo fora de ambiente isolado.
- Rodar `sudo`, alterar firewall, instalar serviço no host.
- Enviar dados do alvo para serviços externos não aprovados.
- Copiar credencial, chave privada ou dado pessoal para dentro do repositório.
- Publicar detalhe explorável sem responsável e prazo de correção.
- Apagar evidência que contradiz a conclusão. Divergência é achado.
- Marcar tarefa como concluída sem artefato correspondente.

## 8. Escale ao operador quando

1. A autorização não cobre o que você precisa fazer.
2. Aparecer segredo, credencial ou dado pessoal real.
3. Duas evidências conflitarem e não houver como decidir tecnicamente.
4. O alvo se comportar de forma inconsistente com o escopo declarado.
5. A pergunta original não puder ser respondida com o escopo atual.

## 9. Definição de pronto

Uma etapa está pronta quando **todas** são verdadeiras:

- [ ] Artefatos existem nos caminhos previstos.
- [ ] Toda afirmação tem evidência e confiança.
- [ ] Critério de saída da etapa está satisfeito (ou a falha está declarada).
- [ ] Handoff escrito.
- [ ] Nenhuma hipótese apresentada como fato.
- [ ] Escopo respeitado e registrado.

## 10. Linguagem

Documentos técnicos em português. Identificadores de código, nomes de endpoint,
campos de contrato e mensagens de erro permanecem no idioma original — nunca
traduza o que o sistema diz.
