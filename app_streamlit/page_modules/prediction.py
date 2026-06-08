import streamlit as st
import requests

def run():

    st.title("Test du modèle Rakuten")

    designation = st.text_input(
        "Désignation",
        placeholder="Ex : iPhone 14 Pro Max 256Go"
    )

    description = st.text_area(
        "Description",
        placeholder="Description du produit..."
    )

    if st.button("Prédire la catégorie"):

        payload = {
            "designation": designation,
            "description": description
        }

        try:
            response = requests.post(
                "http://localhost:8000/predict",
                json=payload,
                timeout=10
            )

            response.raise_for_status()

            result = response.json()

            st.success(
                f"Catégorie prédite : {result['label']}"
            )

            st.write("Code catégorie :", result["prediction"])

        except Exception as e:
            st.error(f"Erreur API : {e}")