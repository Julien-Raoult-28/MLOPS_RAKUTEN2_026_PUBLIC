import streamlit as st
import joblib
import pandas as pd

@st.cache_resource
def load_model():
    return joblib.load("models/model.pkl")

model = load_model()

def run():

    st.title("Test du modèle Rakuten")

    designation = st.text_input("Désignation")
    description = st.text_area("Description")

    st.write("Type du modèle :", type(model))

    if st.button("Prédire la catégorie"):

        if not designation.strip() and not description.strip():
            st.warning("Remplis au moins un champ")
            return

        try:
            input_df = pd.DataFrame([{
                "designation": designation,
                "description": description
            }])

            prediction = model.predict(input_df)[0]

            st.success(f"Catégorie : {prediction}")

        except Exception as e:
            st.error("Erreur modèle")
            st.exception(e)