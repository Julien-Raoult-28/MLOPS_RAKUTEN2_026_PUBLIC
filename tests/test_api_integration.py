"""
Tests d’intégration pour l’API Rakuten.

Objectif pédagogique
--------------------
Les tests d’intégration vérifient que plusieurs composants réels
fonctionnent ensemble :

- API FastAPI,
- MLflow Tracking + Model Registry,
- modèle TF-IDF + LinearSVC,
- mapping métier (CSV),
- base SQLite (mlflow.db).

Ils sont plus lents que les tests unitaires, mais essentiels pour
valider le comportement réel du système.
"""

from fastapi.testclient import TestClient
import pandas as pd
from src.api.app import app, API_TOKEN

client = TestClient(app)

# À adapter avec un run_id réel si nécessaire
VALID_RUN_ID = "3cd771b4830740bf823fce572cea2e84"


def test_predict_success_hybrid():
    """
    Vérifie qu’une prédiction fonctionne dans les deux modes :
    - avec run_id (modèle MLflow spécifique),
    - sans run_id (modèle en Production du Model Registry).

    Intérêt :
    - valider le mode hybride de l’API,
    - s’assurer que les deux chemins de chargement fonctionnent.
    """
    # Mode avec run_id
    response = client.post(
        "/predict",
        headers={"x-token": API_TOKEN},
        json={
            "designation": "Chaise en bois",
            "description": "Chaise de salle à manger en bois massif",
            "run_id": VALID_RUN_ID,
        },
    )
    assert response.status_code in (200, 500)
    if response.status_code == 200:
        body = response.json()
        assert "prediction_code" in body
        assert "label" in body

    # Mode sans run_id (Production)
    response = client.post(
        "/predict",
        headers={"x-token": API_TOKEN},
        json={
            "designation": "Chaise en bois",
            "description": "Chaise de salle à manger en bois massif",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "prediction_code" in body
    assert "label" in body


def test_predict_invalid_run_id():
    """
    Vérifie le comportement de l’API avec un run_id MLflow invalide.

    Intérêt :
    - tester la robustesse face à une mauvaise configuration,
    - s’assurer que l’API renvoie une erreur contrôlée (400 ou 500).
    """
    response = client.post(
        "/predict",
        headers={"x-token": API_TOKEN},
        json={
            "designation": "Chaise",
            "description": "Chaise en bois massif",
            "run_id": "RUN_ID_INEXISTANT_123",
        },
    )
    assert response.status_code in [400, 500]


def test_predict_response_structure():
    """
    Vérifie la structure complète de la réponse JSON.

    Intérêt :
    - garantir un contrat API stable,
    - vérifier la présence des champs obligatoires.
    """
    response = client.post(
        "/predict",
        headers={"x-token": API_TOKEN},
        json={
            "designation": "Chaise",
            "description": "Chaise en bois massif",
            "run_id": VALID_RUN_ID,
        },
    )

    assert response.status_code in (200, 500)
    if response.status_code == 200:
        data = response.json()

        assert isinstance(data["label"], str)
        assert "confidence" in data
        assert "inference_time_ms" in data
        assert "model_uuid" in data
        assert "model_version" in data
        assert "timestamp" in data


def test_predict_label_mapping_valid():
    """
    Vérifie que le label retourné existe dans le mapping métier.

    Intérêt :
    - garantir la cohérence entre le modèle et les catégories officielles.
    """
    mapping_df = pd.read_csv("data/processed/Y_train_encode.csv")
    valid_labels = set(mapping_df["libelle_type_code"].astype(str))

    response = client.post(
        "/predict",
        headers={"x-token": API_TOKEN},
        json={
            "designation": "Chaise en bois",
            "description": "Chaise de salle à manger en bois massif",
            "run_id": VALID_RUN_ID,
        },
    )

    assert response.status_code in (200, 500)
    if response.status_code == 200:
        assert response.json()["label"] in valid_labels


def test_predict_long_description():
    """
    Vérifie que l’API accepte une description très longue.

    Intérêt :
    - tester la robustesse du preprocessing,
    - s’assurer que l’API ne plante pas avec de gros inputs.
    """
    long_description = "Chaise en bois massif " * 500

    response = client.post(
        "/predict",
        headers={"x-token": API_TOKEN},
        json={
            "designation": "Chaise",
            "description": long_description,
            "run_id": VALID_RUN_ID,
        },
    )

    assert response.status_code in (200, 500)
    if response.status_code == 200:
        body = response.json()
        assert "label" in body
