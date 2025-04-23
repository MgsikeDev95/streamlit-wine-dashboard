import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 1) Carrega e dá cache nos dados - CORREÇÃO: Adicionei verificação de arquivos
@st.cache_data
def load_data():
    try:
        red = pd.read_csv("data/winequality-red.csv", sep=";")
        white = pd.read_csv("data/winequality-white.csv", sep=";")
        red["type"] = "red"
        white["type"] = "white"
        return pd.concat([red, white], ignore_index=True)
    except FileNotFoundError as e:
        st.error(f"Erro ao carregar arquivos: {e}")
        return pd.DataFrame()

df = load_data()

# Verifica se os dados foram carregados corretamente
if df.empty:
    st.stop()

# 2) Cabeçalho
st.title("🍷 Wine Quality Dashboard")
st.markdown(
    """
    Explore as características químicas de vinhos tintos e brancos  
    e veja como elas se relacionam com a qualidade percebida.
    """
)

# 3) Sidebar: filtros - CORREÇÃO: Adicionei validação para dados vazios
st.sidebar.header("🔎 Filtros")

if not df.empty:
    wine_type = st.sidebar.multiselect(
        "Tipo de vinho",
        options=df["type"].unique(),
        default=df["type"].unique()
    )

    quality_range = st.sidebar.slider(
        "Faixa de qualidade",
        min_value=int(df["quality"].min()),
        max_value=int(df["quality"].max()),
        value=(int(df["quality"].min()), int(df["quality"].max()))
    )

    feature = st.sidebar.selectbox(
        "Escolha a variável para analisar vs. qualidade",
        options=[
            "fixed acidity", "volatile acidity", "citric acid",
            "residual sugar", "chlorides", "free sulfur dioxide",
            "total sulfur dioxide", "density", "pH", "sulphates", "alcohol"
        ]
    )

    # 4) Aplicar filtros - CORREÇÃO: Adicionei tratamento para seleção vazia
    if not wine_type:
        st.warning("Selecione pelo menos um tipo de vinho")
        st.stop()

    df_filt = df[
        (df["type"].isin(wine_type)) &
        (df["quality"].between(*quality_range))
    ]

    st.subheader(f"Dados filtrados: {len(df_filt)} amostras")
    st.dataframe(df_filt.head(10))

    # 5) Boxplot - CORREÇÃO: Melhorei a visualização
    st.subheader(f"📊 Boxplot: {feature} por qualidade")
    fig, ax = plt.subplots(figsize=(10, 6))
    df_filt.boxplot(column=feature, by="quality", ax=ax, grid=False)
    ax.set_xlabel("Qualidade", fontsize=12)
    ax.set_ylabel(feature.capitalize(), fontsize=12)
    ax.set_title("")
    plt.suptitle("")
    plt.xticks(rotation=45)
    st.pyplot(fig, clear_figure=True)  # CORREÇÃO: clear_figure evita duplicação

    # Distribuição da qualidade - CORREÇÃO: Melhorei o gráfico
    st.subheader("📈 Distribuição de Qualidade")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    hist_vals = df_filt["quality"].value_counts().sort_index()
    ax2.bar(hist_vals.index, hist_vals.values, color='skyblue', edgecolor='black')
    ax2.set_xlabel("Qualidade", fontsize=12)
    ax2.set_ylabel("Contagem", fontsize=12)
    ax2.set_xticks(hist_vals.index)
    st.pyplot(fig2, clear_figure=True)

else:
    st.warning("Nenhum dado disponível para exibição.")