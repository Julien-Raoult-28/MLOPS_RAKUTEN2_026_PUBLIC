from src.models.predict import load_model_from_mlflow, prepare_input, predict_label
import mlflow

def predict_product(designation: str, description: str, run_id: str):
    """
    Service métier : prédire la catégorie d'un produit.
    - Vérifie les inputs
    - Charge le modèle MLflow
    - Prépare les données
    - Retourne la prédiction
    """

    print(">>> predict_product() appelé")
    print(">>> designation =", designation)
    print(">>> description =", description)
    print(">>> run_id =", run_id)

    # 1. Vérification simple des inputs
    if not isinstance(designation, str) or not isinstance(description, str):
        raise ValueError("Les champs 'designation' et 'description' doivent être des chaînes de caractères.")

    if not run_id:
        raise ValueError("Le run_id MLflow est obligatoire.")

    # 2. Configurer MLflow
    tracking_uri = "file:///C:/Users/angel/Desktop/A/Datascientest/Projet MLOps/FEV26-CMLOPS-RAKUTEN/mlruns"
    print(">>> tracking_uri =", tracking_uri)

    mlflow.set_tracking_uri(tracking_uri)

    # 3. Charger le modèle MLflow
    print(">>> Chargement du modèle MLflow...")
    model = load_model_from_mlflow(run_id)
    print(">>> Modèle chargé avec succès")

    # 4. Préparer les données
    print(">>> Préparation des données...")
    X = prepare_input(designation, description)
    print(">>> Données préparées :", X)

    # 5. Prédire
    print(">>> Prédiction en cours...")
    prediction = predict_label(model, X)
    print(">>> Prédiction OK :", prediction)

    # 6. Retourner le résultat
    return {
        "designation": designation,
        "description": description,
        "prediction": prediction,
        "run_id": run_id
    }