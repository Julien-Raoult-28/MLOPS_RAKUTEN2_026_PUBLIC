import streamlit as st
import joblib

@st.cache_resource
def load_model():
    return joblib.load("models/model.pkl")

model = load_model()

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

    st.write("Type du modèle :", type(model))

    if st.button("Prédire la catégorie"):

        if not designation and not description:
            st.warning("Merci de remplir au moins un champ.")
            return

        text = f"{designation} {description}"

        st.write("Test input :", text)

        try:
            prediction = model.predict([text])[0]

            st.success(f"Catégorie prédite : {prediction}")

        except Exception as e:
            st.error(f"Erreur modèle : {e}")