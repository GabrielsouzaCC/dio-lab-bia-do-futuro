# 🚀 Aplicação BIA Investimentos

Chatbot interativo para consultoria de investimentos em ações da B3.

## 📁 Estrutura

```
src/
├── app.py              # Aplicação Streamlit (interface)
├── agente.py           # Lógica de integração com LLMs
├── requirements.txt    # Dependências Python
└── .env.example        # Template de configuração
```

## 🛠️ Instalação

### 1. Instalar dependências

```bash
cd src
pip install -r requirements.txt
```

### 2. Configurar API (escolha uma opção)

**Opção A: OpenAI (ChatGPT)**
```bash
cp .env.example .env
# Edite .env e adicione: OPENAI_API_KEY=sua-chave
```

**Opção B: Anthropic (Claude)**
```bash
cp .env.example .env
# Edite .env e adicione: ANTHROPIC_API_KEY=sua-chave
```

**Opção C: Google (Gemini)**
```bash
cp .env.example .env
# Edite .env e adicione: GOOGLE_API_KEY=sua-chave
```

**Opção D: Ollama (Local - sem API key)**
```bash
# Instale Ollama: https://ollama.ai/
ollama pull llama2
# Trocar para ollama pull gpt-oss
# Não precisa de .env
```

### 3. Ativar integração com LLM

Edite `agente.py` e descomente o código da API escolhida.

## ▶️ Como Rodar

```bash
streamlit run app.py
```

ou

```bash
python -m streamlit run app.py
```

Acesse: http://localhost:8501

## 🎯 Funcionalidades

- ✅ Interface de chat interativa
- ✅ Carregamento automático de dados (perfil + ações)
- ✅ Filtragem de ações por perfil de risco
- ✅ Sidebar com informações do investidor
- ✅ System prompt com regras anti-alucinação
- ✅ Contexto formatado com indicadores fundamentalistas

## 🔌 Integrando com LLM

### Exemplo: OpenAI

1. Obtenha API key em: https://platform.openai.com/api-keys

2. Configure no `.env`:
```
OPENAI_API_KEY=sk-...
```

3. Descomente em `agente.py`:
```python
def chat_openai(mensagens, contexto):
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    # ... resto do código
```

4. Em `app.py`, substitua a resposta simulada:
```python
from agente import processar_mensagem

# Substituir:
resposta = "MODO DEMONSTRAÇÃO..."

# Por:
resposta = processar_mensagem(
    st.session_state.messages,
    contexto_completo,
    provider="openai"
)
```

## 📊 Dados Utilizados

| Arquivo | Localização | Descrição |
|---------|-------------|-----------|
| `acoes_b3.json` | `../data/` | 12 ações com indicadores |
| `perfil_investidor.json` | `../data/` | Perfil do investidor |
| `transacoes.csv` | `../data/` | Histórico financeiro |

## 🧪 Testando

**Perguntas sugeridas:**
- "Quero começar a investir em ações. O que você recomenda?"
- "O que significa P/L?"
- "Como diversificar minha carteira entre setores?"
- "Qual a diferença entre ITUB4 e PETR4?"

## ⚠️ Limitações

- Dados mockados (não são cotações reais)
- Não executa ordens de compra/venda
- Não substitui assessoria profissional
- Requer API key de LLM (exceto Ollama)

## 🔐 Segurança

- Nunca commite o arquivo `.env` (já está no .gitignore)
- API keys são carregadas via variáveis de ambiente
- Disclaimers de risco em todas as recomendações

## 📝 Próximos Passos

- [ ] Adicionar histórico persistente de conversas
- [ ] Implementar análise de correlação entre ativos
- [ ] Criar visualizações de carteira sugerida
- [ ] Adicionar exportação de recomendações em PDF
- [ ] Integrar com APIs de cotações reais (Alpha Vantage, Yahoo Finance)