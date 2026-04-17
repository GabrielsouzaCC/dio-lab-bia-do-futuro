# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `acoes_b3.json` | JSON | Base de ações da B3 |
| `perfil_investidor.json` | JSON | Perfil de risco e objetivos do investidor |
| `transacoes.csv` | CSV | Histórico financeiro para análise de capacidade de investimento |
| `historico_atendimento.csv` | CSV | Contexto de interações anteriores |
| `produtos_financeiros.json` | JSON | Produtos de renda fixa para diversificação |

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

##  Adaptações nos Dados do Sky Invest

Durante o desenvolvimento do projeto **Sky Invest**, todos os arquivos de dados foram criados ou adaptados com o objetivo de tornar o sistema mais realista, funcional e alinhado ao mercado financeiro.

---

###  `acoes_b3.json`
- Inclusão de dados de mercado:
  - preço
  - volume de negociações
  - variação percentual
- Classificação por setor econômico
- Estrutura padronizada para análise no sistema

---

###  `perfil_investidor.json`
- Estrutura com diferentes perfis de investidor (conservador, moderado e arrojado)  
- Inclusão de dados como idade, renda mensal e valor disponível  
- Definição de objetivo financeiro e prazo de investimento  
- Classificação de tolerância ao risco  
- Preferências de investimento (renda fixa, ações e fundos)  
- Estrutura preparada para recomendações personalizadas  
---

###  `transacoes.csv`
- Criação de histórico financeiro mensal atualizado (2026)  
- Registro de entradas e saídas financeiras  
- Classificação por categorias (moradia, alimentação, transporte, etc.)  
- Inclusão de identificador (`id`) para cada transação  
- Adição de saldo acumulado após cada operação  
- Padronização dos dados para análise automática  
- Utilizado para cálculo da capacidade de investimento  

---

###  `historico_atendimento.csv`
- Criação de histórico de interações do usuário com o sistema  
- Registro dos canais de atendimento (chat, telefone, e-mail)  
- Classificação dos temas abordados (ex: CDB, Tesouro Selic, suporte)  
- Inclusão de resumo das interações  
- Indicação se o atendimento foi resolvido  
- Padronização dos dados para análise de comportamento  
- Utilizado para personalização das recomendações  

---

###  `produtos_financeiros.json`
- Criação de base de produtos financeiros (renda fixa e fundos)  
- Inclusão de informações relevantes:
  - nível de risco  
  - rentabilidade  
  - liquidez  
  - prazo  
  - tributação  
- Definição de valor mínimo de investimento  
- Indicação do perfil de investidor recomendado  
- Estrutura preparada para recomendações automáticas e diversificação  

---

## Resultado

Com essas adaptações, o **Sky Invest** passa a contar com uma base de dados estruturada que permite:

-  Análises financeiras mais precisas  
-  Personalização baseada no perfil do investidor  
-  Cálculo da capacidade de investimento  
-  Base preparada para recomendações de ativos e produtos  
-  Estrutura para simulação de um consultor financeiro automatizado
   
## Estratégia de Integração

### Como os dados são carregados?
Os arquivos JSON e CSV são carregados no início da sessão do chatbot e formatados como contexto estruturado para o LLM. O agente tem acesso a:
- Lista completa de ações disponíveis com todos os indicadores
- Perfil detalhado do investidor (risco, objetivos, capital)
- Histórico de transações para análise de padrão financeiro

### Como os dados são usados no prompt?
**Estratégia híbrida:**
- **System Prompt**: Contém regras, limitações e formato de resposta
- **Context Injection**: Dados do perfil e ações são injetados no contexto de cada conversa
- **Filtragem dinâmica**: Apenas ações compatíveis com o perfil são destacadas nas recomendações

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
PERFIL DO INVESTIDOR:
- Nome: João Silva
- Perfil: Moderado
- Capital disponível para ações: R$ 5.000,00
- Horizonte: 5-10 anos
- Setores de interesse: financeiro, tecnologia, energia
- Objetivo: Construir carteira diversificada de ações

AÇÕES DISPONÍVEIS (compatíveis com perfil moderado):
1. ITUB4 - Itaú Unibanco PN
   - Setor: Financeiro | Risco: Baixo
   - P/L: 7.8 | ROE: 18.5% | Dividend Yield: 5.2%
   - Preço: R$ 28,90

2. PETR4 - Petrobras PN
   - Setor: Petróleo e Gás | Risco: Médio
   - P/L: 4.2 | ROE: 28.5% | Dividend Yield: 12.8%
   - Preço: R$ 38,50

[...outras ações compatíveis]
```
