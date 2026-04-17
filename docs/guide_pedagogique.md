Guide pédagogique complet — Projet MLOps Rakuten (Version 2)

Comprendre, installer, exécuter et tester le pipeline de bout en bout

🟦 1. Introduction : Pourquoi ce guide ?
Ce document est destiné :
à toute personne qui veut comprendre comment fonctionne la Version 2 du projet Rakuten

Il explique pas à pas, sans prérequis :

comment installer le projet

comment lancer MLflow

comment entraîner un modèle

comment fonctionne le Model Registry

comment fonctionne l’API

comment tester l’API

comment comprendre la prédiction

comment fonctionne le mode hybride

comment lire les tests automatisés

Ce guide complète le README professionnel, qui lui est plus concis et orienté usage.

🟩 2. Comprendre l’architecture du projet
Voici la structure simplifiée :

Code
FEV26-CMLOPS-RAKUTEN/
│
├── src/
│   ├── api/
│   │   ├── app.py                ← API FastAPI
│   │   ├── prediction_service.py ← Logique métier de prédiction
│   │   ├── utils.py              ← Chargement modèle MLflow
│   │   └── schemas.py            ← Validation Pydantic
│   │
│   ├── models/
│   │   └── train.py              ← Entraînement du modèle
│   │
│   └── utils/                    ← Fonctions utilitaires
│
├── tests/                        ← Tests unitaires, intégration, E2E
├── mlflow.db                     ← Base MLflow (tracking)
├── mlruns/                       ← Artefacts MLflow
├── README.md                     ← Documentation professionnelle
└── docs/                         ← Documentation pédagogique
Ce qu’il faut retenir :
src/api/ → tout ce qui concerne l’API

src/models/ → entraînement du modèle

mlflow.db + mlruns/ → tout l’historique des modèles

tests/ → vérifie que tout fonctionne

docs/ → documents pédagogiques

🟦 3. Installation du projet (pas à pas)
3.1. Cloner le projet
bash
git clone <URL_DU_REPO>
cd FEV26-CMLOPS-RAKUTEN
3.2. Créer un environnement virtuel
bash
python -m venv .venv
3.3. Activer l’environnement
Windows PowerShell :
powershell
.\.venv\Scripts\activate
3.4. Installer les dépendances
bash
pip install -r requirements.txt
3.5. Définir PYTHONPATH (important)
powershell
$env:PYTHONPATH = (Get-Location)
Sans cette ligne, Python ne trouve pas le dossier src/.

🟦 4. Lancer MLflow (interface web)
MLflow permet de :

suivre les entraînements

comparer les modèles

gérer les versions

définir un modèle Production

Lancer MLflow :
cmd
mlflow ui
Puis ouvrir :

👉 http://127.0.0.1:5000 (127.0.0.1 in Bing)

🟩 5. Entraîner un modèle (pas à pas)
Le script d’entraînement se trouve dans :

Code
src/models/train.py
Lancer un entraînement complet :
bash
python src/models/train.py --mode full
Ce que fait ce script :
Charge les données

Prépare le texte (TF‑IDF)

Entraîne un modèle LinearSVC

Évalue le modèle

Loggue dans MLflow :

paramètres

métriques

artefacts

modèle

Enregistre une nouvelle version dans le Model Registry

Où voir le résultat ?
Dans MLflow UI → onglet Models → rakuten_classifier.

🟦 6. Comprendre le Model Registry
Le Model Registry contient :

toutes les versions du modèle

la version Production

les modèles en Staging

les modèles archivés

Pourquoi c’est important ?
Parce que l’API utilise :

soit un modèle Production

soit un modèle spécifique via run_id

C’est ce qu’on appelle le mode hybride.

🟩 7. Lancer l’API FastAPI
bash
uvicorn src.api.app:app --reload
Ouvrir la documentation interactive :
👉 http://127.0.0.1:8000/docs

L’API contient :
GET / → test simple

POST /predict → prédiction complète

🟦 8. Faire une prédiction (pas à pas)
8.1. Exemple de requête
Body :

json
{
  "designation": "chaussure sport",
  "description": "chaussures running homme",
  "run_id": null
}
Header :

Code
x-token: RAKUTEN_SECRET_123
8.2. Réponse obtenue
json
{
  "prediction_code": 21,
  "label": "Fournitures Papeterie",
  "run_id": null,
  "confidence": null,
  "inference_time_ms": 12.4,
  "model_uuid": "unknown",
  "model_version": "Production",
  "timestamp": "2026-04-17T08:12:45Z"
}
Ce que signifie chaque champ :
Champ	Signification
prediction_code	Code numérique prédit par le modèle
label	Libellé métier (décodé depuis le mapping)
run_id	Run MLflow utilisé (ou null si Production)
confidence	Probabilité (null pour LinearSVC)
inference_time_ms	Temps d’inférence
model_uuid	Identifiant interne
model_version	Version MLflow (Production ou run_id)
timestamp	Horodatage ISO

🟧 9. Comprendre le mode hybride
1. run_id = null
→ L’API charge automatiquement le modèle Production.

2. run_id = "xxxx"
→ L’API charge un modèle spécifique depuis MLflow.

Pourquoi c’est puissant ?
permet de tester plusieurs modèles

permet de comparer les versions

permet de faire du A/B testing

permet de reproduire un bug

🟦 10. Tests automatisés (pas à pas)
Les tests se trouvent dans :

Code
tests/
10.1. Tests unitaires
bash
pytest tests/test_api_unit.py -v
Vérifient :

validation Pydantic

sécurité token

erreurs 401 / 422

structure JSON

10.2. Tests d’intégration
bash
pytest tests/test_api_integration.py -v
Vérifient :

interaction API ↔ MLflow

mapping métier

structure complète

10.3. Tests E2E
bash
pytest tests/test_api_e2e.py -v
Vérifient :

parcours complet utilisateur

cohérence API / Swagger

comportement réel

🟩 11. Résumé pour l’équipe
À retenir :

MLflow = mémoire du projet

Model Registry = version officielle du modèle

API = interface pour prédire

prediction_service = cœur métier

tests = garantissent la qualité

mapping CSV = traduction code → label

mode hybride = flexibilité totale

🟦 12. Pour aller plus loin
Dockerisation

CI/CD GitHub Actions

Monitoring

Endpoint /health

Dashboard Streamlit

Orchestration Airflow

🟩 13. Conclusion
Ce guide vous permet de :

comprendre la V2

installer le projet

entraîner un modèle

utiliser MLflow

lancer l’API

faire une prédiction

comprendre le mode hybride

exécuter les tests

Vous êtes maintenant capables d’utiliser toute la chaîne MLOps du projet Rakuten.