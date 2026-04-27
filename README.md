
---

# Fonte do Dataset

* [https://www.kaggle.com/datasets/nalisha/job-salary-prediction-dataset?resource=download](https://www.kaggle.com/datasets/nalisha/job-salary-prediction-dataset?resource=download)

## Variáveis escolhidas

## Variáveis escolhidas

| Profissão | Experiência | Habilidades técnicas | Nível de educação | Localização | Salário |
|-----------|------------|----------------------|-------------------|------------|---------|
|           |            |                      |                   |            |         |
---

# Construção da Base de Conhecimento

## Normalização do dataset (`construcao.py`)

```python
for column in ["Profissao", "Nivel Educacao", "Localizacao"]:
    df[column] = df[column].str.lower().str.strip().str.replace(" ", "_")
```

## Conversão do CSV para `.pl`

```python
with open("profissoes.pl", "w") as f:
    for _, row in df.iterrows():
        f.write(
            f"profissao({row['Profissao']}, {row['Experiencia']}, {row['Habilidades']}, "
            f"{row['Nivel Educacao']}, {row['Localizacao']}, {row['Salario']}).\n"
        )
```

---

# Execução

Para rodar a base de conhecimento, utilizamos:

* [https://swish.swi-prolog.org/](https://swish.swi-prolog.org/)

---

# Perguntas à Base de Conhecimento

## 1. Toda pessoa com formação superior tem mais experiência e habilidades do que alguém com ensino médio?

Utilizamos a função:

```prolog
pessoa_ensino_medio_mais_experiencia(Educacao2) :-
    profissao(_, Anos1, Habilidades1, high_school, _, _),
    profissao(_, Anos2, Habilidades2, Educacao2, _, _),
    Educacao2 \= high_school,
    (
        Anos2 =< Anos1,
        Habilidades2 =< Habilidades1
    ).
```

Consulta:

```prolog
pessoa_ensino_medio_mais_experiencia(Educacao).
```

Resultado:

* `Educacao2 = diploma ...`

Conclusão:

* Isso mostra um contraexemplo, logo a afirmação é **falsa** (prova por contraposição).

---

## 2. Qual área possui a maior média salarial?

Função para calcular a média salarial por área:

```prolog
media_salarial(Area, Media) :-
    setof(Salario, Anos^Hab^Edu^Loc^profissao(Area, Anos, Hab, Edu, Loc, Salario), Lista),
    sum_list(Lista, Soma),
    length(Lista, N),
    N > 0,
    Media is Soma / N.
```

Função para encontrar a maior média:

```prolog
maior_media_salarial(Area, Media) :-
    setof((Media, Area), media_salarial(Area, Media), Lista),
    last(Lista, (Media, Area)).
```

Consulta:

```prolog
maior_media_salarial(Area, Media).
```

Resultado:

* `Area = ai_engineer`
* `Media = 169266.89024390245`

---

## 3. Em qual localização há mais profissionais com PhD e Master?

Função que conta profissionais com PhD ou Master:

```prolog
profissional_phd_master(Localizacao, 1) :-
    profissao(_, _, _, Edu, Localizacao, _),
    (Edu == phd ; Edu == master).
```

Função para contagem por localização:

```prolog
contagem_profissionais_phd_master(Localizacao, Total) :-
    setof(Localizacao, A^B^C^D^profissao(_, A, B, C, Localizacao, D), Localizacoes),
    member(Localizacao, Localizacoes),
    findall(N, profissional_phd_master(Localizacao, N), Lista),
    sum_list(Lista, Total).
```

Função para encontrar a localização com maior quantidade:

```prolog
localizacao_mais_profissionais_phd_master(Localizacao, Qtd) :-
    findall((Qtd, Localizacao),
            contagem_profissionais_phd_master(Localizacao, Qtd),
            Lista),
    sort(Lista, ListaOrdenada),
    last(ListaOrdenada, (Qtd, Localizacao)).
```

Consulta:

```prolog
localizacao_mais_profissionais_phd_master(Localizacao, Qtd).
```

Resultado:

* `Localizacao = germany`
* `Qtd = 54`

---
