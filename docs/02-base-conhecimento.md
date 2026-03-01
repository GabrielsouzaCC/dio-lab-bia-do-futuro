# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `acoes_b3.json` | JSON | Base de ações da B3 com indicadores fundamentalistas |
| `perfil_investidor.json` | JSON | Perfil de risco e objetivos do investidor |
| `transacoes.csv` | CSV | Histórico financeiro para análise de capacidade de investimento |
| `historico_atendimento.csv` | CSV | Contexto de interações anteriores |
| `produtos_financeiros.json` | JSON | Produtos de renda fixa para diversificação |

> [!TIP]
> **Quer um dataset mais robusto?** Você pode utilizar datasets públicos do [Hugging Face](https://huggingface.co/datasets) relacionados a finanças, desde que sejam adequados ao contexto do desafio.

---

## Adaptações nos Dados

**Arquivo criado: `acoes_b3.json`**
- Contém 12 ações de diferentes setores da B3
- Inclui indicadores: P/L, ROE, Dividend Yield, volatilidade
- Classificação de risco e perfil indicado
- Descrição resumida de cada empresa

**Arquivo adaptado: `perfil_investidor.json`**
- Ajustado para perfil moderado interessado em ações
- Adicionado capital disponível para investimento em ações
- Incluído setores de interesse e horizonte de investimento
- Metas focadas em construção de carteira e renda passiva

---

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
