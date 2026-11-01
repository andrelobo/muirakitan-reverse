# CONTEXT — Muirakitan Reverse

## 1. Propósito

Este repositório é um **laboratório de engenharia reversa assistida por IA**.

Não é um produto fechado, não é uma agência e não é um curso. É a base técnica de
uma nova linha de especialização da Muirakitan: conduzir **investigação técnica
reproduzível** sobre sistemas existentes — documentados ou não — e entregar
resultados verificáveis.

O diferencial não é "usar IA para desmontar um binário". É **conduzir uma
investigação**: separar fato de hipótese, registrar evidência, validar conclusão
e reconstruir o sistema de forma independente.

> Regra fundadora: nenhuma conclusão deste laboratório vale sem evidência
> anexada e grau de confiança declarado.

## 2. Problema que resolvemos

O mercado não compra "engenharia reversa". Ele compra a saída de situações
concretas:

| Dor do cliente | O que ele realmente precisa |
| --- | --- |
| "Meu sistema funciona, mas ninguém sabe como foi construído." | Inventário, mapa de dependências e documentação executável |
| "Quero sair de uma tecnologia antiga." | Diagnóstico de acoplamentos e plano de modernização por etapas |
| "Perdi o desenvolvedor que conhecia o sistema." | Conhecimento extraído do artefato, não da memória de alguém |
| "Preciso integrar uma plataforma sem documentação." | Contrato de API inferido e validado por comportamento |
| "Quero saber se minha aplicação está vulnerável." | Avaliação com escopo autorizado e relatório reproduzível |

## 3. Linhas de serviço

Três ofertas progressivas. A ordem reflete o esforço de entrada, não a ambição.

### 3.1 Legacy System Intelligence
Diagnóstico técnico de sistemas existentes.
Inventário tecnológico · mapa de dependências · documentação de APIs ·
identificação de riscos · plano de modernização.

**Cliente ideal:** empresa com sistema antigo, documentação incompleta e
dependência de fornecedor único.

### 3.2 AI-Assisted Software Reconstruction
Reconstrução de aplicações a partir de requisitos e comportamentos observados.
Reverse engineering funcional · especificação SDD · nova arquitetura ·
implementação e testes · migração gradual.

### 3.3 AI Security Assessment
Avaliação de segurança assistida por agentes.
Análise estática · dependências vulneráveis · configurações inseguras ·
análise de APIs · relatório técnico e recomendações.

**Sempre** com autorização formal, escopo escrito e ambiente de teste controlado.
Ver [SECURITY.md](SECURITY.md).

## 4. Frentes técnicas priorizadas

| Frente | Aplicação comercial | Prioridade |
| --- | --- | --- |
| Reverse Engineering de APIs | Entender integrações sem documentação | 1 |
| Legacy Software Intelligence | Analisar sistemas antigos e documentar funcionamento | 1 |
| AI Security Audit | Identificar vulnerabilidades com agentes | 1 |
| Software Reconstruction | Reconstruir sistemas a partir de evidências | 2 |
| Firmware Intelligence | Analisar firmware e embarcados autorizados | 3 |

As três primeiras exigem menos hardware especializado e estão mais próximas da
competência já existente (Node.js, TypeScript, Python, NestJS, APIs,
arquitetura, SDD, OpenCode).

**Firmware não é o ponto de partida.** O laboratório começa em software:
aplicações web, APIs e sistemas legados.

## 5. Escopo do laboratório

**Dentro:**
- Análise de aplicações web e APIs próprias ou de código aberto.
- Análise de sistemas legados com autorização do titular.
- Análise estática de binários em ambiente isolado.
- Reconstrução funcional com testes de equivalência.
- Produção de artefatos persistentes: inventário, especificação, evidência.

**Fora:**
- Qualquer alvo sem autorização escrita e registrada.
- Sistemas de terceiros em produção.
- Bypass de proteção, DRM ou licenciamento.
- Coleta de dados pessoais além do necessário para a análise.
- Publicação de detalhes exploráveis sem responsável e prazo de correção.

## 6. Não-objetivos

- Não somos um laboratório de pentest ofensivo contratado.
- Não emitimos laudo pericial com validade judicial.
- Não prometemos "descobrir tudo" sobre um alvo. Prometemos cobertura
  declarada, com o que ficou fora explicitamente listado.
- Não automatizamos decisão de risco. A IA produz análise; humano assina.

## 7. Indicadores de sucesso

Medidos por engajamento, registrados em `docs/reconstruction/`:

| Indicador | Meta inicial |
| --- | --- |
| Tempo até o primeiro inventário útil | ≤ 1 dia de trabalho |
| Funcionalidades documentadas | ≥ 80% dos fluxos mapeados |
| Cobertura de fluxos de negócio | ≥ 70% dos fluxos críticos |
| Inconsistências identificadas | registradas, não descartadas |
| Testes de equivalência aprovados | ≥ 90% na reconstrução |
| Tempo de reconstrução vs. desenvolvimento convencional | ≤ 60% |

## 8. Premissas

1. **Autorização precede acesso.** Sem escopo assinado, não há análise.
2. **Isolamento é requisito, não cuidado.** Alvo roda em VM/container descartável.
3. **Saída do LLM não é verdade.** É hipótese com evidência anexada.
4. **Artefato em disco vence contexto em memória.** O que não foi escrito não
   aconteceu.
5. **O laboratório é separado da agência.** Nada de misturar com repositórios de
   cliente ou de produção.

## 9. Relação com os outros documentos

| Documento | Responde |
| --- | --- |
| [ARCHITECTURE.md](ARCHITECTURE.md) | Como o engine é montado |
| [METHODOLOGY.md](METHODOLOGY.md) | Como a investigação é conduzida |
| [AGENTS.md](AGENTS.md) | Regras de operação dos agentes |
| [MCP.md](MCP.md) | Ferramentas e integrações |
| [SECURITY.md](SECURITY.md) | Autorização, isolamento e guardrails |
| [ROADMAP.md](ROADMAP.md) | Implementação incremental |
