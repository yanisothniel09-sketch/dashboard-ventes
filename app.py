import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import sqlite3

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Portfolio Data Analytics",
    page_icon="📊",
    layout="wide"
)

# Titre Principal
st.title("📊 Portfolio Data Analyst - Projets & Démonstrations")
st.markdown("Application centralisée regroupant mes réalisations en **Analyse de Données (EDA)**, **Veille Concurrentielle (Scraping)** et **Requêtage SQL**.")

# Création des 3 onglets
tab1, tab2, tab3 = st.tabs([
    "📈 Performance Ventes (EDA)", 
    "🛒 Veille & Suivi des Prix", 
    "🗄️ Requêtes & Base SQL"
])

# ==========================================
# ONGLET 1 : EDA PERFORMANCE VENTES
# ==========================================
with tab1:
    st.header("Analyse Exploratoire de la Performance Ventes")
    
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

# ==========================================
# ONGLET 2 : VEILLE DE PRIX & SCRAPING
# ==========================================
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

# ==========================================
# ONGLET 3 : DEMO REQUÊTES SQL
# ==========================================
with tab3:
    st.header("🗄️ Analyse Relationnelle & Exécution SQL (SQLite)")
    st.markdown("Exécution dynamique de requêtes complexes sur un schéma relationnel e-commerce.")
    
    # Base de données SQLite temporaire
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    cursor.executescript('''
        CREATE TABLE clients (client_id INT, nom TEXT, ville TEXT);
        INSERT INTO clients VALUES (1, 'Koffi Mensah', 'Cotonou'), (2, 'Amina Djibo', 'Parakou'), (3, 'Sègla Dossou', 'Porto-Novo');
        
        CREATE TABLE produits (produit_id INT, nom_produit TEXT, categorie TEXT, prix INT);
        INSERT INTO produits VALUES (10, 'Écouteurs', 'Électronique', 15000), (20, 'Montre', 'Électronique', 35000);
        
        CREATE TABLE commandes (commande_id INT, client_id INT, produit_id INT, quantite INT);
        INSERT INTO commandes VALUES (1001, 1, 10, 2), (1002, 1, 20, 1), (1003, 2, 10, 1), (1004, 3, 20, 2);
    ''')
    
    sql_query = """
    SELECT 
        cl.nom AS Client, 
        cl.ville AS Ville, 
        COUNT(co.commande_id) AS Commandes,
        SUM(co.quantite * pr.prix) AS Total_Depense_FCFA
    FROM clients cl
    JOIN commandes co ON cl.client_id = co.client_id
    JOIN produits pr ON co.produit_id = pr.produit_id
    GROUP BY cl.client_id
    ORDER BY Total_Depense_FCFA DESC;
    """
    
    st.subheader("Requête SQL Exécutée (Jointures & Agrégation) :")
    st.code(sql_query, language="sql")
    
    df_sql_result = pd.read_sql_query(sql_query, conn)
    st.subheader("Résultat généré en direct par le serveur SQLite :")
    st.dataframe(df_sql_result, use_container_width=True)
