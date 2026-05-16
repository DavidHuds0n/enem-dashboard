import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3

# ── Configuração da página ──────────────────────────────────────────
st.set_page_config(
    page_title="ENEM 2023 — Dashboard",
    page_icon="📊",
    layout="wide"
)

# ── Carregamento dos dados ──────────────────────────────────────────
@st.cache_data
def carregar_dados():
    conn = sqlite3.connect('data/enem.db')
    df = pd.read_sql("SELECT * FROM alunos", conn)
    conn.close()
    return df

df = carregar_dados()

# ── Cabeçalho ───────────────────────────────────────────────────────
st.title("📊 Análise do ENEM 2023")
st.markdown("Explore os dados de **127.574 participantes** do ENEM 2023 através de filtros dinâmicos e visões detalhadas.")
st.divider()

# ── Filtros na barra lateral ────────────────────────────────────────
st.sidebar.header("🔎 Filtros Dinâmicos")
st.sidebar.markdown("Deixe em branco para selecionar todas as opções.")

# Listas de valores únicos
regioes_opcoes = sorted(df['region'].dropna().unique().tolist())
escolas_opcoes = sorted(df['school_type'].dropna().unique().tolist())
internet_opcoes = sorted(df['has_internet'].dropna().unique().tolist())
genero_opcoes = sorted(df['genre'].dropna().unique().tolist())

# Componentes de Multiselect
regioes_selecionadas = st.sidebar.multiselect("Região", regioes_opcoes, placeholder="Todas as regiões")
escolas_selecionadas = st.sidebar.multiselect("Tipo de Escola", escolas_opcoes, placeholder="Pública e Privada")
internet_selecionadas = st.sidebar.multiselect("Acesso à Internet", internet_opcoes, placeholder="Com e Sem Internet")
generos_selecionados = st.sidebar.multiselect("Gênero", genero_opcoes, placeholder="Todos os gêneros")

# ── Aplica filtros ───────────────────────────────────────────────────
df_filtrado = df.copy()

if regioes_selecionadas:
    df_filtrado = df_filtrado[df_filtrado['region'].isin(regioes_selecionadas)]

if escolas_selecionadas:
    df_filtrado = df_filtrado[df_filtrado['school_type'].isin(escolas_selecionadas)]

if internet_selecionadas:
    df_filtrado = df_filtrado[df_filtrado['has_internet'].isin(internet_selecionadas)]

if generos_selecionados:
    df_filtrado = df_filtrado[df_filtrado['genre'].isin(generos_selecionados)]

# ── Métricas principais ──────────────────────────────────────────────
st.subheader("📌 Visão Geral da Seleção")

# Tratamento para evitar erro se o filtro zerar a base
if df_filtrado.empty:
    st.warning("Nenhum dado encontrado com os filtros selecionados.")
    st.stop()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Alunos", f"{len(df_filtrado):,}".replace(",", "."))
col2.metric("Nota Média Geral", f"{df_filtrado['mean_score'].mean():.1f}")
col3.metric("Melhor Nota (Matemática)", f"{df_filtrado['score_math'].max():.1f}")
col4.metric("Melhor Nota (Redação)", f"{df_filtrado['score_essay'].max():.1f}")

st.write("") # Espaçamento

# ── Organização em Abas ──────────────────────────────────────────────
aba1, aba2, aba3, aba4 = st.tabs([
    "🌎 Desempenho Regional", 
    "🏫 Perfil Escolar", 
    "💰 Fator Socioeconômico", 
    "📈 Correlações Analíticas"
])

# ================= ABA 1: DESEMPENHO REGIONAL =================
with aba1:
    st.markdown("### Desempenho Médio por Região")
    media_regiao = (
        df_filtrado.groupby('region')['mean_score']
        .mean()
        .reset_index()
        .sort_values('mean_score', ascending=False)
    )
    media_regiao.columns = ['Região', 'Nota Média']

    fig_regiao = px.bar(
        media_regiao,
        x='Região',
        y='Nota Média',
        color='Nota Média',
        color_continuous_scale='Blues',
        text_auto='.1f'
    )
    fig_regiao.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_regiao, use_container_width=True)

# ================= ABA 2: PERFIL ESCOLAR =================
with aba2:
    st.markdown("### Impacto do Tipo de Escola no Desempenho")
    col_a, col_b = st.columns(2)

    with col_a:
        # Gráfico de Barras: Matemática por Escola
        media_escola = (
            df_filtrado.groupby('school_type')['score_math']
            .mean()
            .reset_index()
        )
        fig_escola = px.bar(
            media_escola,
            x='school_type',
            y='score_math',
            color='school_type',
            color_discrete_map={'Public': '#2196F3', 'Private': '#FF9800'},
            labels={'school_type': 'Tipo de Escola', 'score_math': 'Média em Matemática'},
            text_auto='.1f'
        )
        fig_escola.update_layout(showlegend=False)
        st.plotly_chart(fig_escola, use_container_width=True)

    with col_b:
        # Boxplot: Distribuição da Média Geral
        fig_box = px.box(
            df_filtrado,
            x='school_type',
            y='mean_score',
            color='school_type',
            color_discrete_map={'Public': '#2196F3', 'Private': '#FF9800'},
            labels={'school_type': 'Tipo de Escola', 'mean_score': 'Nota Média Geral'}
        )
        fig_box.update_layout(showlegend=False)
        st.plotly_chart(fig_box, use_container_width=True)

# ================= ABA 3: FATOR SOCIOECONÔMICO =================
with aba3:
    col_c, col_d = st.columns(2)
    
    with col_c:
        st.markdown("### Renda Familiar")
        media_renda = (
            df_filtrado.groupby('family_income')['mean_score']
            .mean()
            .reset_index()
            .sort_values('mean_score', ascending=True)
        )
        fig_renda = px.bar(
            media_renda,
            x='mean_score',
            y='family_income',
            orientation='h',
            color='mean_score',
            color_continuous_scale='Greens',
            labels={'mean_score': 'Nota Média', 'family_income': 'Faixa de Renda'},
            text_auto='.1f'
        )
        fig_renda.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_renda, use_container_width=True)

    with col_d:
        st.markdown("### Acesso à Internet")
        # Substituí por um gráfico de rosca para ver a proporção de alunos no filtro
        contagem_internet = df_filtrado['has_internet'].value_counts().reset_index()
        contagem_internet.columns = ['Acesso à Internet', 'Quantidade']
        
        fig_internet = px.pie(
            contagem_internet,
            names='Acesso à Internet',
            values='Quantidade',
            hole=0.4,
            color='Acesso à Internet',
            color_discrete_map={'Yes': '#4CAF50', 'No': '#F44336'}
        )
        st.plotly_chart(fig_internet, use_container_width=True)
        
    st.markdown("### Desempenho por Gênero e Área de Conhecimento")
    colunas_notas = {
        'score_languages': 'Linguagens',
        'score_math': 'Matemática',
        'score_human': 'Humanas',
        'score_natural': 'Natureza',
        'score_essay': 'Redação'
    }

    medias_genero = (
        df_filtrado.groupby('genre')[list(colunas_notas.keys())]
        .mean()
        .reset_index()
        .melt(id_vars='genre', var_name='area', value_name='nota')
    )
    medias_genero['area'] = medias_genero['area'].map(colunas_notas)
    
    fig_genero = px.bar(
        medias_genero,
        x='area',
        y='nota',
        color='genre',
        barmode='group',
        color_discrete_map={'Female': '#E91E63', 'Male': '#2196F3'},
        labels={'area': 'Área', 'nota': 'Nota Média', 'genre': 'Gênero'}
    )
    st.plotly_chart(fig_genero, use_container_width=True)

# ================= ABA 4: CORRELAÇÕES ANALÍTICAS =================
with aba4:
    st.markdown("### Correlação entre Áreas de Conhecimento")
    st.markdown("Verifique como o desempenho em uma área afeta as demais.")
    
    col_e, col_f = st.columns(2)
    
    with col_e:
        # Matriz de Correlação
        st.markdown("**Matriz de Correlação**")
        notas_cols = ['score_languages', 'score_math', 'score_human', 'score_natural', 'score_essay']
        nomes_bonitos = ['Linguagens', 'Matemática', 'Humanas', 'Natureza', 'Redação']
        
        df_notas = df_filtrado[notas_cols].dropna()
        matriz_corr = df_notas.corr()
        
        fig_corr = px.imshow(
            matriz_corr,
            x=nomes_bonitos,
            y=nomes_bonitos,
            text_auto=".2f",
            color_continuous_scale='RdBu_r',
            zmin=-1, zmax=1
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        
    with col_f:
        # Gráfico de Densidade (melhor que Scatter para 127k pontos)
        st.markdown("**(Densidade) Matemática vs. Redação**")
        fig_densidade = px.density_heatmap(
            df_filtrado, 
            x='score_math', 
            y='score_essay',
            labels={'score_math': 'Nota em Matemática', 'score_essay': 'Nota em Redação'},
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_densidade, use_container_width=True)

st.divider()
st.caption("Fonte: Kaggle — Student Performance (ENEM 2023) | Desenvolvido por David Hudson")