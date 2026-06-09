import streamlit as st
import joblib

# =========================
# Chargement du modèle
# =========================
@st.cache_resource
def load_model():
    return joblib.load("models/model.pkl")

model = load_model()

# =========================
# App Streamlit
# =========================
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

    # =========================
    # Bouton prediction
    # =========================
    if st.button("Prédire la catégorie"):

        # validation input
        if not designation.strip() and not description.strip():
            st.warning("Merci de remplir au moins un champ.")
            return

        # construction input modèle
        text = f"{designation} {description}".strip()

        try:
            # prediction sklearn pipeline
            prediction = model.predict([text])[0]

            st.success(f"Catégorie prédite : {prediction}")

        except Exception as e:
            st.error("Erreur lors de la prédiction")
            st.exception(e)