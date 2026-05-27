import streamlit as st

from core.layout import apply_layout
from core.sidebar import render_sidebar
from page_modules import presentation
from page_modules import PAGE_2
from page_modules import PAGE_3
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

elif page == "PAGE_2":
    PAGE_2.run()

elif page == "PAGE_3":
    PAGE_3.run()

elif page == "PAGE_4":
    PAGE_4.run()