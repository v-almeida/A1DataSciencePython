
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


from google.colab import files
print("Por favor, faça upload do arquivo .xlsx contendo a lista de NPS")
uploaded = files.upload()


file_name = list(uploaded.keys())[0]


df = pd.read_excel(file_name, sheet_name=0)


conditions = [
    (df['nota'] >= 9),              # Notas 9 ou 10: Promotor
    (df['nota'].between(7, 8)),     # Notas 7 ou 8: Neutro
    (df['nota'] < 7)                # Notas < 7: Detrator
]


classes = ['promotor', 'neutro', 'detrator']


df['target'] = pd.cut(
    df['nota'],
    bins=[-1, 6, 8, 10],  # Intervalos: <7, 7-8, 9-10
    labels=classes[::-1],  # Classes na ordem inversa para alinhar com os bins
    include_lowest=True
)


target_counts = df['target'].value_counts()


print("Contagem das classes no target:")
print(target_counts)


if (target_counts['promotor'] == 18251 and 
    target_counts['neutro'] == 4738 and 
    target_counts['detrator'] == 2185):
    print("\nAs contagens das classes estão corretas!")
else:
    print("\nAs contagens das classes não estão de acordo. Verifique os dados.")


plt.figure(figsize=(8, 6))
sns.countplot(data=df, x='target', order=['promotor', 'neutro', 'detrator'], palette='coolwarm')
plt.title("Distribuição das Classes no Target")
plt.xlabel("Classes")
plt.ylabel("Quantidade")
plt.show()


grouped_counts = df.groupby('target').count()
print("\nContagem detalhada por classe com df.groupby('target').count():")
print(grouped_counts)
