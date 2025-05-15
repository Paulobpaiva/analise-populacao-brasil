# analise_populacao.py - Versão adaptada para seu formato
import pandas as pd
import os
from datetime import datetime

def setup_project():
    """Cria a estrutura de diretórios do projeto"""
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    os.makedirs('notebooks', exist_ok=True)
    os.makedirs('reports', exist_ok=True)

def clean_data():
    """Versão específica para o formato do seu arquivo"""
    try:
        # Lê o arquivo ignorando as primeiras linhas de cabeçalho
        df = pd.read_csv('data/raw/populacao_bruta.csv', sep=';', encoding='utf-8', skiprows=3, nrows=1)
        
        # Remove coluna vazia inicial
        df = df.drop(columns=df.columns[0])
        
        # Transpõe os dados (transforma colunas em linhas)
        df = df.T.reset_index()
        
        # Renomeia colunas
        df.columns = ['Ano', 'População']
        
        # Remove linhas com anos vazios
        df = df[df['Ano'].str.isnumeric()]
        
        # Converte tipos
        df['Ano'] = df['Ano'].astype(int)
        df['População'] = df['População'].astype(str).str.replace('.', '').astype(int)
        
        # Ordena por ano
        df = df.sort_values('Ano')
        
        # Salva dados limpos
        df.to_csv('data/processed/populacao_limpa.csv', index=False)
        return df
    
    except Exception as e:
        print(f"\nErro detalhado: {str(e)}")
        print("\n*** Vamos tentar uma abordagem alternativa ***")
        
        # Tenta ler como texto e processar manualmente
        try:
            with open('data/raw/populacao_bruta.csv', 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Encontra a linha com os dados
            data_line = None
            for line in lines:
                if line.startswith('"Brasil"'):
                    data_line = line
                    break
            
            if data_line:
                # Extrai anos (linha 3)
                years = lines[2].replace('"";', '').replace('"', '').strip().split(';')
                # Extrai valores
                values = data_line.replace('"Brasil";', '').replace('"', '').strip().split(';')
                
                # Cria DataFrame
                df = pd.DataFrame({'Ano': years, 'População': values})
                
                # Limpeza
                df = df[df['Ano'].str.isnumeric()]
                df['Ano'] = df['Ano'].astype(int)
                df['População'] = df['População'].str.replace('.', '').astype(int)
                df = df.sort_values('Ano')
                
                # Salva
                df.to_csv('data/processed/populacao_limpa.csv', index=False)
                return df
        
        except Exception as e2:
            print(f"Erro na abordagem alternativa: {e2}")
            return None

if __name__ == "__main__":
    print("Iniciando Sprint 1 - Versão Adaptada")
    setup_project()
    
    df = clean_data()
    
    if df is not None:
        print("\nDados processados com sucesso!")
        print("Primeiras linhas:")
        print(df.head())
        print("\nÚltimas linhas:")
        print(df.tail())
        print(f"\nSalvo em: data/processed/populacao_limpa.csv")
        
        # Gera relatório
        with open('reports/sprint1_report.md', 'w') as f:
            f.write(f"# Relatório Sprint 1\n\n")
            f.write(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## Dados Processados (2001-2024)\n```\n{df.to_markdown()}\n```")
        
        print("\nPronto para a Sprint 2! Execute: python analise_exploratoria.py")
    else:
        print("\n*** ATENÇÃO ***")
        print("Não foi possível processar o arquivo.")
        print("Por favor, envie o arquivo completo para que eu possa ajudar melhor.")