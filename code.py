# 1. Importando as bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 2. Caminho para o arquivo Excel
file_name = "Lista NPS Positivo_V4.csv"

  # Substitua pelo nome exato do arquivo

try:
    # 3. Carregar a primeira sheet do arquivo Excel
    df = pd.read_excel(file_name, sheet_name=0)
    print("Arquivo carregado com sucesso!")
except FileNotFoundError:
    print(f"Erro: O arquivo '{file_name}' não foi encontrado no diretório especificado.")
    exit()

# 4. Criar a nova coluna "target" com base na análise da variável "nota"
# Condições para classificação
conditions = [
    (df['nota'] >= 9),              # Notas 9 ou 10: Promotor
    (df['nota'].between(7, 8)),     # Notas 7 ou 8: Neutro
    (df['nota'] < 7)                # Notas < 7: Detrator
]

# Classes associadas às condições
classes = ['promotor', 'neutro', 'detrator']

# Aplicar condições para criar a coluna 'target'
df['target'] = pd.cut(
    df['nota'],
    bins=[-1, 6, 8, 10],  # Intervalos: <7, 7-8, 9-10
    labels=classes[::-1],  # Classes na ordem inversa para alinhar com os bins
    include_lowest=True
)

# 5. Verificar as contagens das classes no target
target_counts = df['target'].value_counts()

# Exibir as contagens para validar com os valores esperados
print("Contagem das classes no target:")
print(target_counts)

# Verificação específica para garantir que os valores estão corretos
if (target_counts['promotor'] == 18251 and 
    target_counts['neutro'] == 4738 and 
    target_counts['detrator'] == 2185):
    print("\nAs contagens das classes estão corretas!")
else:
    print("\nAs contagens das classes não estão de acordo. Verifique os dados.")

# 6. Visualizar a distribuição das classes em um gráfico de barras...
plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='target', order=['promotor', 'neutro', 'detrator'], palette='coolwarm')
plt.title("Distribuição das Classes no Target")
plt.xlabel("Classes")
plt.ylabel("Quantidade")
plt.show()

# 7. Executar df.groupby('target').count() para exibir a contagem detalhada por classe
grouped_counts = df.groupby('target').count()
print("\nContagem detalhada por classe com df.groupby('target').count():")
print(grouped_counts)
 # type: ignore