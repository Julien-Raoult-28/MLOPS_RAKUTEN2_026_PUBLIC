"""
Tests unitaires pour l'API FastAPI du projet Rakuten.

Ce fichier contient :
- des tests simples (statut, token, validation)
- des tests complexes (structure, mapping métier, robustesse)

Chaque test est documenté pour faciliter la compréhension
par des débutants en MLOps et en tests API.

Le mode hybride de l'API est testé :
- avec run_id (modèle MLflow spécifique)
- sans run_id (modèle en Production du Model Registry)
"""

from fastapi.testclient import TestClient
import pandas as pd
from src.api.app import app, API_TOKEN

# Client de test FastAPI
client = TestClient(app)

# Run ID réel utilisé pour tester le chargement d'un modèle MLflow
VALID_RUN_ID = "1eb81543c0cc4b9c8d9cd5352d1fe57c"


# ============================================================
# TESTS SIMPLES
# ============================================================

def test_root_ok():
    """
    Vérifie que l'endpoint racine "/" fonctionne correctement.

    Objectif :
    - S'assurer que l'API est en ligne
    - Vérifier le message de santé ("healthcheck")
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API Rakuten opérationnelle"}


def test_predict_unauthorized_without_token():
    """
    Vérifie que l'accès à /predict est refusé sans token.

    Objectif :
    - Tester la sécurité de l'API
    - S'assurer que l'authentification est obligatoire
    """
    response = client.post(
        "/predict",
        json={
            "designation": "Chaise",
            "description": "Chaise en bois",
            "run_id": "12345"
        }
    )
    assert response.status_code == 401


def test_predict_with_token_and_bad_body():
    """
    Vérifie que la validation Pydantic fonctionne.

    Objectif :
    - Tester les erreurs de validation (422)
    - Vérifier que les champs trop courts sont refusés
    """
    response = client.post(
        "/predict",
        headers={"x-token": API_TOKEN},
        json={
            "designation": "",
            "description": "x"
            # run_id non requis
        }
    )
    assert response.status_code == 422


def test_predict_success():
    """
    Vérifie qu'une prédiction complète fonctionne.

    Objectif :
    - Tester le chemin complet : token + validation + MLflow
    - Vérifier que la réponse contient bien une prédiction
    - Tester les deux modes : avec run_id et sans run_id
    """

    # --- Mode avec run_id ---
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

    # --- Mode sans run_id (Model Registry) ---
    response = client.post(
        "/predict",
        headers={"x-token": API_TOKEN},
        json={
            "designation": "Chaise en bois",
            "description": "Chaise de salle à manger en bois massif"
            # pas de run_id
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

    Objectif :
    - Tester la robustesse face à un modèle introuvable
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

    Objectif :
    - S'assurer que tous les champs attendus sont présents
    - Garantir un contrat API stable pour les futurs consommateurs
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
    assert "prediction" in data

    pred = data["prediction"]

    # Champs obligatoires
    assert "label" in pred
    assert isinstance(pred["label"], str)

    assert "confidence" in pred  # Peut être None selon le modèle

    assert "inference_time_ms" in pred
    assert isinstance(pred["inference_time_ms"], float)

    assert "model_uuid" in pred
    assert "model_version" in pred
    assert "timestamp" in pred


def test_predict_label_mapping_valid():
    """
    Vérifie que le label retourné par le modèle existe dans le mapping métier.

    Objectif :
    - Garantir la cohérence entre le modèle et les catégories officielles
    - Éviter les labels fantômes ou incohérents
    """
    mapping_df = pd.read_csv("data/processed/Y_train_encode.csv")
    mapping_df = mapping_df[["prdtypecode_encoded", "libelle_type_code"]].drop_duplicates()

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

    pred = response.json()["prediction"]
    assert pred["label"] in valid_labels


def test_predict_long_description():
    """
    Vérifie que l'API accepte une description très longue.

    Objectif :
    - Tester la robustesse du preprocessing
    - S'assurer que l'API ne plante pas avec de gros textes
    """
    long_description = "Chaise en bois massif " * 500  # ~10 000 caractères

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

    pred = response.json()["prediction"]
    assert "label" in pred


def test_predict_with_wrong_token():
    """
    Vérifie que l'API refuse un token incorrect.

    Objectif :
    - Tester la sécurité
    - S'assurer que seul le bon token permet l'accès à /predict
    """
    wrong_token = "BAD_TOKEN_123"

    response = client.post(
        "/predict",
        headers={"x-token": wrong_token},
        json={
            "designation": "Chaise",
            "description": "Chaise en bois massif",
            "run_id": VALID_RUN_ID
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Token invalide ou manquant"
