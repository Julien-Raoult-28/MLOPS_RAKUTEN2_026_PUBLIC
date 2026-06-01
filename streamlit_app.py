import streamlit as st

from streamlit.core.layout import apply_layout
from streamlit.core.sidebar import render_sidebar
from streamlit.page_modules import presentation
from streamlit.page_modules import Objectif_et_Contexte
from streamlit.page_modules import Orchestration_et_Deploiement
from streamlit.page_modules import prediction

st.set_page_config(
    page_title="Rakuten FEV26MLOPS",
    page_icon="assets/images/favicon_Rakuten.png",
    layout="wide"
)

apply_layout()

page = render_sidebar()

if page == "Présentation du projet":
    presentation.run()

elif page == "Objectif et Contexte":
    Objectif_et_Contexte.run()

elif page == "Orchestration et Déploiement":
    Orchestration_et_Deploiement.run()

elif page == "Démonstration du modèle":
    prediction.run()