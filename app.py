import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import sqlite3

st.set_page_config(
    page_title="Portfolio Data & Web",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Portfolio Data Analyst & Développeur Web")
st.markdown("Application centralisée regroupant mes réalisations en **Analyse de Données**, **Veille Concurrentielle**, **SQL** et **Projets Web / E-Commerce**.")

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Performance Ventes (EDA)", 
    "🛒 Veille & Suivi des Prix", 
    "🗄️ Requêtes & Base SQL",
    "🌐 Projets Web & E-Commerce"
])

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


with tab2:
    st.header("🛒 Veille Concurrentielle & Comparatif des Prix")
    st.markdown("Suivi et historique des prix relevés automatiquement via web scraping.")
    
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

with tab3:
    st.header("🗄️ Analyse Relationnelle & Exécution SQL")
    st.markdown("Exécution dynamique de requêtes complexes sur un schéma relationnel e-commerce.")
    
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

# ==========================================
# ONGLET 4 : PROJETS WEB & E-COMMERCE
# ==========================================
with tab4:
    st.header("🌐 Portfolio Développement Web & Visualisations")
    st.markdown("Présentation de mes applications web interactives, dashboards JS et projets e-commerce.")
    
    st.subheader("💻 Projets Web & Dashboards Interactifs (HTML / CSS / Chart.js)")
    
    col_w1, col_w2 = st.columns(2)
    
    with col_w1:
        st.markdown("### 🌤️ App Météo & Historique")
        st.write("**Technologies :** HTML5, CSS3, JavaScript")
        st.markdown("[👉 Voir l'App Météo en direct](https://yanisothniel09-sketch.github.io/projets-web-html/meteo.html)")
        
        st.markdown("---")
        
        st.markdown("### 📈 Dashboard E-Commerce - Aperçu Général")
        st.write("**Technologies :** HTML5, CSS3, JavaScript")
        st.markdown("[👉 Voir le Dashboard E-Commerce](https://yanisothniel09-sketch.github.io/projets-web-html/dashboard-ecommerce.html)")

    with col_w2:
        st.markdown("### 📊 Dashboard Chart.js - Indicateurs Afrique de l'Ouest")
        st.write("**Technologies :** HTML5, CSS3, Chart.js")
        st.markdown("[👉 Voir le Dashboard Afrique](https://yanisothniel09-sketch.github.io/projets-web-html/dashboard-afrique.html)")
        
        st.markdown("---")
        
        st.markdown("### 🎨 Infographie : E-commerce en Afrique de l'Ouest")
        st.write("**Technologies :** HTML5, CSS Grid/Flexbox")
        st.markdown("[👉 Voir l'Infographie Interactive](https://yanisothniel09-sketch.github.io/projets-web-html/infographie.html)")

    st.markdown("---")
    
    st.subheader("🛍️ Projets & Administration E-Commerce (Shopify)")
    st.markdown("Conception, paramétrage de catalogues et gestion de boutiques en ligne.")
    
    col_s1, col_s2 = st.columns(2)
    
    with col_s1:
        st.markdown("### 🛒 Charlotte Store")
        st.write("**Plateforme :** Shopify")
        st.write("**Secteur :** Produits High-Tech & Électronique")
        st.write("**Réalisations techniques :**")
        st.write("- Configuration complète du back-office et du thème d'affichage")
        st.write("- Structuration du catalogue produits et inventaire")
        st.write("- Paramétrage des méthodes de paiement et parcours de commande")
        st.info("📌 *Étude de cas : Boutique configurée et gérée dans le cadre de projets d'expérimentation e-commerce.*")
        
    with col_s2:
        st.markdown("### 🏬 Stella's Store")
        st.write("**Plateforme :** Shopify")
        st.write("**Secteur :** Commerce généralist et accessoires")
        st.write("**Réalisations techniques :**")
        st.write("- Personnalisation de l'interface vitrine et fiches produits")
        st.write("- Intégration des solutions de gestion des stocks et commandes")
        st.write("- Optimisation du tunnel de conversion (Checkout)")
        st.info("📌 *Étude de cas : Projet d'intégration e-commerce et gestion de boutique en ligne.*")
