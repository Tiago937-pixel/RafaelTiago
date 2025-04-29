# Cole aqui todo o código do aplicativo que mostrei acima
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import binom
from scipy.stats import norm
import pandas as pd
from PIL import Image
import warnings
warnings.filterwarnings("ignore")

# Configuração da página
st.set_page_config(page_title="Análise de Operações Aéreas - Aérea Confiável",
                   layout="wide",
                   initial_sidebar_state="expanded")

# Slider CSS customization for blue color (cor da empresa aérea)
st.markdown(
    """
    <style>
    .stSlider > div > div > div > div > div > div {
        background-color: #0066CC !important;  /* Azul para o slider */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Título e Descrição
st.markdown("<h1 style='text-align: center; color: #0066CC;'>Análise de Operações Aéreas</h1>", 
            unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #0066CC;'>Aérea Confiável</h3>", 
            unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Ferramentas de análise para otimização de assentos e investimentos</p>", 
            unsafe_allow_html=True)

st.markdown("---")

# Criação das abas para diferentes análises
tab1, tab2, tab3, tab4 = st.tabs(["Análise de Overbooking", "Viabilidade de Passagens Extras", 
                                 "Investimento em SI", "Simulação de ROI"])

# Aba da Análise de Overbooking
with tab1:
    st.header("Análise de Overbooking")
    st.markdown("""
    Esta análise utiliza a distribuição binomial para calcular a probabilidade de overbooking em voos com 
    120 assentos disponíveis, considerando que podem ser vendidas até 130 passagens.
    """)

    # Parâmetros ajustáveis
    st.markdown("<h4 style='color: #0066CC;'>Probabilidade de Comparecimento (%)</h4>", unsafe_allow_html=True)
    p = st.slider("", min_value=0.80, max_value=0.95, value=0.88, step=0.01, key="p_overbooking")
    
    st.markdown("<h4 style='color: #0066CC;'>Número de Assentos no Avião</h4>", unsafe_allow_html=True)
    num_seats = st.slider("", min_value=100, max_value=150, value=120, step=1, key="num_seats")
    
    st.markdown("<h4 style='color: #0066CC;'>Número Máximo de Passagens a Vender</h4>", unsafe_allow_html=True)
    max_tickets = st.slider("", min_value=num_seats, max_value=num_seats+20, value=130, step=1, key="max_tickets")
    
    st.markdown("<h4 style='color: #0066CC;'>Nível de Risco Aceito (%)</h4>", unsafe_allow_html=True)
    risk_level = st.slider("", min_value=0.01, max_value=0.20, value=0.07, step=0.01, key="risk_level")
    
    # Cálculo da probabilidade de overbooking
    tickets_range = np.arange(num_seats, max_tickets + 1)
    probabilities = [1 - binom.cdf(num_seats - 1, n, p) for n in tickets_range]
    
    # Gráfico dinâmico usando Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=tickets_range, 
                             y=probabilities,
                             mode='lines+markers', 
                             line=dict(color='#0066CC', width=3)))
    
    fig.add_hline(y=risk_level, line_dash="dash", line_color="red", line_width=1)
    
    fig.update_layout(title=f"Risco de Overbooking para mais de {num_seats} passageiros",
                      xaxis_title="Passagens Vendidas",
                      yaxis_title="Probabilidade de Overbooking",
                      xaxis=dict(tickmode='linear', tick0=num_seats, dtick=1),
                      yaxis=dict(range=[0, max(max(probabilities)+0.05, risk_level+0.05)]),
                      plot_bgcolor="white",
                      height=400)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tabela de probabilidades
    table = pd.DataFrame({
        'Passagens Vendidas': tickets_range, 
        'Risco de Overbooking (%)': [round(p*100, 2) for p in probabilities]
    })
    
    st.write("### Tabela de Probabilidades de Overbooking")
    st.dataframe(table)
    
    # Determinar o número máximo de passagens vendidas dentro do risco aceito
    max_tickets_within_risk = table[table['Risco de Overbooking (%)'] <= risk_level*100]['Passagens Vendidas'].max()
    if pd.notna(max_tickets_within_risk):
        st.success(f"O número máximo de passagens que podem ser vendidas para manter o risco abaixo de {risk_level*100}% é de {int(max_tickets_within_risk)} passagens.")
    else:
        st.error(f"Nenhuma quantidade de passagens vendidas está abaixo do nível de risco aceito ({risk_level*100}%).")

# Aba da Viabilidade de Venda de Passagens Extras
with tab2:
    st.header("Viabilidade de Venda de Passagens Extras")
    st.markdown("""
    Esta análise avalia se é financeiramente vantajoso vender passagens extras, considerando possíveis 
    custos de overbooking, danos à imagem e receitas adicionais.
    """)
    
    # Parâmetros financeiros
    st.markdown("<h4 style='color: #0066CC;'>Valor Médio da Passagem (R$)</h4>", unsafe_allow_html=True)
    ticket_price = st.slider("", min_value=300, max_value=1000, value=500, step=10, key="ticket_price")
    
    st.markdown("<h4 style='color: #0066CC;'>Custo por Passageiro em Overbooking (R$)</h4>", unsafe_allow_html=True)
    overbooking_cost = st.slider("", min_value=500, max_value=2000, value=1200, step=100, key="overbooking_cost")
    
    st.markdown("<h4 style='color: #0066CC;'>Número de Passagens Extras a Vender</h4>", unsafe_allow_html=True)
    extra_tickets = st.slider("", min_value=1, max_value=15, value=10, step=1, key="extra_tickets")
    
    st.markdown("<h4 style='color: #0066CC;'>Probabilidade de Comparecimento (%)</h4>", unsafe_allow_html=True)
    p_attendance = st.slider("", min_value=0.80, max_value=0.95, value=0.88, step=0.01, key="p_attendance")
    
    # Número de assentos e total de passagens
    num_seats_viability = 120
    total_tickets = num_seats_viability + extra_tickets
    
    # Simular 10.000 voos
    np.random.seed(42)
    num_simulations = 10000
    passengers_showing = np.random.binomial(total_tickets, p_attendance, num_simulations)
    
    # Calcular overbooking e lucro
    overbooking_occurrences = passengers_showing > num_seats_viability
    revenue_from_extras = extra_tickets * ticket_price
    
    overbooking_passengers = np.maximum(0, passengers_showing - num_seats_viability)
    overbooking_costs = overbooking_passengers * overbooking_cost
    
    profits = np.full(num_simulations, revenue_from_extras) - overbooking_costs
    
    # Estatísticas
    avg_profit = np.mean(profits)
    profitable_flights = np.sum(profits > 0) / num_simulations * 100
    overbooking_freq = np.sum(overbooking_occurrences) / num_simulations * 100
    
    # Resultados em colunas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Lucro Médio por Voo", f"R$ {avg_profit:.2f}")
    with col2:
        st.metric("Frequência de Overbooking", f"{overbooking_freq:.2f}%")
    with col3:
        st.metric("Voos Lucrativos", f"{profitable_flights:.2f}%")
    
    # Histograma de lucros
    fig = px.histogram(
        x=profits,
        nbins=50,
        labels={"x": "Lucro por Voo (R$)"},
        title="Distribuição de Lucros com Venda de Passagens Extras",
        color_discrete_sequence=['#0066CC']
    )
    
    fig.update_layout(
        xaxis_title="Lucro (R$)",
        yaxis_title="Frequência",
        plot_bgcolor="white",
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Recomendação baseada nos resultados
    if avg_profit > 0 and profitable_flights > 60:
        st.success(f"Recomendação: É vantajoso vender {extra_tickets} passagens extras, com lucro médio de R$ {avg_profit:.2f} por voo.")
    elif avg_profit > 0:
        st.warning(f"Recomendação: A venda de {extra_tickets} passagens extras é marginalmente lucrativa, com lucro médio de R$ {avg_profit:.2f} por voo, mas os riscos devem ser considerados.")
    else:
        st.error(f"Recomendação: Não é vantajoso vender {extra_tickets} passagens extras, resultando em prejuízo médio de R$ {abs(avg_profit):.2f} por voo.")

# Aba de Investimento em Sistema de Informação
with tab3:
    st.header("Investimento em Sistema de Informação")
    st.markdown("""
    Esta análise calcula o ROI (Return on Investment) para um sistema de informação que promove 
    a melhoria da gestão de passagens.
    """)
    
    # Parâmetros do investimento
    st.markdown("<h4 style='color: #0066CC;'>Custo do Investimento (R$)</h4>", unsafe_allow_html=True)
    investment_cost = st.slider("", min_value=50000, max_value=200000, value=100000, step=10000, key="investment_cost")
    
    st.markdown("<h4 style='color: #0066CC;'>Receita Adicional Projetada (R$)</h4>", unsafe_allow_html=True)
    projected_revenue = st.slider("", min_value=50000, max_value=150000, value=80000, step=5000, key="projected_revenue")
    
    st.markdown("<h4 style='color: #0066CC;'>Custos Operacionais Anuais (R$)</h4>", unsafe_allow_html=True)
    operational_costs = st.slider("", min_value=5000, max_value=30000, value=10000, step=1000, key="operational_costs")
    
    st.markdown("<h4 style='color: #0066CC;'>Anos de Projeção</h4>", unsafe_allow_html=True)
    projection_years = st.slider("", min_value=1, max_value=10, value=5, step=1, key="projection_years")
    
    # Cálculo do ROI
    profit = projected_revenue - operational_costs
    total_profit_over_time = profit * projection_years
    roi = (total_profit_over_time / investment_cost) * 100
    
    # Anos para recuperar o investimento
    payback_years = investment_cost / profit if profit > 0 else float('inf')
    
    # Mostrar resultados
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("ROI Projetado", f"{roi:.2f}%")
    with col2:
        st.metric("Lucro Anual", f"R$ {profit:,.2f}")
    with col3:
        st.metric("Tempo de Retorno (Anos)", f"{payback_years:.2f}")
    
    # Gráfico de fluxo de caixa ao longo do tempo
    years = list(range(0, projection_years + 1))
    cash_flow = [-investment_cost]
    
    for _ in range(projection_years):
        cash_flow.append(cash_flow[-1] + profit)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=years,
        y=cash_flow,
        mode='lines+markers',
        name='Fluxo de Caixa',
        line=dict(color='#0066CC', width=3)
    ))
    
    fig.add_hline(y=0, line_dash="solid", line_color="red", line_width=1)
    
    fig.update_layout(
        title="Fluxo de Caixa Acumulado do Investimento ao Longo do Tempo",
        xaxis_title="Anos",
        yaxis_title="Fluxo de Caixa Acumulado (R$)",
        plot_bgcolor="white",
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Avaliação do investimento
    if roi > 20:
        st.success(f"Avaliação: Excelente investimento com ROI de {roi:.2f}% em {projection_years} anos.")
    elif roi > 0:
        st.info(f"Avaliação: Investimento positivo com ROI de {roi:.2f}% em {projection_years} anos.")
    else:
        st.error(f"Avaliação: Investimento não recomendado com ROI negativo de {roi:.2f}% em {projection_years} anos.")

# Aba de Simulação de ROI com Monte Carlo
with tab4:
    st.header("Simulação de Cenários de ROI")
    st.markdown("""
    Simulações Monte Carlo para avaliar o desempenho do sistema em diferentes cenários 
    (otimista, pessimista e realista), considerando incertezas no mercado.
    """)
    
    # Parâmetros para a simulação
    st.markdown("<h4 style='color: #0066CC;'>Custo do Investimento (R$)</h4>", unsafe_allow_html=True)
    mc_investment_cost = st.slider("", min_value=50000, max_value=200000, value=100000, step=10000, key="mc_investment_cost")
    
    st.markdown("<h4 style='color: #0066CC;'>Média da Receita Adicional Projetada (R$)</h4>", unsafe_allow_html=True)
    mc_mean_revenue = st.slider("", min_value=50000, max_value=150000, value=80000, step=5000, key="mc_mean_revenue")
    
    st.markdown("<h4 style='color: #0066CC;'>Desvio Padrão da Receita (%)</h4>", unsafe_allow_html=True)
    mc_revenue_std_pct = st.slider("", min_value=5, max_value=30, value=15, step=1, key="mc_revenue_std_pct")
    
    st.markdown("<h4 style='color: #0066CC;'>Média dos Custos Operacionais (R$)</h4>", unsafe_allow_html=True)
    mc_mean_costs = st.slider("", min_value=5000, max_value=30000, value=10000, step=1000, key="mc_mean_costs")
    
    st.markdown("<h4 style='color: #0066CC;'>Desvio Padrão dos Custos (%)</h4>", unsafe_allow_html=True)
    mc_costs_std_pct = st.slider("", min_value=5, max_value=30, value=10, step=1, key="mc_costs_std_pct")
    
    st.markdown("<h4 style='color: #0066CC;'>Anos de Projeção</h4>", unsafe_allow_html=True)
    mc_projection_years = st.slider("", min_value=1, max_value=10, value=5, step=1, key="mc_projection_years")
    
    st.markdown("<h4 style='color: #0066CC;'>Número de Simulações</h4>", unsafe_allow_html=True)
    num_simulations = st.slider("", min_value=100, max_value=10000, value=1000, step=100, key="num_simulations")
    
    # Converter os percentuais para valores
    mc_revenue_std = mc_mean_revenue * (mc_revenue_std_pct / 100)
    mc_costs_std = mc_mean_costs * (mc_costs_std_pct / 100)
    
    # Realizar simulações Monte Carlo
    np.random.seed(42)
    annual_revenues = np.random.normal(mc_mean_revenue, mc_revenue_std, num_simulations)
    annual_costs = np.random.normal(mc_mean_costs, mc_costs_std, num_simulations)
    annual_profits = annual_revenues - annual_costs
    total_profits = annual_profits * mc_projection_years
    rois = (total_profits / mc_investment_cost) * 100
    
    # Percentis para cenários
    percentiles = [10, 50, 90]  # Pessimista, Realista, Otimista
    roi_scenarios = np.percentile(rois, percentiles)
    
    # Payback periods em anos
    payback_periods = np.zeros(num_simulations)
    for i in range(num_simulations):
        if annual_profits[i] <= 0:
            payback_periods[i] = float('inf')
        else:
            payback_periods[i] = mc_investment_cost / annual_profits[i]
    
    avg_payback = np.mean(payback_periods[payback_periods < float('inf')])
    
    # Probabilidade de ROI positivo
    prob_positive_roi = np.mean(rois > 0) * 100
    
    # Mostrar resultados em colunas
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("ROI Médio", f"{np.mean(rois):.2f}%")
    with col2:
        st.metric("Probabilidade de ROI Positivo", f"{prob_positive_roi:.2f}%")
    with col3:
        st.metric("Payback Médio (Anos)", f"{avg_payback:.2f}")
    with col4:
        st.metric("Desvio Padrão do ROI", f"{np.std(rois):.2f}%")
    
    # Cenários
    st.markdown("### Cenários de ROI")
    scenario_col1, scenario_col2, scenario_col3 = st.columns(3)
    with scenario_col1:
        st.metric("Cenário Pessimista (10%)", f"{roi_scenarios[0]:.2f}%")
    with scenario_col2:
        st.metric("Cenário Realista (50%)", f"{roi_scenarios[1]:.2f}%")
    with scenario_col3:
        st.metric("Cenário Otimista (90%)", f"{roi_scenarios[2]:.2f}%")
    
    # Histograma do ROI
    fig = px.histogram(
        x=rois,
        nbins=50,
        labels={"x": "ROI (%)"},
        title="Distribuição do ROI nas Simulações",
        color_discrete_sequence=['#0066CC']
    )
    
    fig.add_vline(x=0, line_dash="dash", line_color="red", line_width=1)
    
    fig.update_layout(
        xaxis_title="ROI (%)",
        yaxis_title="Frequência",
        plot_bgcolor="white",
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Avaliação do investimento baseada nas simulações
    if prob_positive_roi > 80:
        st.success(f"Avaliação: Investimento de baixo risco com {prob_positive_roi:.2f}% de chance de ROI positivo.")
    elif prob_positive_roi > 50:
        st.info(f"Avaliação: Investimento de risco moderado com {prob_positive_roi:.2f}% de chance de ROI positivo.")
    else:
        st.error(f"Avaliação: Investimento de alto risco com apenas {prob_positive_roi:.2f}% de chance de ROI positivo.")
