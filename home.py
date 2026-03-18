import streamlit as st

st.set_page_config(page_title="Accueil - Prénoms", layout="wide")

st.title("📊 Analyse des prénoms en France")
st.markdown("Explore l'évolution d'un prénom dans le temps et dans l'espace.")
st.markdown("""
Cette interface est un dashboard intéractif permettant la visualisation de données sur des 
prénoms en France (source : [data.gouv](https://www.insee.fr/fr/statistiques/7633685)). 

On pourra visualiser ces prénoms selon :
- 📈 évolution selon les années  
- 🗺️ répartition par départements  
- 🚻 distinction par sexe  

👉 Utilise le menu à gauche pour aller sur la page **Dashboard**.
""")

st.success("➡️ Sélectionne **Dashboard** dans la barre latérale pour commencer !")
st.page_link(
    "pages/1_dashboard.py",
    label="Accéder au Dashboard",
    icon="🚀",
    use_container_width=True,
)
