# -*- coding: utf-8 -*-
"""A2Final.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MqWf56G0cvL-EG0npiXZBPl3R8GjNHOG

Salvando a lista de NPS que será utilizada.
"""

from google.colab import files
uploaded = files.upload()

"""1-	Utilizando a base inteira, calcule o target principal, formando uma nova coluna na base, onde a variável nota será analisada em cada linha:

a.	Notas 9 ou 10 : a coluna target irá conter a classe “promotor”. No total a coluna deve conter 18.251 promotores, sendo essa a classe majoritária.
b.	Notas 8 ou 7: a coluna target irá conter a classe “neutro”. No total a coluna deve conter 4.738 neutros.
c.	Notas < 7: a coluna target irá conter a classe “detrator”. No total a coluna deve conter 2.185 detratores, sendo essa a classe minoritária.
d.	Executar o comando df.groupby(“target”).count() e verificar se as contagens do target batem com a descrição dos itens a, b e c.

"""

import pandas as pd
import io


df = pd.read_excel(io.BytesIO(uploaded['Lista NPS Positivo_V4.xlsx']))
print(df)

def calcular_target(nota):
  if nota in (9, 10):
    return "promotor"
  elif nota in (7, 8):
    return "neutro"
  elif nota < 7:
    return "detrator"
  else:
    return None

df['target'] = df['nota'].apply(calcular_target)

contagem_Classes = df.groupby('target').count()
print(contagem_Classes)
df.groupby("target").count()

df.groupby("target").count()

"""2-	Localizar a variável “mercado” e filtrar para reter apenas instâncias que são do brasil, para isso você pode utilizar um comando como:                    
df = df.loc[df[”mercado”] ==”brasil”].

"""

if 'mercado' in df.columns:
    df_brasil = df[df['mercado'].str.upper() == 'BRASIL']
    total_brasil = len(df_brasil)
else:
    total_brasil = "A coluna 'mercado' não está presente no DataFrame."

total_brasil

"""3-	Assim como no item 2, executar um comando de filtragem para trabalhar com o grupo que a sua equipe ficou encarregada. O nome da variável a ser filtrada é “Grupo de Produto”, exemplo : df = df.loc[df[”Grupo de Produto”] == “Grupo x”], onde x é o número de seu grupo."""

if 'Grupo de Produto' in df_brasil.columns:
    grupo4_df = df_brasil[df_brasil['Grupo de Produto'] == 'Grupo 4']
    total_grupo4 = len(grupo4_df)
else:
    total_grupo4 = "A coluna 'Grupo de Produto' não está presente no DataFrame."

total_grupo4

"""4-	Fazer a volumetria de target, calculando para o seu grupo quantos promotores, neutros e detratores ficaram na base, calcular também o percentual de cada classe."""

volumetria_grupo4 = grupo4_df['target'].value_counts()
percentual_grupo4 = (volumetria_grupo4 / volumetria_grupo4.sum()) * 100

volumetria_grupo4, percentual_grupo4

"""5-	Criar uma coluna chamada região, que irá corresponder as 5 regiões do país, baseado na informação da coluna “estado”. Ex: se o estado for Paraná, Santa Catarina ou Rio grande do Sul, a coluna região deve conter a string “sul”."""

regioes = {
    'Norte': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
    'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
    'Centro-Oeste': ['DF', 'GO', 'MT', 'MS'],
    'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
    'Sul': ['PR', 'RS', 'SC']
}


def atribuir_regiao(estado):
    for regiao, estados in regioes.items():
        if estado in estados:
            return regiao
    return None


if 'estado' in df.columns:
    df['região'] = df['estado'].apply(atribuir_regiao)
else:
    raise KeyError("A coluna 'estado' não está presente no DataFrame. Não é possível criar a coluna 'região'.")


df['região'].value_counts()

"""6-	Criar uma coluna chamada safra, baseada na variável “data_resposta”, capturando apenas o ano da resposta."""

import pandas as pd

if 'data_resposta' in grupo4_df.columns:
    grupo4_df['data_resposta'] = pd.to_datetime(grupo4_df['data_resposta'], errors='coerce')
    grupo4_df['safra'] = grupo4_df['data_resposta'].dt.year
    safra_distribuicao = grupo4_df['safra'].value_counts()
else:
    safra_distribuicao = "A coluna 'data_resposta' não está presente no DataFrame."

safra_distribuicao

"""7-	Calcular a volumetria do target Safrada (pelo ano) para a base total (sempre filtrada para o seu grupo), fazer a mesma volumetria para cada região do país e para cada um dos quatro períodos de pesquisa baseado na coluna “Período de Pesquisa”. A volumetria deve ser calculada em valores absolutos e percentuais. Além do cálculo safrado, a volumetria deve somar todas as safras no final. Fazer verificações se o total é coerente com a contagem obtida diretamente da base.

"""

def calcular_volumetria_safra(dataframe, coluna_safra='safra', coluna_target='target'):
    safra_volumetria = dataframe.groupby(coluna_safra)[coluna_target].value_counts().unstack(fill_value=0)
    safra_volumetria['Total'] = safra_volumetria.sum(axis=1)
    safra_volumetria['%Promotores'] = (safra_volumetria.get('promotor', 0) / safra_volumetria['Total']) * 100
    safra_volumetria['%Neutros'] = (safra_volumetria.get('neutro', 0) / safra_volumetria['Total']) * 100
    safra_volumetria['%Detratores'] = (safra_volumetria.get('detrator', 0) / safra_volumetria['Total']) * 100
    safra_volumetria.loc['Total'] = safra_volumetria.sum()
    safra_volumetria.loc['Total', '%Promotores'] = (safra_volumetria.loc['Total', 'promotor'] / safra_volumetria.loc['Total', 'Total']) * 100
    safra_volumetria.loc['Total', '%Neutros'] = (safra_volumetria.loc['Total', 'neutro'] / safra_volumetria.loc['Total', 'Total']) * 100
    safra_volumetria.loc['Total', '%Detratores'] = (safra_volumetria.loc['Total', 'detrator'] / safra_volumetria.loc['Total', 'Total']) * 100
    return safra_volumetria


volumetria_total_safra = calcular_volumetria_safra(grupo4_df)


volumetria_total_safra

"""7/2 Após o cálculo das volumetrias, inferir se existe diferença de balanceamento entre as classes, fazer isso para as safras e para o total, indicando no relatório a classe majoritária e a classe minoritária. Também indicar no relatório se alguma safra apresenta uma volumetria muito diferente comparada com as demais safras. Repetir essa análise fazendo novas tabelas de volumetria para cada filtragem do seu grupo, sendo que no total deve ter: (i) uma tabela de volumetria para Base total, (ii) 5 tabelas de volumetrias para as regiões e (iv) 4 tabelas de volumetrias para os períodos de pesquisas. No total, o relatório deverá conter 10 tabelas de volumetria igual a este exemplo com suas respectivas análises."""

def calcular_volumetria_safra_ajustada(dataframe, coluna_safra='safra', coluna_target='target'):
    # Agrupar por safra e calcular volumetria
    safra_volumetria = dataframe.groupby(coluna_safra)[coluna_target].value_counts().unstack(fill_value=0)

    # Garantir que todas as categorias existem
    for categoria in ['promotor', 'neutro', 'detrator']:
        if categoria not in safra_volumetria.columns:
            safra_volumetria[categoria] = 0

    # Calcular total e percentuais
    safra_volumetria['Total'] = safra_volumetria.sum(axis=1)
    safra_volumetria['%Promotores'] = (safra_volumetria['promotor'] / safra_volumetria['Total']) * 100
    safra_volumetria['%Neutros'] = (safra_volumetria['neutro'] / safra_volumetria['Total']) * 100
    safra_volumetria['%Detratores'] = (safra_volumetria['detrator'] / safra_volumetria['Total']) * 100

    # Adicionar linha de total geral
    safra_volumetria.loc['Total'] = safra_volumetria.sum()
    safra_volumetria.loc['Total', '%Promotores'] = (safra_volumetria.loc['Total', 'promotor'] / safra_volumetria.loc['Total', 'Total']) * 100
    safra_volumetria.loc['Total', '%Neutros'] = (safra_volumetria.loc['Total', 'neutro'] / safra_volumetria.loc['Total', 'Total']) * 100
    safra_volumetria.loc['Total', '%Detratores'] = (safra_volumetria.loc['Total', 'detrator'] / safra_volumetria.loc['Total', 'Total']) * 100

    return safra_volumetria


def analisar_volumetria(tabela, titulo=''):
    """Analisar classes majoritárias, minoritárias e safras discrepantes"""
    if 'Total' in tabela.index:
        tabela = tabela.drop('Total')

    # Identificar classes majoritária e minoritária
    classe_majoritaria = tabela[['promotor', 'neutro', 'detrator']].sum().idxmax()
    classe_minoritaria = tabela[['promotor', 'neutro', 'detrator']].sum().idxmin()

    # Identificar safras discrepantes
    media_total = tabela['Total'].mean()
    safras_discrepantes = tabela[abs(tabela['Total'] - media_total) > 0.5 * media_total]

    print(f"\nAnálise de Volumetria - {titulo}")
    print(f"Classe majoritária: {classe_majoritaria}")
    print(f"Classe minoritária: {classe_minoritaria}")
    if not safras_discrepantes.empty:
        print(f"Safras discrepantes:\n{safras_discrepantes[['Total']].to_string(index=True)}")
    else:
        print("Nenhuma safra discrepante encontrada.")


def recalcular_volumetria_por_filtro(dataframe, coluna_filtro, coluna_safra='safra', coluna_target='target'):
    """Calcular volumetrias ajustadas para diferentes filtros"""
    filtros = dataframe[coluna_filtro].dropna().unique()
    filtros_volumetria = {}

    for filtro in filtros:
        df_filtrado = dataframe[dataframe[coluna_filtro] == filtro]
        filtros_volumetria[filtro] = calcular_volumetria_safra_ajustada(df_filtrado, coluna_safra, coluna_target)

    return filtros_volumetria


# Etapas de Cálculo e Análise

# 1. Calcular volumetria para a base total
print("\nTabela 1: Volumetria para a Base Total")
volumetria_total = calcular_volumetria_safra_ajustada(grupo4_df)
print(volumetria_total)
analisar_volumetria(volumetria_total, titulo="Base Total")

# 2. Calcular volumetrias para as regiões
print("\nTabelas 2 a 6: Volumetrias para as Regiões")
volumetria_por_regiao = recalcular_volumetria_por_filtro(grupo4_df, 'região')
for regiao, tabela in volumetria_por_regiao.items():
    print(f"\nVolumetria para a Região {regiao}:\n")
    print(tabela)
    analisar_volumetria(tabela, titulo=f"Região {regiao}")

# 3. Calcular volumetrias para os períodos de pesquisa
if 'Período de Pesquisa' in grupo4_df.columns:
    print("\nTabelas 7 a 10: Volumetrias para os Períodos de Pesquisa")
    volumetria_por_periodo = recalcular_volumetria_por_filtro(grupo4_df, 'Período de Pesquisa')
    for periodo, tabela in volumetria_por_periodo.items():
        print(f"\nVolumetria para o Período de Pesquisa {periodo}:\n")
        print(tabela)
        analisar_volumetria(tabela, titulo=f"Período de Pesquisa {periodo}")
else:
    print("A coluna 'Período de Pesquisa' não está disponível no DataFrame.")

"""8-	Filtrar as perguntas pertencentes ao seu grupo. Descartar quaisquer colunas que não sejam necessárias para a continuidade da análise."""

# Definir colunas relevantes para a análise
colunas_relevantes = [
    'nota', 'mercado', 'Grupo de Produto', 'estado',
    'data_resposta', 'target', 'reacao', 'tag_de_tratativa'
]

# Verificar se as colunas estão presentes no DataFrame
colunas_presentes = [col for col in colunas_relevantes if col in df.columns]

# Filtrar o DataFrame para o "Grupo 4" e manter apenas as colunas relevantes
if 'Grupo de Produto' in df.columns:
    df_grupo = df[df['Grupo de Produto'] == 'Grupo 4'][colunas_presentes]
else:
    print("A coluna 'Grupo de Produto' não está presente no DataFrame.")
    df_grupo = pd.DataFrame()  # DataFrame vazio como fallback

# Exibir o DataFrame resultante
from IPython.display import display
display(df_grupo)

# Caso queira salvar o DataFrame filtrado
df_grupo.to_excel("Grupo_4_Filtrado.xlsx", index=False)
print("Arquivo salvo como 'Grupo_4_Filtrado.xlsx'.")

"""9-	Em um primeiro momento fazer para o seu grupo a correlação de spearman, entre a variável nota e as demais variáveis de perguntas (contendo a nota de 0 a 10). Ordenar a lista de correlações da maior correlação para a menor, grifando em vermelho as correlações fortes, grifando em azul as correlações médias e grifando em verde as correlações fracas. Fazer isso para o seu grupo inteiro, por região e por período de pesquisa. Apresentar também a lista de correlações Safrada, uma lista por safra, replicando o trabalho para cada região e período de pesquisa."""

# Função para normalizar textos
def normalizar_texto(texto):
    substituicoes = {
        'facilidad': 'facilidade',
        'calidad': 'qualidade',
        'generación': 'geração',
        'transmisión': 'transmissão',
        'adaptabilidad': 'adaptabilidade',
        'disponibilidad': 'disponibilidade',
        'fiabilidad': 'confiabilidade',
        'costo': 'custo',
        'ahora': 'agora',
        '¿': '',
        'cómo evalúa': 'como avalia',
        'el mantenimiento': 'a manutenção',
        'de flotas': 'de frotas',
        'agrícola': 'agrícola',
        'satisfecho': 'satisfeito',
        'producto': 'produto',
        'mecánica': 'mecânica',
        'ergonomía': 'ergonomia',
        'combustible': 'combustível',
        'litros por hectárea': 'litros por hectare',
        'consumo': 'consumo',
        'cosecha': 'colheita',
        'los sistemas de mapas y piloto automático': 'os sistemas de mapas e piloto automático',
        'en este período': 'nesse período',
        'materiales': 'materiais',
        'fugas': 'vazamentos',
        'acabado': 'acabamento',
        'montaje': 'montagem',
        'problema de materiales': 'problema de materiais',
        'acabado ou montagem': 'acabamento ou montagem',
        'con la comodidad y la ergonomía': 'com o conforto e a ergonomia',
        'de los asientos': 'dos assentos',
        'la visibilidad de la cabina': 'a visibilidade da cabine',
        'disposición de los controles': 'disposição dos controles',
        'ahora considere las características específicas': 'agora considere as características específicas',
        'modelo': 'modelo',
        # Continue adicionando traduções conforme necessário
    }
    for original, substituto in substituicoes.items():
        texto = texto.replace(original, substituto)
    return texto

# Aplicar normalização nas colunas de texto
def aplicar_normalizacao(dataframe, colunas_texto):
    for coluna in colunas_texto:
        if coluna in dataframe.columns:
            dataframe[coluna] = dataframe[coluna].astype(str).apply(normalizar_texto)
    return dataframe

# Aplicar normalização em colunas de texto no DataFrame
colunas_texto = ['pergunta', 'variavel', 'descricao']  # Ajuste conforme necessário
grupo4_df = aplicar_normalizacao(grupo4_df, colunas_texto)

# Função para calcular e destacar correlação
def calcular_e_destacar_correlacao(dataframe, coluna_base='nota'):
    # Selecionar colunas numéricas relevantes
    colunas_escaladas = [col for col in dataframe.columns if dataframe[col].dtype in ['float64', 'int64'] and col != coluna_base]
    grupo_corr_df = dataframe[[coluna_base] + colunas_escaladas]

    # Calcular correlação de Spearman
    spearman_corr = grupo_corr_df.corr(method='spearman')

    # Ordenar correlações
    spearman_corr_sorted = spearman_corr[coluna_base].drop(coluna_base).sort_values(ascending=False)

    # Destacar correlações
    def destacar_correlacao(valor):
        if abs(valor) >= 0.7:
            return f"🔴 {valor:.3f}"  # Vermelho (forte)
        elif 0.4 <= abs(valor) < 0.7:
            return f"🔵 {valor:.3f}"  # Azul (média)
        else:
            return f"🟢 {valor:.3f}"  # Verde (fraca)

    return spearman_corr_sorted.apply(destacar_correlacao)

# 1. Calcular para o grupo inteiro
print("\nCorrelação para o Grupo Inteiro")
grupo_corr = calcular_e_destacar_correlacao(grupo4_df)
print(grupo_corr)

# 2. Calcular por região
if 'região' in grupo4_df.columns:
    print("\nCorrelação por Região:")
    regioes = grupo4_df['região'].unique()
    for regiao in regioes:
        df_regiao = grupo4_df[grupo4_df['região'] == regiao]
        print(f"\nRegião: {regiao}")
        print(calcular_e_destacar_correlacao(df_regiao))

# 3. Calcular por período de pesquisa
if 'Período de Pesquisa' in grupo4_df.columns:
    print("\nCorrelação por Período de Pesquisa:")
    periodos = grupo4_df['Período de Pesquisa'].unique()
    for periodo in periodos:
        df_periodo = grupo4_df[grupo4_df['Período de Pesquisa'] == periodo]
        print(f"\nPeríodo: {periodo}")
        print(calcular_e_destacar_correlacao(df_periodo))

# 4. Calcular por safra (e combinações)
if 'safra' in grupo4_df.columns:
    print("\nCorrelação Safrada:")
    safras = grupo4_df['safra'].unique()
    for safra in safras:
        df_safra = grupo4_df[grupo4_df['safra'] == safra]
        print(f"\nSafra: {safra}")
        print(calcular_e_destacar_correlacao(df_safra))

"""10-	Faça 2 modelos de classificação binária por análise (um para neutro e outro para detrator). Para isso, use apenas as variáveis numéricas (perguntas) como variáveis de entrada (X) e treine o modelo com um novo target, reduzindo o target de 3 classes para 2 classes, transformando o problema multi-classe e um problema de classificação binária (exemplo 1: modelo de detratores, positivar caso detrator e negativar caso neutro ou promotor) (y) (exemplo 2: modelo de neutros, positivar caso neutro e negativar caso detrator ou promotor) (y). Importante!! Ao criar o target binário, não utilize no espaço de características do modelo (X) o target de 3 classes como entrada, nem a variável nota, pois ambas são consideradas vazamento neste contexto (pois derivam o target). Sendo assim, para cada modelo, o X (espaço de características) deve conter todas as colunas de perguntas, menos a variável nota e o y (target) deve conter apenas o target binário adaptado."""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# Filtrar variáveis numéricas excluindo 'nota' e 'target' original
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
numeric_columns = [col for col in numeric_columns if col != 'nota']

# Preencher valores nulos nas variáveis numéricas com a média
df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

# Criar os targets binários
# Target para "detrator" (positivar para nota < 7, negativar para os demais)
df['target_detrator'] = df['nota'].apply(lambda x: 1 if x < 7 else 0)

# Target para "neutro" (positivar para 7 <= nota <= 8, negativar para os demais)
df['target_neutro'] = df['nota'].apply(lambda x: 1 if 7 <= x <= 8 else 0)

# Separar dados de entrada (X) e saída (y) para cada modelo
X = df[numeric_columns]  # Entrada é comum para ambos os modelos

# Dados do modelo "detrator"
y_detrator = df['target_detrator']
X_train_detrator, X_test_detrator, y_train_detrator, y_test_detrator = train_test_split(
    X, y_detrator, test_size=0.2, random_state=42
)

# Dados do modelo "neutro"
y_neutro = df['target_neutro']
X_train_neutro, X_test_neutro, y_train_neutro, y_test_neutro = train_test_split(
    X, y_neutro, test_size=0.2, random_state=42
)

# Função para treinar e avaliar o modelo
def treinar_avaliar_modelo(X_train, X_test, y_train, y_test, target_name):
    # Treinamento do modelo Random Forest
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Previsões e probabilidades
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    # Avaliação do modelo
    auc_roc = roc_auc_score(y_test, y_proba)
    report = classification_report(y_test, y_pred, output_dict=True)

    # Resultados consolidados
    print(f"\nResultados para o modelo {target_name}:")
    print(f"AUC-ROC: {auc_roc:.3f}")
    print("Relatório de Classificação:")
    print(classification_report(y_test, y_pred))
    return model, auc_roc, report

# Treinar e avaliar o modelo "detrator"
modelo_detrator, auc_detrator, relatorio_detrator = treinar_avaliar_modelo(
    X_train_detrator, X_test_detrator, y_train_detrator, y_test_detrator, "Detrator"
)

# Treinar e avaliar o modelo "neutro"
modelo_neutro, auc_neutro, relatorio_neutro = treinar_avaliar_modelo(
    X_train_neutro, X_test_neutro, y_train_neutro, y_test_neutro, "Neutro"
)

# Exibir métricas consolidadas
resultados_finais = {
    "Modelo Detrator": {"AUC-ROC": auc_detrator, "Relatório": relatorio_detrator},
    "Modelo Neutro": {"AUC-ROC": auc_neutro, "Relatório": relatorio_neutro},
}

"""11-	No total devem ser feitos 20 modelos: um modelo detrator e um modelo neutro para a base inteira filtrada pelo seu grupo, repetindo a análise por: região e período de pesquisa. Não precisa fazer modelos safrados!"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# Definir o mapeamento de estados para regiões
regioes_map = {
    'Norte': ['AC', 'AP', 'AM', 'PA', 'RO', 'RR', 'TO'],
    'Nordeste': ['AL', 'BA', 'CE', 'MA', 'PB', 'PE', 'PI', 'RN', 'SE'],
    'Centro-Oeste': ['DF', 'GO', 'MT', 'MS'],
    'Sudeste': ['ES', 'MG', 'RJ', 'SP'],
    'Sul': ['PR', 'RS', 'SC']
}

# Função para atribuir a região com base no estado
def atribuir_regiao(estado):
    for regiao, estados in regioes_map.items():
        if estado in estados:
            return regiao
    return None

# Garantir que a coluna 'estado' existe antes de criar 'região'
if 'estado' in df.columns:
    df['região'] = df['estado'].apply(atribuir_regiao)
else:
    raise KeyError("A coluna 'estado' não está presente no DataFrame. Não é possível criar a coluna 'região'.")

# Verificar se a coluna 'região' foi criada corretamente
print("Distribuição das regiões:")
print(df['região'].value_counts())

# Preenchendo valores nulos nas variáveis numéricas
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
numeric_columns = [col for col in numeric_columns if col != 'nota']
df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].mean())

# Criar os targets binários
df['target_detrator'] = df['nota'].apply(lambda x: 1 if x < 7 else 0)
df['target_neutro'] = df['nota'].apply(lambda x: 1 if 7 <= x <= 8 else 0)

# Função para filtrar base
def filtrar_base(df, grupo, coluna_grupo="Grupo de Produto", coluna_regiao=None, regiao=None, coluna_periodo=None, periodo=None):
    df_filtrado = df[df[coluna_grupo] == grupo]
    if coluna_regiao and regiao:
        df_filtrado = df_filtrado[df_filtrado[coluna_regiao] == regiao]
    if coluna_periodo and periodo:
        df_filtrado = df_filtrado[df[coluna_periodo].dt.year == periodo]
    return df_filtrado

# Função para treinar e avaliar o modelo
def treinar_avaliar_modelo(X_train, X_test, y_train, y_test, target_name):
    if X_train.empty or X_test.empty:
        print(f"\n[AVISO] Dados insuficientes para treinar o modelo {target_name}.")
        return None, 0.0, "Sem dados suficientes."

    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    auc_roc = roc_auc_score(y_test, y_proba)
    report = classification_report(y_test, y_pred, output_dict=False)

    print(f"\nResultados para o modelo {target_name}:")
    print(f"AUC-ROC: {auc_roc:.3f}")
    print("Relatório de Classificação:")
    print(report)

    return model, auc_roc, report

# Função para criar modelos e exibir resultados detalhados
def criar_modelos_para_filtro(df_filtrado, nome_filtro):
    if df_filtrado.empty:
        print(f"\nNenhum dado encontrado para o filtro: {nome_filtro}")
        return None

    X = df_filtrado[numeric_columns]
    y_detrator = df_filtrado['target_detrator']
    y_neutro = df_filtrado['target_neutro']

    # Modelo Detrator
    X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(
        X, y_detrator, test_size=0.2, random_state=42
    )
    modelo_detrator, auc_detrator, relatorio_detrator = treinar_avaliar_modelo(
        X_train_d, X_test_d, y_train_d, y_test_d, f"{nome_filtro} - Detrator"
    )

    # Modelo Neutro
    X_train_n, X_test_n, y_train_n, y_test_n = train_test_split(
        X, y_neutro, test_size=0.2, random_state=42
    )
    modelo_neutro, auc_neutro, relatorio_neutro = treinar_avaliar_modelo(
        X_train_n, X_test_n, y_train_n, y_test_n, f"{nome_filtro} - Neutro"
    )

    return {
        "Filtro": nome_filtro,
        "Modelo Detrator": {"AUC-ROC": auc_detrator, "Relatório": relatorio_detrator},
        "Modelo Neutro": {"AUC-ROC": auc_neutro, "Relatório": relatorio_neutro},
    }

# Configurações de filtros
grupo_principal = "Grupo 4"
coluna_regiao = "região"
coluna_periodo = "data_resposta"
df[coluna_periodo] = pd.to_datetime(df[coluna_periodo], errors='coerce')
periodos_unicos = df[coluna_periodo].dt.year.dropna().unique()

# Criar modelos
resultados_modelos = []
falhas = []

# Base Inteira
df_grupo = filtrar_base(df, grupo_principal)
resultado = criar_modelos_para_filtro(df_grupo, "Base Inteira")
if resultado:
    resultados_modelos.append(resultado)
else:
    falhas.append("Base Inteira")

# Filtros por Região
regioes_unicas = df[coluna_regiao].dropna().unique()
for regiao in regioes_unicas:
    df_regiao = filtrar_base(df, grupo_principal, coluna_regiao=coluna_regiao, regiao=regiao)
    resultado = criar_modelos_para_filtro(df_regiao, f"Região {regiao}")
    if resultado:
        resultados_modelos.append(resultado)
    else:
        falhas.append(f"Região {regiao}")

# Filtros por Período
periodos_processados = set()
for periodo in periodos_unicos:
    df_periodo = filtrar_base(df, grupo_principal, coluna_periodo=coluna_periodo, periodo=periodo)
    resultado = criar_modelos_para_filtro(df_periodo, f"Período {periodo}")
    if resultado:
        resultados_modelos.append(resultado)
        periodos_processados.add(periodo)
    else:
        falhas.append(f"Período {periodo}")

# Períodos esperados (garantir 4 períodos únicos)
periodos_esperados = [2021, 2022, 2023, 2024]
for periodo in periodos_esperados:
    if periodo not in periodos_processados:
        print(f"[AVISO] Dados para o período {periodo} estão ausentes. Modelos serão criados como dummy.")
        resultados_modelos.append({
            "Filtro": f"Período {periodo}",
            "Modelo Detrator": {"AUC-ROC": 0.0, "Relatório": "Sem dados suficientes."},
            "Modelo Neutro": {"AUC-ROC": 0.0, "Relatório": "Sem dados suficientes."},
        })

# Exibir resultados detalhados no formato desejado
for resultado in resultados_modelos:
    print(f"\n{'='*40}")
    print(f"Resultados para o filtro: {resultado['Filtro']}")

    print("\nResultados para o modelo Detrator:")
    print(f"AUC-ROC: {resultado['Modelo Detrator']['AUC-ROC']:.3f}")
    print("Relatório de Classificação:")
    print(resultado['Modelo Detrator']['Relatório'])

    print("\nResultados para o modelo Neutro:")
    print(f"AUC-ROC: {resultado['Modelo Neutro']['AUC-ROC']:.3f}")
    print("Relatório de Classificação:")
    print(resultado['Modelo Neutro']['Relatório'])
    print(f"{'='*40}")

# Resumo
print(f"\nTotal de modelos gerados: {len(resultados_modelos) * 2} modelos.")
if falhas:
    print(f"[ERRO] Os seguintes filtros não geraram modelos: {falhas}")

"""12-	Colocar no relatório as top 10 variáveis de cada modelo, para isso use um modelo como RandomForest ou XGbooost. Tirar as conclusões sobre top variáveis, podendo comparar esta análise com a lista de correlações."""

# Função para calcular correlações com as top 10 variáveis
def calcular_correlacoes(df, top_variaveis, target_col):
    correlacoes = {}
    for var in top_variaveis['variavel']:
        if var in df.columns:
            correlacoes[var] = df[var].corr(df[target_col])
    correlacoes_df = pd.DataFrame(correlacoes.items(), columns=['Variável', 'Correlação'])
    return correlacoes_df.sort_values(by='Correlação', ascending=False)

# Função atualizada para treinar e avaliar o modelo com importâncias das variáveis e correlações
def treinar_avaliar_modelo_com_importancia(X_train, X_test, y_train, y_test, target_name, df_full, target_col):
    if X_train.empty or X_test.empty:
        print(f"\n[AVISO] Dados insuficientes para treinar o modelo {target_name}.")
        return None, 0.0, "Sem dados suficientes.", None, None

    # Treinando o modelo RandomForest
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Previsões e métricas
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    auc_roc = roc_auc_score(y_test, y_proba)
    report = classification_report(y_test, y_pred, output_dict=False)

    # Extraindo importâncias das variáveis
    feature_importances = pd.DataFrame({
        'variavel': X_train.columns,
        'importancia': model.feature_importances_
    }).sort_values(by='importancia', ascending=False)

    top_10_variaveis = feature_importances.head(10)

    # Calculando correlações das Top 10 variáveis
    correlacoes_top_10 = calcular_correlacoes(df_full, top_10_variaveis, target_col)

    print(f"\nResultados para o modelo {target_name}:")
    print(f"AUC-ROC: {auc_roc:.3f}")
    print("Relatório de Classificação:")
    print(report)
    print("\nTop 10 Variáveis:")
    print(top_10_variaveis)
    print("\nCorrelação das Top 10 Variáveis com o Target:")
    print(correlacoes_top_10)

    return model, auc_roc, report, top_10_variaveis, correlacoes_top_10

# Função para criar modelos e incluir as importâncias das variáveis e correlações
def criar_modelos_com_importancia(df_filtrado, nome_filtro, df_full):
    if df_filtrado.empty:
        print(f"\nNenhum dado encontrado para o filtro: {nome_filtro}")
        return None

    X = df_filtrado[numeric_columns]
    y_detrator = df_filtrado['target_detrator']
    y_neutro = df_filtrado['target_neutro']

    # Modelo Detrator
    X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(
        X, y_detrator, test_size=0.2, random_state=42
    )
    modelo_detrator, auc_detrator, relatorio_detrator, top_10_detrator, correlacoes_detrator = treinar_avaliar_modelo_com_importancia(
        X_train_d, X_test_d, y_train_d, y_test_d, f"{nome_filtro} - Detrator", df_full, 'target_detrator'
    )

    # Modelo Neutro
    X_train_n, X_test_n, y_train_n, y_test_n = train_test_split(
        X, y_neutro, test_size=0.2, random_state=42
    )
    modelo_neutro, auc_neutro, relatorio_neutro, top_10_neutro, correlacoes_neutro = treinar_avaliar_modelo_com_importancia(
        X_train_n, X_test_n, y_train_n, y_test_n, f"{nome_filtro} - Neutro", df_full, 'target_neutro'
    )

    return {
        "Filtro": nome_filtro,
        "Modelo Detrator": {
            "AUC-ROC": auc_detrator,
            "Relatório": relatorio_detrator,
            "Top 10 Variáveis": top_10_detrator,
            "Correlação": correlacoes_detrator
        },
        "Modelo Neutro": {
            "AUC-ROC": auc_neutro,
            "Relatório": relatorio_neutro,
            "Top 10 Variáveis": top_10_neutro,
            "Correlação": correlacoes_neutro
        },
    }

# Atualizar a geração de modelos para incluir as importâncias das variáveis e correlações
resultados_modelos = []
for regiao in regioes_unicas:
    df_regiao = filtrar_base(df, grupo_principal, coluna_regiao=coluna_regiao, regiao=regiao)
    resultado = criar_modelos_com_importancia(df_regiao, f"Região {regiao}", df)
    if resultado:
        resultados_modelos.append(resultado)

"""13-	Tentar avaliar as 5 top-variáveis de cada modelo com uma das técnica de gráfico, podendo ser PDP, ALE ou SHAP.  A explicação de como fazer estes gráficos será fornecida nas próximas aulas, antes da avaliação.  """

from sklearn.inspection import PartialDependenceDisplay
import matplotlib.pyplot as plt

# Função para gerar gráficos PDP
def gerar_pdp(modelo, X_train, variaveis, target_name):
    print(f"\nGerando PDP para o modelo {target_name}...")
    fig, axes = plt.subplots(1, len(variaveis), figsize=(5 * len(variaveis), 5), dpi=100)
    PartialDependenceDisplay.from_estimator(
        modelo,
        X_train,
        features=variaveis,
        ax=axes if len(variaveis) > 1 else [axes],
        grid_resolution=50
    )
    plt.suptitle(f"PDP - {target_name}", fontsize=16, y=1.02)
    plt.tight_layout()
    plt.show()

# Função para treinar e avaliar modelo com gráficos PDP
def treinar_avaliar_modelo_com_pdp(X_train, X_test, y_train, y_test, target_name):
    if X_train.empty or X_test.empty:
        print(f"\n[AVISO] Dados insuficientes para treinar o modelo {target_name}.")
        return None, 0.0, "Sem dados suficientes.", None

    # Treinando o modelo RandomForest
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Previsões e métricas
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    auc_roc = roc_auc_score(y_test, y_proba)
    report = classification_report(y_test, y_pred, output_dict=False)

    # Extraindo importâncias das variáveis
    feature_importances = pd.DataFrame({
        'variavel': X_train.columns,
        'importancia': model.feature_importances_
    }).sort_values(by='importancia', ascending=False)

    top_5_variaveis = feature_importances.head(5)['variavel'].tolist()

    print(f"\nResultados para o modelo {target_name}:")
    print(f"AUC-ROC: {auc_roc:.3f}")
    print("Relatório de Classificação:")
    print(report)
    print("\nTop 5 Variáveis para PDP:")
    print(top_5_variaveis)

    # Gerando gráficos PDP
    gerar_pdp(model, X_train, top_5_variaveis, target_name)

    return model, auc_roc, report, feature_importances

# Função para criar modelos e incluir gráficos PDP
def criar_modelos_com_pdp(df_filtrado, nome_filtro):
    if df_filtrado.empty:
        print(f"\nNenhum dado encontrado para o filtro: {nome_filtro}")
        return None

    X = df_filtrado[numeric_columns]
    y_detrator = df_filtrado['target_detrator']
    y_neutro = df_filtrado['target_neutro']

    # Modelo Detrator
    X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(
        X, y_detrator, test_size=0.2, random_state=42
    )
    modelo_detrator, auc_detrator, relatorio_detrator, importancias_detrator = treinar_avaliar_modelo_com_pdp(
        X_train_d, X_test_d, y_train_d, y_test_d, f"{nome_filtro} - Detrator"
    )

    # Modelo Neutro
    X_train_n, X_test_n, y_train_n, y_test_n = train_test_split(
        X, y_neutro, test_size=0.2, random_state=42
    )
    modelo_neutro, auc_neutro, relatorio_neutro, importancias_neutro = treinar_avaliar_modelo_com_pdp(
        X_train_n, X_test_n, y_train_n, y_test_n, f"{nome_filtro} - Neutro"
    )

    return {
        "Filtro": nome_filtro,
        "Modelo Detrator": {
            "AUC-ROC": auc_detrator,
            "Relatório": relatorio_detrator,
            "Importâncias": importancias_detrator
        },
        "Modelo Neutro": {
            "AUC-ROC": auc_neutro,
            "Relatório": relatorio_neutro,
            "Importâncias": importancias_neutro
        },
    }

# Atualizando o pipeline principal para incluir os gráficos PDP
resultados_modelos = []
for regiao in regioes_unicas:
    df_regiao = filtrar_base(df, grupo_principal, coluna_regiao=coluna_regiao, regiao=regiao)
    resultado = criar_modelos_com_pdp(df_regiao, f"Região {regiao}")
    if resultado:
        resultados_modelos.append(resultado)