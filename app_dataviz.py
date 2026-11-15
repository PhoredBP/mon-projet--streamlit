import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Import donnees web et si erreur .csv local
@st.cache_data
def charger_donnees():
    try:
        return pd.read_csv("https://raw.githubusercontent.com/mwaskom/seaborn-data/refs/heads/master/flights.csv")
    except Exception:
        return pd.read_csv("data/flights.csv")

flights_df = charger_donnees()
flights_df["date"] = pd.to_datetime(
    flights_df["month"] + " " + flights_df["year"].astype(str),
    format="%B %Y")

# Titre
st.title("Fly me to the moon")

# Années slider
annee_max_filtre = int(flights_df["year"].max())
annee_min_filtre = int(flights_df["year"].min())
plage_annee_complete = (annee_min_filtre, annee_max_filtre)

annee_min, annee_max = st.slider("Année", min_value = annee_min_filtre, max_value = annee_max_filtre, value = plage_annee_complete)

df_annees = flights_df[ (flights_df["year"] >= annee_min) & (flights_df["year"] <= annee_max)]

# Selectbox mois ## A reviser, complex!
mois = ["Tous les mois"] + flights_df["month"].dropna().unique().tolist()
choix_mois = st.selectbox(
    "Select ton mois",
    mois)

if choix_mois == "Tous les mois":
    mois_period = df_annees
else: 
    mois_period = df_annees[df_annees["month"] == choix_mois]

st.dataframe(mois_period)

# Nb passagers metric
nb_passagers = int(mois_period["passengers"].sum())
st.metric("Nombre de passagers pour la periode: ", nb_passagers, icon="✈️")

# Graphique du nb de passagers au fil de mois/années ## A reviser
st.line_chart(mois_period, x="date",y="passengers")

# Heatmap ## A reviser
afficher_heatmap = st.checkbox("Afficher la heatmap")
if afficher_heatmap:
    grille = df_annees.pivot(index="month", columns="year", values="passengers")
    grille = grille.reindex(flights_df["month"].unique())

    fig, ax = plt.subplots()
    sns.heatmap(grille, annot=True, fmt="d", cmap="YlOrRd", ax=ax)
    st.pyplot(fig)