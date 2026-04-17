# 📘 Changelog
Toutes les modifications notables de ce projet sont documentées dans ce fichier.  
Format conforme à **Keep a Changelog** et au **Semantic Versioning**.

---

## [2.0.0] - 2026-04-17
### 🎯 Version majeure — refonte complète du pipeline MLOps
Cette version marque une transformation profonde du projet :  
l’API, le pipeline MLflow, la structure du code, les tests et la documentation ont été entièrement revus pour atteindre un niveau **professionnel**, **robuste**, **traçable** et **industrialisation-ready**.

---

## 🟦 Added — Nouveautés

### 🔹 Mode hybride MLflow (run_id / Production)
- L’API peut charger :
  - un modèle spécifique via `run_id`
  - ou automatiquement le modèle **Production** du Model Registry.

### 🔹 Model Registry MLflow
- Ajout d’un registre de modèles complet :
  - versions v1, v2, v3…
  - promotion en Production
  - rollback possible
  - traçabilité totale.

### 🔹 Prédiction enrichie (réponse API)
La réponse JSON contient désormais :
- `prediction_code`
- `label`
- `confidence`
- `inference_time_ms`
- `model_uuid`
- `model_version`
- `timestamp`

### 🔹 Tests automatisés complets
- Tests **unitaires**
- Tests **d’intégration** (API ↔ MLflow)
- Tests **E2E** (parcours utilisateur complet)
- 100 % des tests PASSENT.

### 🔹 Schémas Pydantic v2 complets
- Validation stricte
- Types robustes
- Cohérence totale avec la réponse API.

### 🔹 Documentation professionnelle
- README réécrit
- Rapport de soutenance
- Rapport V1 → V2
- Architecture MLOps clarifiée.

---

## 🟧 Changed — Modifications majeures

### 🔹 Architecture du projet simplifiée
- Suppression de la complexité inutile (SQLite backend, loaders séparés).
- Regroupement logique :
  - `api/app.py`
  - `api/prediction_service.py`
  - `api/utils.py`
  - `api/schemas.py`
- Structure plus lisible, plus claire, plus MLOps-friendly.

### 🔹 Mapping métier via CSV
- Remplacement du backend SQLite par un mapping CSV chargé en mémoire.
- Plus simple, plus portable, plus rapide.

### 🔹 API FastAPI refactorisée
- Code plus propre et plus robuste.
- Gestion d’erreurs améliorée.
- Swagger cohérent avec la réalité.

### 🔹 Pipeline MLflow stabilisé
- Logging complet (params, metrics, artefacts).
- Conversion numpy → types Python natifs.
- Chargement modèle via Registry.

---

## 🟥 Removed — Suppressions

### 🔹 Backend SQLite
- Remplacé par un mapping CSV plus simple et plus portable.

### 🔹 mlflow_loader séparé
- Fusionné dans `utils.py` pour simplifier l’architecture.

### 🔹 Ancienne API V1 minimaliste
- Remplacée par une API complète, robuste et testée.

### 🔹 Ancien README orienté pipeline ML
- Remplacé par un README professionnel orienté MLOps.

---

## ⚠️ Breaking Changes — Changements cassants

- Suppression du backend SQLite (incompatible avec V1).
- Refactor complet de l’API (schémas modifiés).
- Ancienne réponse API incompatible avec la nouvelle version.
- Structure du projet modifiée (fichiers déplacés).
- Suppression de mlflow_loader (imports à mettre à jour).
- Tests V1 incompatibles avec V2.

---

## 📦 Migration Guide — V1 → V2

Pour migrer un projet basé sur la V1 vers la V2 :

1. **Mettre à jour les imports**
   - Supprimer les références à `sqlite_backend`.
   - Remplacer par le mapping CSV chargé dans `prediction_service.py`.

2. **Mettre à jour les appels API**
   - Adapter les clients pour utiliser les nouveaux champs :
     - `prediction_code`
     - `inference_time_ms`
     - `model_version`
     - `timestamp`

3. **Mettre à jour les tests**
   - Les schémas ont changé.
   - Les réponses API sont enrichies.

4. **Reconfigurer MLflow**
   - Utiliser le Model Registry.
   - Définir un modèle Production.

5. **Nettoyer les dépendances**
   - Supprimer SQLite du projet.

---

## 🟨 Deprecated — Dépréciations

- Ancien format de réponse API (label seul).
- Utilisation directe de `mlflow.pyfunc.load_model` sans Registry.
- Ancienne architecture API (main.py + mlflow_loader + SQLite).

---

## 🔐 Security — Améliorations de sécurité

- Validation stricte Pydantic v2 (prévention des payloads invalides).
- Gestion améliorée des erreurs 401 / 422 / 500.
- Sécurisation renforcée via header `x-token`.

---

## 🚀 Performance — Optimisations

- Mapping métier chargé en mémoire (plus rapide que SQLite).
- Temps d’inférence mesuré et exposé dans l’API.
- Chargement modèle plus rapide via Model Registry.

---

## 🛠️ Developer Experience — DX améliorée

- Architecture simplifiée et plus lisible.
- Tests unitaires, intégration et E2E facilitant le développement.
- Documentation interne améliorée (README, rapport, schémas).
- Code plus propre, plus typé, plus maintenable.

---

## 🐞 Known Issues — Limitations connues

- Le modèle LinearSVC ne fournit pas de probabilités (`confidence = null`).
- Pas encore de Dockerfile officiel.
- Pas encore de pipeline CI/CD automatisé.
- Pas encore d’endpoints `/health` ou `/model-info`.

---

## 🔮 Future Work — Évolutions prévues

- Dockerisation de l’API.
- CI/CD GitHub Actions.
- Monitoring API et modèle.
- Endpoints `/health` et `/model-info`.
- Orchestration (Airflow / Prefect).
- Monitoring de dérive.
- Dashboard Streamlit / Gradio.

---

## [1.0.0] - 2026-04-10
### 🎯 Première version stable
- API FastAPI fonctionnelle.
- Sécurité via x-token.
- Mapping métier via SQLite.
- MLflow Tracking basique.
- Tests unitaires API (9 PASS).
- Architecture modulaire.
- Release officielle v1.0.0.

---

## 📌 Format du fichier
Ce changelog suit les principes :
- **Keep a Changelog** : https://keepachangelog.com
- **Semantic Versioning** : https://semver.org
