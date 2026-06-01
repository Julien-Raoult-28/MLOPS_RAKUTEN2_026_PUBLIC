import streamlit as st

PAGES = [
    "Présentation du projet",
    "Objectif et Contexte",
    "Orchestration et Déploiement",
    "Démonstration du modèle"
]

def render_sidebar():
    with st.sidebar:
        st.image("streamlit/assets/images/rakuten.png", use_container_width=True)
        st.markdown("<br>", unsafe_allow_html=True)

        st.title("Sommaire")
        page = st.radio("", PAGES)

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown("""
        **Auteurs :**  
        Angella FONTAINE  
        Fatiha IDDER  
        Julien RAOULT
        """)

    return page