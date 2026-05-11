import pandas as pd
import os
from database import load_database


# ========= EXTRACT =========
def extract(path):
    print('lendo o arquivo')

    if path.endswith('.xlsx'):
        df = pd.read_excel(path)
    else:
        df = pd.read_csv(path, sep=';', encoding='latin1')

    print(f'Dados carregados: {df.shape[0]} linhas, {df.shape[1]} colunas')
    return df


# ========= TRANSFORM =========
def transform(df):
    print('transformando os dados')

    # remover duplicados
    df = df.drop_duplicates()

    # limpar textos principais
    text_cols = ['nmProjeto', 'nmSujeito', 'nmSetor']

    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.upper()

    # converter valores monetários
    if 'VlDolar' in df.columns:
        df['VlDolar'] = (
            df['VlDolar']
            .astype(str)
            .str.replace(',', '.', regex=False)
        )
        df['VlDolar'] = pd.to_numeric(df['VlDolar'], errors='coerce')

    # converter datas (formato BR)
    date_columns = [
        'dtRecebimento',
        'dtValidadeRecomendacao',
        'dtReuniaoNegociacao',
        'dtAprovDiretoria',
        'dtAprovacaoSenado',
        'dtAssinatura',
        'dtPrimeiraAmortizacao',
        'dtUltimaAmortizacao'
    ]

    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce', dayfirst=True)

    # feature engineering
    if 'dtRecebimento' in df.columns:
        df['ano_recebimento'] = df['dtRecebimento'].dt.year

    print('transformação concluida')
    return df


# ========= LOAD FILE =========
def load_file(df, output_path):
    print('saving csv trated')

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)

    print(f'arquivo foi salvo em: {output_path}')


# ========= RUN ETL =========
def run_etl():
    input_path = '../data/raw/dados_2025-02-05.xlsx'
    output_path = '../data/processed/cofiex_dadostratados.csv'

    df = extract(input_path)
    df = transform(df)
    load_file(df, output_path)

    # salvar no banco
    load_database(df)

    print('\netl finalizado')


# ========= EXECUTE =========
if __name__ == "__main__":
    run_etl()