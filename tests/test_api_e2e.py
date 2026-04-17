"""
Tests end-to-end (E2E) pour l’API Rakuten.

Objectif pédagogique
--------------------
Les tests E2E (end-to-end) simulent un parcours utilisateur complet.

Ils vérifient :
- qu’un client externe peut appeler l’API,
- avec un token valide,
- avec des données réalistes,
- et obtenir une réponse exploitable.

Ils ne se concentrent pas sur les détails internes, mais sur
le comportement global du système vu de l’extérieur.
"""

from fastapi.testclient import TestClient
from src.api.app import app, API_TOKEN

client = TestClient(app)


def test_e2e_full_prediction_flow():
    """
    Test E2E : parcours complet de prédiction.

    Étapes simulées :
    1. Un client externe prépare une requête JSON réaliste.
    2. Il ajoute le token d’authentification dans les headers.
    3. Il appelle l’endpoint /predict.
    4. Il récupère la prédiction et l’utilise.

    Intérêt :
    - valider que l’API est utilisable telle quelle par un client,
    - vérifier que la documentation (Swagger) est cohérente avec le comportement réel,
    - servir de démonstration simple pour un jury ou un recruteur.
    """
    payload = {
        "designation": "Livre de cuisine",
        "description": "Livre de recettes françaises traditionnelles avec photos",
        "run_id": None,  # utilisation du modèle en Production
    }

    response = client.post(
        "/predict",
        headers={"x-token": API_TOKEN},
        json=payload,
    )

    assert response.status_code == 200

    data = response.json()

    # Vérifications minimales mais parlantes
    assert "prediction_code" in data
    assert "label" in data
    assert "inference_time_ms" in data
    assert isinstance(data["prediction_code"], int)
    assert isinstance(data["label"], str)


def test_e2e_invalid_payload_then_fix():
    """
    Test E2E : scénario d’erreur puis correction.

    Étapes simulées :
    1. Le client envoie une requête invalide (description trop courte).
    2. L’API renvoie une erreur 422 (validation).
    3. Le client corrige la requête.
    4. L’API renvoie une prédiction valide.

    Intérêt :
    - montrer comment un client doit réagir aux erreurs,
    - illustrer le rôle de la validation Pydantic dans un flux réel.
    """
    # Requête invalide
    bad_payload = {
        "designation": "A",
        "description": "B",
    }

    bad_response = client.post(
        "/predict",
        headers={"x-token": API_TOKEN},
        json=bad_payload,
    )

    assert bad_response.status_code == 422

    # Requête corrigée
    good_payload = {
        "designation": "Table en bois",
        "description": "Table de salle à manger en bois massif pour 6 personnes",
    }

    good_response = client.post(
        "/predict",
        headers={"x-token": API_TOKEN},
        json=good_payload,
    )

    assert good_response.status_code == 200
    data = good_response.json()
    assert "prediction_code" in data
    assert "label" in data
