import pandas as pd 
df = pd.read_csv("profissoesDf.csv", index_col=0)
#Normalizando as variaveis qualitativas
for colum in ["Profissao", "Nivel Educacao", "Localizacao"]:
    df[colum] = df[colum].str.lower().str.strip().str.replace(" ", "_")

with open("profissoes.pl", "w") as f:
    for _,row in df.iterrows():
        f.write(f"profissao({row["Profissao"]}, {row["Experiencia"]}, {row["Habilidades"]}, {row["Nivel Educacao"]}, {row["Localizacao"]}, {row["Salario"]}).\n")