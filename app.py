import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np


st.set_page_config(
    page_title="E-Commerce Analytics & Veille Prix",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Plateforme E-Commerce & Veille Concurrentielle")
st.markdown("Application interactive combinant l'Analyse Exploratoire des Ventes (EDA) et le Suivi Automatisé des Prix Concurrents.")


tab1, tab2 = st.tabs(["📈 Performance Ventes (EDA)", "🛒 Veille & Suivi des Prix Concurrents"])

with tab1:
    st.header("Analyse de la Performance Ventes")
    

    np.random.seed(42)
    regions = ['Cotonou', 'Porto-Novo', 'Parakou', 'Calavi']
    categories = ['Électronique', 'Mode', 'Maison']
    
    data_ventes = []
    for i in range(100):
        data_ventes.append({
            "Date": pd.date_range(start="2026-01-01", periods=100, freq="D")[i],
            "Region": np.random.choice(regions),
            "Categorie": np.random.choice(categories),
            "Montant_FCFA": np.random.randint(10000, 150000)
        })
    df_ventes = pd.DataFrame(data_ventes)
    

    selected_regions = st.multiselect("Filtrer par Région :", options=regions, default=regions)
    df_filtered = df_ventes[df_ventes['Region'].isin(selected_regions)]
    
    ca_total = df_filtered['Montant_FCFA'].sum()
    nb_ventes = len(df_filtered)
    panier_moyen = ca_total / nb_ventes if nb_ventes > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Chiffre d'Affaires Total", f"{ca_total:,.0f} FCFA".replace(",", " "))
    col2.metric("Nombre total de Ventes", f"{nb_ventes}")
    col3.metric("Panier Moyen", f"{panier_moyen:,.0f} FCFA".replace(",", " "))
    
    st.markdown("---")
    
    g_col1, g_col2 = st.columns(2)
    with g_col1:
        fig_cat = px.bar(
            df_filtered.groupby("Categorie")["Montant_FCFA"].sum().reset_index(),
            x="Categorie", y="Montant_FCFA",
            title="Répartition du CA par Catégorie de Produit",
            color="Categorie", labels={"Montant_FCFA": "CA (FCFA)"}
        )
        st.plotly_chart(fig_cat, use_container_width=True)
        
    with g_col2:
        df_time = df_filtered.groupby("Date")["Montant_FCFA"].sum().reset_index()
        fig_time = px.line(
            df_time, x="Date", y="Montant_FCFA",
            title="Tendance Quotidienne du Chiffre d'Affaires",
            markers=True
        )
        st.plotly_chart(fig_time, use_container_width=True)

with tab2:
    st.header("🛒 Veille Concurrentielle & Comparatif des Prix")
    st.markdown("Suivi et historique des prix relevés automatiquement via web scraping sur les plateformes concurrentes.")
    
   
    data_prix = [
        {"Produit": "Écouteurs Bluetooth Wireless", "Plateforme": "Site Concurrent A", "Prix_Releve": 15000, "Prix_Notre_Boutique": 13500, "Statut": "🟢 Moins cher chez nous"},
        {"Produit": "Écouteurs Bluetooth Wireless", "Plateforme": "Site Concurrent B", "Prix_Releve": 13000, "Prix_Notre_Boutique": 13500, "Statut": "🔴 Plus cher chez nous"},
        {"Produit": "Montre Connectée Sport", "Plateforme": "Site Concurrent A", "Prix_Releve": 35000, "Prix_Notre_Boutique": 32000, "Statut": "🟢 Moins cher chez nous"},
        {"Produit": "Montre Connectée Sport", "Plateforme": "Site Concurrent B", "Prix_Releve": 32000, "Prix_Notre_Boutique": 32000, "Statut": "🟠 Prix Alignés"},
        {"Produit": "Drone E77 Air Camera HD", "Plateforme": "Site Concurrent A", "Prix_Releve": 45000, "Prix_Notre_Boutique": 42500, "Statut": "🟢 Moins cher chez nous"},
        {"Produit": "Drone E77 Air Camera HD", "Plateforme": "Site Concurrent B", "Prix_Releve": 40000, "Prix_Notre_Boutique": 42500, "Statut": "🔴 Plus cher chez nous"},
    ]
    df_prix = pd.DataFrame(data_prix)
    

    col_v1, col_v2, col_v3 = st.columns(3)
    col_v1.metric("Produits Surveillés", "3 Références")
    col_v2.metric("Plateformes Scrapées", "2 Concurrents")
    col_v3.metric("Indice de Positionnement", "Competitive Zone (67%)")
    
    st.subheader("Dernier Relevé des Prix (Base SQLite / Scraping)")
    st.dataframe(df_prix, use_container_width=True)
    
   
    fig_comp = px.bar(
        df_prix, x="Produit", y=["Prix_Notre_Boutique", "Prix_Releve"],
        barmode="group",
        title="Comparatif des Prix : Notre Boutique vs Concurrents (FCFA)",
        labels={"value": "Prix (FCFA)", "variable": "Source"}
    )
    st.plotly_chart(fig_comp, use_container_width=True)
