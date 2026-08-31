import requests
import pandas as pd
import streamlit as st
from datetime import datetime

st.title("Notícias da UFRN sobre a EAJ")

url = "https://webcache01-producao.info.ufrn.br/admin/portal-ufrn/wp-json/wp/v2/noticias-busca/"

pagina = 1
noticias = []

while True:
    parametros = {
        "per_page": 100,
        "page": pagina,
        "termo": "EAJ",
        "tags": "",
        "data": ""
    }

    resposta = requests.get(
        url,
        params=parametros,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    dados = resposta.json()

    if not dados:
        break

    for noticia in dados:
        timestamp = int(noticia["acf"]["data_de_publicacao"])
        ano = datetime.fromtimestamp(timestamp).year
        link = noticia["link"]

        noticias.append((ano, link))

    pagina += 1

with open("noticias_eaj.txt", "w", encoding="utf-8") as arquivo:
    for ano, link in noticias:
        arquivo.write(f"{ano} | {link}\n")

df = pd.DataFrame(
    noticias,
    columns=["Ano", "Link"]
)

quantidade_por_ano = (
    df["Ano"]
    .value_counts()
    .sort_index()
)

st.write(f"Total de notícias encontradas: {len(noticias)}")

st.subheader("Quantidade de notícias por ano")

st.bar_chart(quantidade_por_ano)