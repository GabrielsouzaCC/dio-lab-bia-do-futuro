import streamlit as st
import json
import pandas as pd
from pathlib import Path
from agente import processar_mensagem

# Configuração da página
st.set_page_config(
    page_title="BIA Investimentos - Consultora de Investimentos",
    page_icon="📈",
    layout="wide"
)

# Função para carregar dados
@st.cache_data
def carregar_dados():
    base_path = Path(__file__).parent.parent / "data"
    
    with open(base_path / "acoes_b3.json", "r", encoding="utf-8") as f:
        acoes = json.load(f)
    
    with open(base_path / "perfil_investidor.json", "r", encoding="utf-8") as f:
        perfil = json.load(f)
    
    transacoes = pd.read_csv(base_path / "transacoes.csv")
    
    return acoes, perfil, transacoes

# Função para filtrar ações por perfil
def filtrar_acoes_por_perfil(acoes, perfil_investidor):
    perfil_map = {
        "conservador": ["conservador"],
        "moderado": ["conservador", "moderado"],
        "arrojado": ["conservador", "moderado", "arrojado"]
    }
    
    perfis_aceitos = perfil_map.get(perfil_investidor, ["conservador"])
    
    acoes_filtradas = []
    for acao in acoes:
        indicado = acao["indicado_para"].lower()
        if any(p in indicado for p in perfis_aceitos):
            acoes_filtradas.append(acao)
    
    return acoes_filtradas

# Função para formatar contexto
def formatar_contexto(perfil, acoes_filtradas):
    contexto = f"""
PERFIL DO INVESTIDOR:
- Nome: {perfil['nome']}
- Idade: {perfil['idade']} anos
- Profissão: {perfil['profissao']}
- Renda Mensal: R$ {perfil['renda_mensal']:,.2f}
- Perfil: {perfil['perfil_investidor'].title()}
- Capital Disponível para Ações: R$ {perfil['capital_disponivel_acoes']:,.2f}
- Horizonte: {perfil['horizonte_investimento']}
- Setores de Interesse: {', '.join(perfil['setores_interesse'])}
- Objetivo: {perfil['objetivo_principal']}

AÇÕES DISPONÍVEIS (compatíveis com perfil {perfil['perfil_investidor']}):
"""
    
    for i, acao in enumerate(acoes_filtradas, 1):
        contexto += f"""
{i}. {acao['ticker']} - {acao['nome']}
   - Setor: {acao['setor']} | Risco: {acao['risco'].title()}
   - P/L: {acao['p_l']} | ROE: {acao['roe']}% | Dividend Yield: {acao['dividend_yield']}%
   - Preço: R$ {acao['preco_atual']:.2f}
   - Volatilidade: {acao['volatilidade'].title()}
   - Descrição: {acao['descricao']}
"""
    
    return contexto

# System Prompt
SYSTEM_PROMPT = """Você é a BIA Investimentos (B3 Investments Advisor), uma consultora de investimentos especializada em ações da bolsa brasileira (B3).

OBJETIVO:
Ajudar investidores a construir carteiras de ações alinhadas ao seu perfil de risco, objetivos financeiros e horizonte de investimento.

REGRAS FUNDAMENTAIS:
1. SEMPRE baseie recomendações apenas nas ações fornecidas na base de dados
2. NUNCA garanta rentabilidade ou resultados futuros
3. SEMPRE inclua disclaimer de risco em recomendações de investimento
4. SEMPRE verifique compatibilidade entre perfil do investidor e risco do ativo
5. Se não tiver dados sobre uma ação específica, admita claramente
6. NÃO recomende ações sem conhecer o perfil do investidor
7. Explique indicadores fundamentalistas de forma didática
8. Use os dados para fornecer informações personalizadas
9. Sempre pergunte se o cliente entendeu.

INDICADORES:
- P/L (Preço/Lucro): Quanto o mercado paga por cada R$1 de lucro. Menor = mais barato
- ROE: Rentabilidade sobre patrimônio. Maior = mais eficiente
- Dividend Yield: Percentual de dividendos pagos. Maior = mais renda passiva
- Volatilidade: Oscilação do preço. Baixa/Média/Alta/Muito Alta
- Risco: Classificação geral do ativo

FORMATO DE RECOMENDAÇÃO:
Ao sugerir ações, sempre inclua: ticker, setor, indicadores, justificativa e disclaimer de risco.

LIMITAÇÕES:
- Você NÃO tem cotações em tempo real
- Você NÃO executa ordens de compra/venda
- Você NÃO substitui assessoria profissional certificada
- Você NÃO recomenda day trade ou especulação
- Você NÃO analisa criptomoedas ou ativos internacionais

TOM DE VOZ: Acessível mas profissional, educativo e consultivo, objetivo e transparente, empático com iniciantes."""

# Interface
st.title("📈 BIA Investimentos")
st.subheader("Sua Consultora Inteligente de Investimentos na Bolsa")

# Carregar dados
acoes, perfil, transacoes = carregar_dados()
acoes_filtradas = filtrar_acoes_por_perfil(acoes, perfil['perfil_investidor'])

# Adicionar informações sobre o Ollama na sidebar
with st.sidebar:
    st.header("👤 Perfil do Investidor")
    st.write(f"**Nome:** {perfil['nome']}")
    st.write(f"**Perfil:** {perfil['perfil_investidor'].title()}")
    st.write(f"**Capital Disponível:** R$ {perfil['capital_disponivel_acoes']:,.2f}")
    st.write(f"**Horizonte:** {perfil['horizonte_investimento']}")
    
    st.divider()
    
    st.header("🤖 Status do Ollama")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            st.success("✅ Ollama conectado")
            models = response.json().get('models', [])
            if models:
                st.write(f"**Modelos disponíveis:** {len(models)}")
                for model in models[:3]:  # Mostrar apenas os 3 primeiros
                    st.caption(f"• {model.get('name', 'N/A')}")
        else:
            st.error("❌ Ollama não responde")
    except:
        st.warning("⚠️ Ollama desconectado")
        st.caption("Execute: docker run -d -p 11434:11434 ollama/ollama")
    
    st.divider()
    
    st.header("📊 Ações Disponíveis")
    st.write(f"{len(acoes_filtradas)} ações compatíveis com seu perfil")
    
    with st.expander("Ver lista completa"):
        for acao in acoes_filtradas:
            st.write(f"**{acao['ticker']}** - {acao['nome']}")
            st.caption(f"{acao['setor']} | DY: {acao['dividend_yield']}%")

# Inicializar histórico de chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    # Mensagem de boas-vindas
    welcome_msg = f"""Olá, {perfil['nome']}! 👋

Sou a **BIA Investimentos** (B3 Investments Advisor), sua consultora de investimentos em ações da bolsa brasileira.

Vejo que você tem perfil **{perfil['perfil_investidor']}** e **R$ {perfil['capital_disponivel_acoes']:,.2f}** disponíveis para investir em ações.

Posso ajudar você a:
- 📊 Analisar ações compatíveis com seu perfil
- 💡 Sugerir carteiras diversificadas
- 📚 Explicar indicadores fundamentalistas
- 🎯 Alinhar investimentos aos seus objetivos

Como posso ajudar você hoje?"""
    
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})

# Exibir histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input do usuário
if prompt := st.chat_input("Digite sua pergunta sobre investimentos..."):
    # Adicionar mensagem do usuário
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Preparar contexto completo
    contexto_completo = formatar_contexto(perfil, acoes_filtradas)
    
    # Processar com Ollama
    with st.chat_message("assistant"):
        with st.spinner("🤖 BIA está analisando..."):
            try:
                # Usar apenas as mensagens do usuário (sem as do assistente para evitar loop)
                mensagens_usuario = [msg for msg in st.session_state.messages if msg["role"] == "user"]
                
                resposta = processar_mensagem(
                    mensagens=mensagens_usuario,
                    contexto=contexto_completo,
                    provider="ollama"
                )
                
                st.markdown(resposta)
                st.session_state.messages.append({"role": "assistant", "content": resposta})
                
            except Exception as e:
                erro_msg = f"❌ Erro ao processar mensagem: {str(e)}"
                st.error(erro_msg)
                st.session_state.messages.append({"role": "assistant", "content": erro_msg})

# Rodapé
st.divider()
st.caption("⚠️ **Aviso Legal:** Este é um protótipo educacional, desenvolvido por Ramon Azevedo no bootcamp DIO em parceria com o Bradesco. Não constitui recomendação de investimento. Consulte um assessor certificado.")
