import streamlit as st
import pandas as pd

# Importe de la base de données.
taxis_df = pd.read_csv("data/taxis.csv")

# Titre
st.title("Dashboard Analyse Taxis - Borja Perez Garcia")

# Analyse des quartiers uniques dans pickup_borough en retirant les nan.
quartiers = taxis_df["pickup_borough"].dropna().unique() 

# Creation de menu deroulant.
choix_quartier = st.selectbox(
    "Choisissez le quartier de prise en charge:",
    quartiers
)

# Filtre par arrondissement dataframe
arrondissement_filtre = taxis_df["pickup_borough"] == choix_quartier
arrondissement = taxis_df[arrondissement_filtre]
st.dataframe(arrondissement.head(5))

# Nombre total de courses du quartier
st.metric("Nombre de courses:", len(arrondissement))
