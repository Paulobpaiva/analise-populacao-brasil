import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime

# Configurações de estilo CORRIGIDAS
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 12
sns.set_palette("husl")

def load_clean_data():
    """Carrega os dados processados da Sprint 1"""
    try:
        df = pd.read_csv('data/processed/populacao_limpa.csv')
        print("Dados carregados com sucesso!")
        return df
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return None

def calculate_growth_metrics(df):
    """Calcula métricas de crescimento"""
    print("\nCalculando métricas de crescimento...")
    
    df['Crescimento_Anual'] = df['População'].pct_change() * 100
    df['Crescimento_Acumulado'] = (df['População'] / df.iloc[0]['População'] - 1) * 100
    df['Media_Movel_5_Anos'] = df['Crescimento_Anual'].rolling(window=5).mean()
    
    return df

def generate_visualizations(df):
    """Gera visualizações profissionais"""
    print("\nGerando visualizações...")
    
    # 1. Evolução Populacional Total
    plt.figure()
    ax = sns.lineplot(x='Ano', y='População', data=df, marker='o', linewidth=2.5)
    plt.title('Evolução da População Brasileira (2001-2024)', fontsize=16, pad=20)
    plt.ylabel('População', fontsize=12)
    plt.xlabel('Ano', fontsize=12)
    ax.yaxis.set_major_formatter(lambda x, _: f'{x/1e6:.1f}M')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig('reports/evolucao_populacional.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Taxa de Crescimento Anual
    plt.figure()
    ax = sns.barplot(x='Ano', y='Crescimento_Anual', data=df[1:])
    plt.title('Taxa de Crescimento Populacional Anual (%)', fontsize=16, pad=20)
    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('Variação Anual (%)', fontsize=12)
    plt.xticks(rotation=45)
    
    for p in ax.patches:
        ax.annotate(f"{p.get_height():.2f}%", 
                   (p.get_x() + p.get_width() / 2., p.get_height()), 
                   ha='center', va='center', 
                   xytext=(0, 10), 
                   textcoords='offset points',
                   fontsize=10)
    
    plt.axhline(0, color='black', linewidth=0.8)
    plt.tight_layout()
    plt.savefig('reports/taxa_crescimento_anual.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Comparação Crescimento vs Média Móvel
    plt.figure()
    sns.lineplot(x='Ano', y='Crescimento_Anual', data=df[1:], 
                 label='Crescimento Anual', linewidth=2.5)
    sns.lineplot(x='Ano', y='Media_Movel_5_Anos', data=df[1:], 
                 label='Média Móvel (5 anos)', linewidth=2.5, linestyle='--')
    plt.title('Taxa de Crescimento vs Tendência (Média Móvel 5 anos)', fontsize=16, pad=20)
    plt.xlabel('Ano', fontsize=12)
    plt.ylabel('Variação (%)', fontsize=12)
    plt.axhline(0, color='black', linewidth=0.8)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig('reports/crescimento_vs_tendencia.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_report(df):
    """Gera relatório completo em Markdown"""
    print("\nGerando relatório...")
    
    pop_2001 = df.iloc[0]['População']
    pop_2024 = df.iloc[-1]['População']
    crescimento_total = (pop_2024 - pop_2001) / pop_2001 * 100
    crescimento_medio_anual = df['Crescimento_Anual'][1:].mean()
    ano_maior_crescimento = df.loc[df['Crescimento_Anual'].idxmax()]['Ano']
    
    report = f"""
# Relatório de Análise Exploratória - População Brasileira

**Data da análise**: {datetime.now().strftime('%d/%m/%Y %H:%M')}

## Principais Métricas
- **População em 2001**: {pop_2001:,.0f} habitantes
- **População em 2024**: {pop_2024:,.0f} habitantes
- **Crescimento total (2001-2024)**: {crescimento_total:.2f}%
- **Taxa média anual de crescimento**: {crescimento_medio_anual:.2f}%
- **Ano com maior crescimento**: {ano_maior_crescimento} ({df['Crescimento_Anual'].max():.2f}%)

## Visualizações

### Evolução Populacional
![Evolução](evolucao_populacional.png)

### Taxa de Crescimento Anual
![Crescimento Anual](taxa_crescimento_anual.png)

### Tendência de Crescimento
![Crescimento vs Tendência](crescimento_vs_tendencia.png)
"""
    
    with open('reports/relatorio_analise.md', 'w') as f:
        f.write(report)
    
    df.to_csv('data/processed/populacao_analisada.csv', index=False)

if __name__ == "__main__":
    print("Iniciando Sprint 2 - Análise Exploratória (Versão Corrigida)")
    
    df = load_clean_data()
    
    if df is not None:
        df = calculate_growth_metrics(df)
        generate_visualizations(df)
        generate_report(df)
        
        print("\nSprint 2 concluída com sucesso!")
        print("Visualizações salvas em: reports/")
        print("Relatório completo: reports/relatorio_analise.md")