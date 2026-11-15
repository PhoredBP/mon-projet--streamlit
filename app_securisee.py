import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu

# Initialisation de la session
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "nom" not in st.session_state:
    st.session_state["nom"] =""

# Vérification des identifiants
@st.cache_data
def load_accounts():
    return pd.read_csv("data/accounts.csv")

def authenticate(nom_input, mot_de_passe_input):
    df_accounts = load_accounts()
    # Verification de la correspondance nom d'utilisateur et mot de passe
    utilisateur_valide = df_accounts[(df_accounts["nom"] == nom_input) & (df_accounts["mot_de_passe"].astype(str) == mot_de_passe_input)]
    return not utilisateur_valide.empty

# Gestion de l'affichage conditionel
if not st.session_state["logged_in"]:
    # Page de connexion
    st.title("Connexion à l'application")
    st.subheader("Veuillez vous identifier pour accéder au contenu")

    nom_input = st.text_input("Nom d'utilisateur")
    mot_de_passe_input = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if authenticate(nom_input, mot_de_passe_input):
            st.session_state["logged_in"] = True
            st.session_state["nom"] = nom_input
            st.success(f"Bienvenue: {nom_input}")
            st.rerun() # Relance le script pour afficher l'application securisé
        else: 
            st.error("Nom d'utilisateur ou mot de passe incorrect.")
    st.stop()
   
        # Application sécurisée (Utilisateur connecté)
        # Bar latérale: Message de bienvenue et bouton de déconnexxion
with st.sidebar:
    st.write(f"Bienvenue, **{st.session_state["nom"]}**!")
    if st.button("Se déconnecter"):
        st.session_state["logged_in"] = False
        st.session_state["nom"] = ""
        st.rerun()
    st.divider()
# Bar latérale: Menu de navigation
with st.sidebar:
    selected_page = option_menu(
        menu_title="Menu principal",
        options=["Accueil", "Galerie Photos"],
        icons=["house", "images"],
        default_index=0
    )
    # Contenu principal des pages
if selected_page == "Accueil":
    st.title("Page d'Accueil Réservée")
    st.write("Ce contenu est uniquement accessible aux utilisateurs authentifiés")
elif selected_page == "Galerie Photos":
    st.title("Album de photos")
    st.write("Voici la galerie multimédia organisée sur 3 colonnes")
        
    # Exemple d'afichage d'images alignées sur 3 colonnes
    cols = st.columns(3)
    sample_images = [
        "images/2 dogmas.jpg",
        "images/4 debull.jpg",
        "images/5 vegan turkey.jpg"
    ]
    for idx, img_url in enumerate(sample_images):
        with cols[idx % 3]:
            st.image(img_url, caption=f"Image {idx+1}", 
use_container_width=True)