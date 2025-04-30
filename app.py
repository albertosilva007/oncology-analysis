import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados


@st.cache_data
def carregar_dados():
    df = pd.read_csv('global_dados.csv')
    return df


# Carregar o DataFrame
df = carregar_dados()

# Título do App
st.title("🌎 Análise Global de Pacientes com Câncer (2015-2024)")

st.markdown("""
Este projeto explora a relação entre tipos de câncer, distribuição geográfica e custo de tratamento em escala global entre 2015 e 2024.
""")

# Barra lateral para filtros
st.sidebar.header("Filtros")
paises = sorted(df['Country_Region'].unique())
tipos_cancer = sorted(df['Cancer_Type'].unique())
estagios_cancer = sorted(df['Cancer_Stage'].unique())

selecao_pais = st.sidebar.multiselect(
    "Filtrar por País/Região", paises, default=paises)
selecao_cancer = st.sidebar.multiselect(
    "Filtrar por Tipo de Câncer", tipos_cancer, default=tipos_cancer)
selecao_estagio = st.sidebar.multiselect(
    "Filtrar por Estágio do Câncer", estagios_cancer, default=estagios_cancer)

# Filtrar os dados com base nas seleções
df_filtrado = df[df['Country_Region'].isin(selecao_pais) &
                 df['Cancer_Type'].isin(selecao_cancer) &
                 df['Cancer_Stage'].isin(selecao_estagio)]

# Visão Geral dos Dados Filtrados
st.header("🔍 Visão Geral dos Dados Filtrados")
st.dataframe(df_filtrado.head())

# Métricas Chave
st.header("📊 Métricas Chave")
col1, col2, col3 = st.columns(3)
with col1:
    total_pacientes = df_filtrado.shape[0]
    st.metric("Total de Pacientes", total_pacientes)
with col2:
    media_custo = df_filtrado['Treatment_Cost_USD'].mean()
    st.metric("Custo Médio de Tratamento (USD)", f"{media_custo:,.2f}")
with col3:
    media_sobrevida = df_filtrado['Survival_Years'].mean()
    st.metric("Sobrevida Média (Anos)", f"{media_sobrevida:.2f}")

# Gráfico: Número de Pacientes por País (Filtrado)
st.header("📍 Distribuição de Pacientes por País/Região (Filtrado)")
fig_pais = px.histogram(
    df_filtrado,
    x="Country_Region",
    title="Número de Pacientes por País/Região",
    color_discrete_sequence=["indianred"]
)
fig_pais.update_layout(xaxis_title="País/Região",
                       yaxis_title="Número de Pacientes")
st.plotly_chart(fig_pais)

# Gráfico: Tipos de Câncer Mais Frequentes (Filtrado)
st.header("🧬 Tipos de Câncer Mais Frequentes (Filtrado)")
fig_cancer = px.histogram(
    df_filtrado,
    x="Cancer_Type",
    title="Tipos de Câncer",
    color_discrete_sequence=["teal"]
)
fig_cancer.update_layout(xaxis_title="Tipo de Câncer", yaxis_title="Contagem")
st.plotly_chart(fig_cancer)

# Relação entre Custo de Tratamento e Sobrevivência (Filtrado)
st.header("💸 Custo de Tratamento vs Anos de Sobrevivência (Filtrado)")
fig_custo = px.scatter(
    df_filtrado,
    x="Treatment_Cost_USD",
    y="Survival_Years",
    color="Cancer_Stage",
    title="Custo de Tratamento vs Anos de Sobrevivência",
    labels={
        "Treatment_Cost_USD": "Custo do Tratamento (USD)",
        "Survival_Years": "Anos de Sobrevivência",
        "Cancer_Stage": "Estágio do Câncer"
    }
)
fig_custo.update_traces(marker=dict(size=8))
st.plotly_chart(fig_custo)

# Análise Adicional: Custo Médio por Tipo de Câncer
st.header("💰 Custo Médio de Tratamento por Tipo de Câncer")
custo_medio_cancer = df_filtrado.groupby('Cancer_Type')[
    'Treatment_Cost_USD'].mean().sort_values(ascending=False).reset_index()
fig_custo_cancer = px.bar(
    custo_medio_cancer,
    x='Cancer_Type',
    y='Treatment_Cost_USD',
    title='Custo Médio de Tratamento por Tipo de Câncer',
    labels={
        'Treatment_Cost_USD': 'Custo Médio (USD)', 'Cancer_Type': 'Tipo de Câncer'},
    color_discrete_sequence=["goldenrod"]
)
st.plotly_chart(fig_custo_cancer)

# Análise Adicional: Sobrevida Média por Estágio do Câncer
st.header("⏳ Sobrevida Média por Estágio do Câncer")
sobrevida_media_estagio = df_filtrado.groupby(
    'Cancer_Stage')['Survival_Years'].mean().sort_values().reset_index()
fig_sobrevida_estagio = px.bar(
    sobrevida_media_estagio,
    x='Cancer_Stage',
    y='Survival_Years',
    title='Sobrevida Média por Estágio do Câncer',
    labels={
        'Survival_Years': 'Sobrevida Média (Anos)', 'Cancer_Stage': 'Estágio do Câncer'},
    color_discrete_sequence=["mediumseagreen"]
)
st.plotly_chart(fig_sobrevida_estagio)
