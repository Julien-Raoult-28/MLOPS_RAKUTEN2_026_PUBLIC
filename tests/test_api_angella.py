"""
Tests unitaires pour l'API FastAPI du projet Rakuten.

Ce module couvre :
- les tests simples (statut, token, validation)
- les tests avancés (structure, robustesse, mapping métier)
- le mode hybride MLflow : run_id OU modèle en Production

Chaque test est documenté pour être compréhensible
par des débutants en MLOps et en tests API.
"""

from fastapi.testclient import TestClient
import pandas as pd
from src.api.app import app, API_TOKEN

# Client de test FastAPI
client = TestClient(app)

# Run ID réel à mettre à jour selon ton dernier entraînement MLflow
VALID_RUN_ID = "3cd771b4830740bf823fce572cea2e84"


# ============================================================
# TESTS SIMPLES
# ============================================================

def test_root_ok():
    """
    Vérifie que l'endpoint racine "/" fonctionne correctement.

    Objectifs :
    - S'assurer que l'API répond
    - Vérifier le message de santé
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API Rakuten opérationnelle"}


def test_predict_unauthorized_without_token():
    """
    Vérifie que l'accès à /predict est refusé sans token.

    Objectifs :
    - Tester la sécurité
    - S'assurer que l'authentification est obligatoire
    """
    response = client.post(
        "/predict",
        json={
            "designation": "Chaise",
            "description": "Chaise en bois",
            "run_id": VALID_RUN_ID
        }
    )
    assert response.status_code == 401


def test_predict_with_token_and_bad_body():
    """
    Vérifie que la validation Pydantic fonctionne.

    Objectifs :
    - Tester les erreurs de validation (422)
    - Vérifier que les champs invalides sont refusés
    """
    response = client.post(
        "/predict",
        headers={"x-token": API_TOKEN},
        json={
            "designation": "",
            "description": "x"
        }
    )
    assert response.status_code == 422


def test_predict_success_hybrid():
    """
    Vérifie qu'une prédiction fonctionne dans les deux modes :
    - avec run_id (modèle MLflow spécifique)
    - sans run_id (modèle en Production du Model Registry)
    """

    # Mode avec run_id
    response = client.post(
        "/predict",
        headers={"x-token": API_TOKEN},
        json={
            "designation": "Chaise en bois",
            "description": "Chaise de salle à manger en bois massif",
            "run_id": VALID_RUN_ID
        }
    )
    assert response.status_code == 200
    assert "prediction" in response.json()

    # Mode sans run_id
    response = client.post(
        "/predict",
        headers={"x-token": API_TOKEN},
        json={
            "designation": "Chaise en bois",
            "description": "Chaise de salle à manger en bois massif"
        }
    )
    assert response.status_code == 200
    assert "prediction" in response.json()


# ============================================================
# TESTS COMPLEXES
# ============================================================

def test_predict_invalid_run_id():
    """
    Vérifie le comportement de l'API avec un run_id MLflow invalide.

    Objectifs :
    - Tester la robustesse
    - L'API doit renvoyer 400 ou 500 selon l'erreur interne
    """
    response = client.post(
        "/predict",
        headers={"x-token": API_TOKEN},
        json={
            "designation": "Chaise",
            "description": "Chaise en bois massif",
            "run_id": "RUN_ID_INEXISTANT_123"
        }
    )
    assert response.status_code in [400, 500]


def test_predict_response_structure():
    """
    Vérifie la structure complète de la réponse JSON.

    Objectifs :
    - Garantir un contrat API stable
    - Vérifier la présence des champs obligatoires
    """
    response = client.post(
        "/predict",
        headers={"x-token": API_TOKEN},
        json={
            "designation": "Chaise",
            "description": "Chaise en bois massif",
            "run_id": VALID_RUN_ID
        }
    )

    assert response.status_code == 200

    data = response.json()
    pred = data["prediction"]

    assert isinstance(pred["label"], str)
    assert "confidence" in pred
    assert isinstance(pred["inference_time_ms"], float)
    assert "model_uuid" in pred
    assert "model_version" in pred
    assert "timestamp" in pred


def test_predict_label_mapping_valid():
    """
    Vérifie que le label retourné existe dans le mapping métier.

    Objectifs :
    - Garantir la cohérence entre modèle et catégories officielles
    """
    mapping_df = pd.read_csv("data/processed/Y_train_encode.csv")
    valid_labels = set(mapping_df["libelle_type_code"].astype(str))

    response = client.post(
        "/predict",
        headers={"x-token": API_TOKEN},
        json={
            "designation": "Chaise en bois",
            "description": "Chaise de salle à manger en bois massif",
            "run_id": VALID_RUN_ID
        }
    )

    assert response.status_code == 200
    assert response.json()["prediction"]["label"] in valid_labels


def test_predict_long_description():
    """
    Vérifie que l'API accepte une description très longue.

    Objectifs :
    - Tester la robustesse du preprocessing
    - S'assurer que l'API ne plante pas
    """
    long_description = "Chaise en bois massif " * 500

    response = client.post(
        "/predict",
        headers={"x-token": API_TOKEN},
        json={
            "designation": "Chaise",
            "description": long_description,
            "run_id": VALID_RUN_ID
        }
    )

    assert response.status_code == 200
    assert "label" in response.json()["prediction"]


def test_predict_with_wrong_token():
    """
    Vérifie que l'API refuse un token incorrect.

    Objectifs :
    - Tester la sécurité
    """
    response = client.post(
        "/predict",
        headers={"x-token": "BAD_TOKEN_123"},
        json={
            "designation": "Chaise",
            "description": "Chaise en bois massif",
            "run_id": VALID_RUN_ID
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Token invalide ou manquant"
