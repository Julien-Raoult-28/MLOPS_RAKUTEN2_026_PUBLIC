import streamlit as st

from core.layout import apply_layout
from core.sidebar import render_sidebar
from page_modules import presentation
from page_modules import Objectif_et_Contexte
from page_modules import Orchestration_et_Deploiement
from page_modules import PAGE_4

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

elif page == "PAGE_4":
    PAGE_4.run()