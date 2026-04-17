"""
Tests unitaires pour l’API Rakuten.

Objectif pédagogique
--------------------
Les tests unitaires vérifient des briques isolées de l’application :
- une route FastAPI,
- la validation Pydantic,
- la sécurité (token),
sans dépendre de MLflow, du modèle ou de la base SQLite.

Ils doivent être :
- rapides,
- stables,
- indépendants des données métiers,
- exécutables à chaque modification de code.
"""

from fastapi.testclient import TestClient
from src.api.app import app, API_TOKEN

client = TestClient(app)


def test_root_ok():
    """
    Vérifie que l’endpoint racine "/" fonctionne correctement.

    Intérêt :
    - s’assurer que l’API démarre,
    - fournir un healthcheck simple.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API Rakuten opérationnelle"}


def test_predict_unauthorized_without_token():
    """
    Vérifie que l’accès à /predict est refusé sans token.

    Intérêt :
    - tester la sécurité,
    - garantir que l’authentification est obligatoire.
    """
    response = client.post(
        "/predict",
        json={
            "designation": "Chaise",
            "description": "Chaise en bois",
        },
    )
    assert response.status_code == 401


def test_predict_with_wrong_token():
    """
    Vérifie que l’API refuse un token incorrect.

    Intérêt :
    - s’assurer que seul le bon token est accepté,
    - éviter les accès non autorisés.
    """
    response = client.post(
        "/predict",
        headers={"x-token": "BAD_TOKEN_123"},
        json={
            "designation": "Chaise",
            "description": "Chaise en bois massif",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Token invalide ou manquant"


def test_predict_with_token_and_bad_body():
    """
    Vérifie que la validation Pydantic fonctionne.

    Intérêt :
    - s’assurer que les entrées invalides sont rejetées,
    - vérifier le statut HTTP 422 (Unprocessable Entity).
    """
    response = client.post(
        "/predict",
        headers={"x-token": API_TOKEN},
        json={
            "designation": "",
            "description": "x",
        },
    )
    assert response.status_code == 422
