import streamlit as st

def apply_layout():

    st.markdown("""
        <div style="
        position: fixed;
        top: 60px;
        left: 100px;
        width: 100%;
        height: 70px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #efefef;
        z-index: 1000;
    ">
        <h3 style="color: #bf0000; margin: 0;">
            Rakuten - Industrialisation complète d’un pipeline de Machine Learning en environnement MLOps
        </h3>
    </div>

    <div style="margin-top:70px;"></div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
        <style>
        section[data-testid="stSidebar"] {
            background-color: #efefef;
        }

        section[data-testid="stSidebar"] * {
            color: #bf0000 !important;
        }
        </style>
    """, unsafe_allow_html=True)