import streamlit as st
import joblib
import pandas as pd

@st.cache_resource
def load_model():
    return joblib.load("models/model.pkl")

model = load_model()

mapping_df = pd.read_csv("data/processed/Y_train_encode.csv")
mapping = mapping_df.set_index("prdtypecode_encoded")["libelle_type_code"].to_dict()

def run():

    st.title("Test du modèle Rakuten")

    designation = st.text_input("Désignation")
    description = st.text_area("Description")

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

            # 🔥 AJOUT IMPORTANT
            label = mapping.get(prediction, "Inconnu")

            st.success(f"Catégorie : {label}")
            st.write("Code brut :", prediction)

        except Exception as e:
            st.error("Erreur modèle")
            st.exception(e)