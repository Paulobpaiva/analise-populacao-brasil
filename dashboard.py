import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from ipywidgets import interact
import ipywidgets as widgets

# Configurações
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# 1. Carregar dados
df = pd.read_csv('data/processed/populacao_analisada.csv')

# 2. Análise por Décadas
def analyze_by_decade(df):
    df['Década'] = (df['Ano'] // 10) * 10
    decade_stats = df.groupby('Década').agg({
        'População': ['min', 'max', 'mean'],
        'Crescimento_Anual': 'mean'
    }).round(2)
    decade_stats.columns = ['Pop_Mínima', 'Pop_Máxima', 'Pop_Média', 'Crescimento_Médio']
    return decade_stats

# 3. Projeção Futura
def future_projection(df, years_to_project=5):
    X = df['Ano'].values.reshape(-1, 1)
    y = df['População'].values
    
    # Modelo polinomial (grau 2)
    poly = PolynomialFeatures(degree=2)
    X_poly = poly.fit_transform(X)
    
    model = LinearRegression()
    model.fit(X_poly, y)
    
    future_years = np.arange(df['Ano'].max() + 1, df['Ano'].max() + years_to_project + 1)
    future_X = poly.transform(future_years.reshape(-1, 1))
    projections = model.predict(future_X)
    
    return pd.DataFrame({
        'Ano': future_years,
        'População': projections.round(0),
        'Projeção': True
    })

# 4. Dashboard Interativo
def create_dashboard(df):
    # Preparar dados
    projections = future_projection(df)
    df['Projeção'] = False
    full_data = pd.concat([df, projections])
    
    # Gráfico 1: Evolução Populacional
    fig1 = px.line(
        full_data, x='Ano', y='População',
        title='População Brasileira: Histórico e Projeção',
        labels={'População': 'População (milhões)'},
        hover_data={'População': ':,.0f'},
        color='Projeção',
        color_discrete_map={False: 'blue', True: 'red'}
    )
    fig1.update_traces(line_width=2.5)
    fig1.update_layout(hovermode='x unified')
    
    # Gráfico 2: Crescimento Anual
    fig2 = px.bar(
        df[1:], x='Ano', y='Crescimento_Anual',
        title='Taxa de Crescimento Anual (%)',
        labels={'Crescimento_Anual': 'Variação %'},
        text_auto='.2f'
    )
    fig2.update_traces(marker_color='green')
    fig2.add_hline(y=df['Crescimento_Anual'].mean(), line_dash="dash")
    
    # Décadas
    decade_stats = analyze_by_decade(df)
    
    # Layout do Dashboard
    fig = go.Figure()
    fig.add_trace(fig1.data[0])
    fig.add_trace(fig1.data[1])
    fig.update_layout(
        title='Dashboard População Brasileira',
        template='plotly_white'
    )
    
    # Salvar HTML
    fig1.write_html('reports/dashboard_evolucao.html')
    fig2.write_html('reports/dashboard_crescimento.html')
    
    return fig1, fig2, decade_stats

# 5. Relatório Completo
def generate_final_report(df, decade_stats):
    projections = future_projection(df)
    pop_2024 = df[df['Ano'] == 2024]['População'].values[0]
    pop_2029 = projections.iloc[-1]['População']
    growth = ((pop_2029 - pop_2024) / pop_2024 * 100).round(2)
    
    report = f"""
# Relatório Final - Análise Populacional Brasileira

**Data**: {datetime.now().strftime('%d/%m/%Y %H:%M')}

## Destaques
- População projetada para 2029: {pop_2029:,.0f} habitantes
- Crescimento esperado (2024-2029): {growth}%
- Década com maior crescimento médio: {decade_stats['Crescimento_Médio'].idxmax()}s

## Dashboard Interativo
[Visualizar Evolução Populacional](dashboard_evolucao.html)
[Visualizar Taxas de Crescimento](dashboard_crescimento.html)

## Análise por Década
{decade_stats.to_markdown()}

## Métodos Utilizados
- Modelo de projeção: Regressão Polinomial (2º grau)
- Fonte dos dados: IBGE
- Período analisado: {df['Ano'].min()} a {df['Ano'].max()}
"""
    
    with open('reports/relatorio_final.md', 'w') as f:
        f.write(report)
    
    # Salva dados completos
    full_data = pd.concat([df, future_projection(df, 10)])
    full_data.to_csv('data/processed/populacao_completa.csv', index=False)

if __name__ == "__main__":
    print("Iniciando Sprint 3 - Dashboard e Análise Avançada")
    
    # Criar dashboard
    fig1, fig2, decade_stats = create_dashboard(df)
    
    # Gerar relatório final
    generate_final_report(df, decade_stats)
    
    print("\nSprint 3 concluída com sucesso!")
    print("Arquivos gerados:")
    print("- reports/dashboard_evolucao.html")
    print("- reports/dashboard_crescimento.html")
    print("- reports/relatorio_final.md")
    print("\nPronto para publicação no GitHub!")