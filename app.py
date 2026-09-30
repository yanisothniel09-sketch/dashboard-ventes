import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Analyse Ventes E-commerce", layout="wide")

st.title("📊 Dashboard EDA - Analyse de la Performance Ventes")
st.markdown("Application de visualisation interactive pour explorer les tendances d'achat e-commerce.")

@st.cache_data
def load_data():
    data = {
        'Date': pd.date_range(start='2026-01-01', periods=100, freq='D'),
        'Categorie': ['Électronique', 'Mode', 'Maison', 'Mode', 'Électronique'] * 20,
        'Ventes_FCFA': [15000, 28000, 8000, 45000, 32000] * 20,
        'Quantite': [1, 2, 1, 3, 2] * 20,
        'Region': ['Cotonou', 'Porto-Novo', 'Parakou', 'Cotonou', 'Calavi'] * 20
    }
    df = pd.DataFrame(data)

    df['Prix_Unitaire'] = df['Ventes_FCFA'] / df['Quantite']
    return df

df = load_data()


st.sidebar.header("Filtres d'Analyse")
selected_region = st.sidebar.multiselect(
    "Filtrer par Région :",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)


filtered_df = df[df['Region'].isin(selected_region)]


col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Chiffre d'Affaires Total", f"{filtered_df['Ventes_FCFA'].sum():,} FCFA".replace(',', ' '))
with col2:
    st.metric("Nombre total de Ventes", len(filtered_df))
with col3:
    panier_moyen = filtered_df['Ventes_FCFA'].mean() if not filtered_df.empty else 0
    st.metric("Panier Moyen", f"{panier_moyen:,.0f} FCFA".replace(',', ' '))

st.divider()


col_graph1, col_graph2 = st.columns(2)

with col_graph1:
    st.subheader("Ventes par Catégorie")
    fig_cat = px.bar(
        filtered_df, 
        x='Categorie', 
        y='Ventes_FCFA', 
        color='Categorie',
        title="Répartition du CA par Catégorie de Produit",
        text_auto='.2s'
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with col_graph2:
    st.subheader("Évolution Chronologique des Ventes")
    fig_line = px.line(
        filtered_df, 
        x='Date', 
        y='Ventes_FCFA',
        title="Tendance Quotidienne du Chiffre d'Affaires",
        markers=True
    )
    st.plotly_chart(fig_line, use_container_width=True)

with st.expander("Aperçu des Données Filtrées (Nettoyées)"):
    st.dataframe(filtered_df)  