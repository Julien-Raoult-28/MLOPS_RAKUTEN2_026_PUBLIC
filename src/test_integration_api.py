"""
Tests d’intégration pour l’API FastAPI du projet Rakuten MLOps.

Ces tests valident l’intégration complète entre :
- l’API FastAPI
- le loader MLflow (run_id + fallback Production)
- le Model Registry
- le backend SQLite (mapping métier)
- le pipeline sklearn encapsulé
- la sécurité via token

Contrairement aux tests unitaires, ces tests vérifient que
toutes les briques fonctionnent ensemble comme en production.
"""

from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

# ---------------------------------------------------------------------------
# 1. Test intégration : prédiction avec run_id valide
# ---------------------------------------------------------------------------

def test_integration_predict_with_valid_run_id():
    """
    Vérifie que l’API charge correctement un modèle MLflow via un run_id valide.

    Étapes :
    - Envoi d’une requête avec description + run_id
    - Chargement du modèle via mlflow_loader
    - Application du pipeline sklearn
    - Mapping métier via SQLite
    - Réponse JSON enrichie

    Résultat attendu :
    - statut 200
    - présence de prediction, label, run_id_used
    """
    payload = {
        "description": "Chaussures de sport pour homme",
        "run_id": "REPLACE_WITH_VALID_RUN_ID"
    }
    headers = {"x-token": "monsupersecret"}

    response = client.post("/predict", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "prediction" in data
    assert "label" in data
    assert data["run_id_used"] == payload["run_id"]


# ---------------------------------------------------------------------------
# 2. Test intégration : fallback vers modèle Production (sans run_id)
# ---------------------------------------------------------------------------

def test_integration_predict_without_run_id_fallback_production():
    """
    Vérifie que l’API utilise le modèle en Production si aucun run_id n’est fourni.

    Résultat attendu :
    - statut 200
    - run_id_used correspond au modèle Production
    """
    payload = {"description": "Ordinateur portable performant"}
    headers = {"x-token": "monsupersecret"}

    response = client.post("/predict", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "prediction" in data
    assert "label" in data
    assert data["run_id_used"] is not None  # modèle Production


# ---------------------------------------------------------------------------
# 3. Test intégration : mapping métier via SQLite
# ---------------------------------------------------------------------------

def test_integration_mapping_sqlite_backend():
    """
    Vérifie que le backend SQLite renvoie correctement le label métier
    correspondant au code prédictif.

    Résultat attendu :
    - prediction est un int
    - label est une chaîne non vide
    """
    payload = {"description": "Livre de cuisine pour débutants"}
    headers = {"x-token": "monsupersecret"}

    response = client.post("/predict", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data["prediction"], int)
    assert isinstance(data["label"], str)
    assert len(data["label"]) > 0


# ---------------------------------------------------------------------------
# 4. Test intégration : gestion des erreurs MLflow (run_id invalide)
# ---------------------------------------------------------------------------

def test_integration_invalid_run_id_returns_error():
    """
    Vérifie que l’API gère proprement les erreurs MLflow
    lorsqu’un run_id invalide est fourni.

    Résultat attendu :
    - statut 400 ou 500
    - message d’erreur explicite
    """
    payload = {
        "description": "Produit test",
        "run_id": "INVALID_RUN_ID"
    }
    headers = {"x-token": "monsupersecret"}

    response = client.post("/predict", json=payload, headers=headers)
    assert response.status_code in (400, 500)

    data = response.json()
    assert "error" in data


# ---------------------------------------------------------------------------
# 5. Test intégration : robustesse texte très long
# ---------------------------------------------------------------------------

def test_integration_long_text():
    """
    Vérifie que l’API et le pipeline sklearn gèrent correctement
    un texte d’entrée très long (stress test).

    Résultat attendu :
    - statut 200
    - prédiction renvoyée sans crash
    """
    long_text = "Chaussure " * 5000
    payload = {"description": long_text}
    headers = {"x-token": "monsupersecret"}

    response = client.post("/predict", json=payload, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert "prediction" in data
    assert "label" in data


# ---------------------------------------------------------------------------
# 6. Test intégration : sécurité token
# ---------------------------------------------------------------------------

def test_integration_missing_token():
    """
    Vérifie que l’API refuse l’accès si aucun token n’est fourni.

    Résultat attendu :
    - statut 401 Unauthorized
    """
    payload = {"description": "Produit test"}

    response = client.post("/predict", json=payload)
    assert response.status_code == 401
