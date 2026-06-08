import streamlit as st

from app_streamlit.core.layout import apply_layout
from app_streamlit.core.sidebar import render_sidebar
from app_streamlit.page_modules import presentation
from app_streamlit.page_modules import Objectif_et_Contexte
from app_streamlit.page_modules import Orchestration_et_Deploiement
from app_streamlit.page_modules import prediction

st.set_page_config(
    page_title="Rakuten FEV26MLOPS",
    page_icon="app_streamlit/assets/images/favicon_Rakuten.png",
    layout="wide"
)

apply_layout()

page = render_sidebar()

#if page == "Présentation du projet":
#    presentation.run()

if page == "Objectif et Contexte":
    Objectif_et_Contexte.run()

elif page == "Orchestration et Déploiement":
    Orchestration_et_Deploiement.run()

elif page == "Démonstration du modèle":
    prediction.run()