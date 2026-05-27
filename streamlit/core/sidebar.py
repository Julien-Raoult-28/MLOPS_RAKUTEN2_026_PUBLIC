import streamlit as st

PAGES = [
    "Présentation du projet",
    "PAGE_2",
    "PAGE_3",
    "PAGE_4"
]

def render_sidebar():
    with st.sidebar:
        st.image("assets/images/rakuten.png", use_container_width=True)
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