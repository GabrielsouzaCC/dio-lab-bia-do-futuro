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

Para Simplificar Podemos "injetar" os Dados em Nosso Prompt, Garantidno Que o Agente Tenha o Melhor Contexto Possivel

### Como os dados são carregados?
import json
import pandas as pd
import requests

def carregar_json_url(url):
    try:
        return requests.get(url).json()
    except:
        print(f"Erro ao carregar {url}")
        return None

def carregar_csv_url(url):
    try:
        return pd.read_csv(url)
    except:
        print(f"Erro ao carregar {url}")
        return None

# 
base = "https://raw.githubusercontent.com/GabrielsouzaCC/dio-lab-bia-do-futuro/main/data/"

acoes_b3 = carregar_json_url(base + "acoes_b3.json")
perfil_investidor = carregar_json_url(base + "perfil_investidor.json")
produtos_financeiros = carregar_json_url(base + "produtos_financeiros.json")

transacoes = carregar_csv_url(base + "transacoes.csv")
historico_atendimento = carregar_csv_url(base + "historico_atendimento.csv")

### Como os dados são usados no prompt?
O **Sky Invest** usa dados reais da pasta `data/` para gerar recomendações financeiras.

---

###  Como funciona

#### System Prompt
Define as regras do sistema:
- respeitar o perfil do investidor  
- sugerir apenas investimentos compatíveis  

#### Context Injection
Os dados são carregados automaticamente:
- `perfil_investidor.json` → dados do investidor  
- `transacoes.csv` → saldo disponível  
- `produtos_financeiros.json` → investimentos  
- `acoes_b3.json` → ações  
- `historico_atendimento.csv` → histórico  

#### Filtragem
O sistema seleciona:
- produtos de acordo com o risco  
- ações compatíveis com o perfil  

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
##  Exemplo de Recomendação

**Investidor:** Waldir Oliveira  
**Perfil:** moderado  
**Saldo:** R$ 2511.10  

---

###  Sugestões de investimento

- Tesouro Selic  
- CDB Liquidez Diária  
- Fundo Multimercado  

---

###  Ações recomendadas

- ITUB4  
- PETR4  
- VALE3  

[...outras ações compatíveis]
```
