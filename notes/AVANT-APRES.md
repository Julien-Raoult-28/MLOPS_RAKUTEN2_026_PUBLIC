# Rakuten MLOps — Avant / Après

> Document de synthèse de la transformation du projet `rakutenmlops_claude` :
> d'un assemblage de scripts manuels exécutés à la main vers une chaîne MLOps
> conteneurisée et orchestrée. Ce document sert de point d'entrée pour la
> rédaction d'une présentation de soutenance d'école.
>
> Public visé : jury technique ayant un bagage data science / MLOps.

---

## 1. Le projet en une phrase

Classifier automatiquement les produits Rakuten dans **27 catégories** à partir
de leur `designation` (titre court) et `description` (texte libre), via un
modèle **TF-IDF + LinearSVC** entraîné sur ~50 000 produits, exposé par une
**API FastAPI** consommée par un client externe.

Le périmètre fonctionnel n'a **pas changé** entre l'avant et l'après. Ce qui a
changé, c'est **la façon de produire, versionner, et servir le modèle**.

---

## 2. TL;DR — En une slide

| Dimension | AVANT (V1) | APRÈS (V2) |
|---|---|---|
| Exécution | Manuelle, script par script | Orchestrée (Airflow DAG) |
| Environnement | Python local, chemins Windows en dur | 3 conteneurs Docker, paths Linux relatifs |
| Modèle | `joblib.dump` → `.pkl` local | `mlflow.sklearn.log_model` → Model Registry versionné |
| Promotion en production | Manuelle (humain copie un fichier) | Automatique (alias `@production` posé par le DAG) |
| Tracking expériences | MLflow installé en local, base SQLite isolée | MLflow conteneurisé, accessible par tous les services |
| API | `uvicorn` lancé à la main, modèle hardcodé | Conteneur Docker, charge le modèle depuis MLflow |
| Reproductibilité | Dépend du poste développeur | `docker compose up -d --build` sur n'importe quelle machine |
| Traçabilité d'un run | Quasi-nulle (un `.pkl` sans contexte) | Run MLflow complet : params, metrics, artefacts, code, signature |
| Rollback | Récupérer un ancien fichier `.pkl` à la main | `client.set_registered_model_alias(... version=N)` |
| Onboarding nouveau dev | Suivre un README de plusieurs pages, installer Python, MLflow, etc. | `git clone && docker compose up -d` → tout tourne en 10 min |

---

## 3. AVANT — Le pipeline artisanal (V1)

### 3.1. Le cycle de travail réel

Avant la refonte, produire un modèle utilisable par l'API se faisait en **5
étapes manuelles**, chacune lancée par un humain dans un terminal :

```
[1] Développeur ouvre un terminal
        │
        │  python src/train.py --mode full
        ▼
[2] Script entraîne le modèle en local
    Sauvegarde un fichier .pkl sur le disque local
        │
        │  (en parallèle, MLflow local tourne peut-être, peut-être pas)
        ▼
[3] Humain vérifie "à l'œil" que les métriques sont bonnes
    (sortie console, ou un coup d'œil sur MLflow UI s'il a pensé à le lancer)
        │
        ▼
[4] Humain DÉCIDE que ce modèle est "le bon"
    → Copie/renomme le .pkl à un emplacement précis
    → Modifie en dur le chemin du modèle dans le code de l'API
        │
        ▼
[5] Humain (re)lance l'API à la main
    uvicorn src.api.app:app --reload
    L'API tourne sur localhost, sur SA machine, avec SON Python
```

### 3.2. Preuve technique — l'ancienne API

Le fichier `src/api/main_OLD.py` (conservé dans le repo comme témoignage)
illustre parfaitement l'état d'esprit V1 :

```python
mapping_path = r"C:\Users\Mproo\Documents\Cours_DATASCIENTEST\FEV26-CMLOPS-RAKUTEN\data\processed\Y_train_encode.csv"
MODEL_PATH   = r"C:\Users\Mproo\Documents\Cours_DATASCIENTEST\FEV26-CMLOPS-RAKUTEN\models\1.3_rakuten_model_final.pkl"

model = joblib.load(MODEL_PATH)
```

Tout y est :

- **Chemins absolus Windows en dur** dans le code applicatif → impossible à
  déployer ailleurs sans modifier la source.
- **Chargement direct d'un `.pkl`** avec `joblib.load` → aucune notion de
  version, d'artefact, de signature, de modèle "production" vs "staging".
- **Pas de MLflow** dans l'API V1 : le modèle est un fichier sur disque, point.
- **Pas d'authentification**, pas de schéma Pydantic typé, pas de healthcheck.
- **Code mort attendant la prochaine modification manuelle** : pour passer en
  v2 du modèle, il faut éditer cette constante et redéployer.

### 3.3. Topologie V1

```
                 ┌──────────────────────────────────┐
                 │   Machine du développeur          │
                 │                                   │
                 │   Python 3.10 (venv local)        │
                 │   ├── train.py (lancé à la main)  │
                 │   ├── mlflow ui (parfois lancé)   │
                 │   └── uvicorn app:app (à la main) │
                 │                                   │
                 │   /models/1.3_rakuten_model.pkl   │
                 │   (chemin hardcodé dans l'API)    │
                 └──────────────────────────────────┘
```

Une seule machine, trois processus lancés à la main, **un seul artefact**
(le `.pkl`) qui circule par copie/renommage manuel.

### 3.4. Les problèmes structurels du V1

| Problème | Conséquence concrète |
|---|---|
| Pas d'orchestration | Si l'humain oublie une étape (ex : preprocess), le modèle est corrompu sans message d'erreur clair. |
| Pas de versioning modèle | Impossible de répondre à "quel modèle a fait cette prédiction le mois dernier ?". |
| Promotion manuelle | Risque humain : on déploie le mauvais `.pkl` en prod. |
| Tracking optionnel | Les runs MLflow lancés en local sont jetés à chaque `rm -rf mlruns/`. |
| Couplage code ↔ machine | Un nouveau dev doit installer **exactement** la même stack Python. |
| API mono-instance | Pas de healthcheck, pas de redémarrage automatique, pas de scaling. |

---

## 4. APRÈS — La chaîne MLOps industrialisée (V2)

### 4.1. Topologie cible

3 conteneurs Docker tournent sur un réseau interne `mlops-net`, orchestrés
par `docker-compose.yml` à la racine du projet :

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│   ┌────────────────────┐   ┌────────────────────┐                │
│   │  Conteneur          │   │  Conteneur          │               │
│   │  airflow            │   │  mlflow-server      │               │
│   │                     │   │                     │               │
│   │  DAG :              │──▶│  - SQLite (runs)    │               │
│   │  rakuten_ml_pipeline│   │  - Volume artefacts │               │
│   │  5 tâches en série  │   │  - Model Registry   │               │
│   │                     │   │                     │               │
│   │  port 8082 (UI)     │   │  port 8081 (UI)     │               │
│   └────────────────────┘   └─────────┬──────────┘                │
│                                       │                          │
│                                       │ models:/rakuten_classifier│
│                                       │        @production       │
│                                       ▼                          │
│                             ┌────────────────────┐                │
│                             │  Conteneur          │               │
│                             │  api-server         │               │
│                             │                     │               │
│                             │  FastAPI :          │               │
│                             │  POST /predict      │               │
│                             │                     │               │
│                             │  port 8000          │               │
│                             └────────────────────┘                │
│                                                                  │
│              Réseau Docker interne : mlops-net                   │
└──────────────────────────────────────────────────────────────────┘
                              │
                              │ ports exposés vers la machine hôte
                              ▼
                ┌─────────────────────────────────┐
                │ Navigateur / client HTTP         │
                │   localhost:8000/docs  (Swagger) │
                │   localhost:8081       (MLflow)  │
                │   localhost:8082       (Airflow) │
                └─────────────────────────────────┘
```

### 4.2. Séparation stricte des responsabilités

Le principe directeur de l'architecture V2 :
**chaque service fait une seule chose, et ne fait pas le travail des autres.**

| Service | Rôle exclusif | Ne fait JAMAIS |
|---|---|---|
| **Airflow** | Orchestrer l'entraînement (load → preprocess → train → evaluate → register) | Servir des prédictions |
| **MLflow** | Stocker runs, métriques, artefacts, registry, alias | Entraîner ou prédire |
| **FastAPI** | Charger le modèle `@production` et exposer `/predict` | Entraîner ou modifier le modèle |

C'est cette séparation qui rend chaque brique remplaçable individuellement
(ex : changer Airflow pour Prefect sans toucher au reste).

### 4.3. Le DAG `rakuten_ml_pipeline` — cœur de la chaîne

Défini dans `dags/rakuten_ml_pipeline.py`, le DAG Airflow enchaîne 5 tâches :

```
   ┌──────────┐   ┌────────────┐   ┌───────┐   ┌─────────────┐   ┌────────────────┐
   │   load   │──▶│ preprocess │──▶│ train │──▶│ evaluate    │──▶│ register_model │
   │          │   │            │   │       │   │ _model      │   │                │
   └──────────┘   └────────────┘   └───────┘   └─────────────┘   └────────────────┘
        │              │              │              │                  │
   raw CSV   →  CSV nettoyé   →   pipeline   →    accuracy,         alias
   (50k lignes)  (lowercase,    sklearn fit       macro_f1,      @production
                 NaN→"")        + MLflow run      weighted_f1      posé sur la
                                logué avec        loggués          nouvelle version
                                code_paths        dans le run
```

Détail des tâches :

1. **`load`** : lit `data/raw/X_train_update.csv` + `Y_train_encode.csv`,
   joint, échantillonne 50k lignes, écrit `/tmp/rakuten_clean.csv`.
2. **`preprocess`** : remplit les NaN, passe en minuscules, réécrit le CSV.
3. **`train`** :
   - Appelle `build_pipeline(config)` (factory partagée — cf. §4.5).
   - Fait `pipeline.fit(X_train, y_train)`.
   - Ouvre un run MLflow, logge params + tags.
   - Appelle `mlflow.sklearn.log_model(..., registered_model_name="rakuten_classifier", code_paths=["/opt/airflow/src"])`.
   - **Crée automatiquement** une nouvelle version dans le Model Registry.
   - Retourne le `run_id` via Airflow XCom.
4. **`evaluate_model`** : récupère le `run_id` via XCom, calcule
   `accuracy`, `macro_f1`, `weighted_f1`, log dans le même run, plus un
   `metrics.json` en artefact.
5. **`register_model`** : retrouve la version créée par `log_model` et
   pose l'alias `production` dessus via
   `client.set_registered_model_alias(..., alias="production")`.

> Point critique : c'est la **dernière tâche** qui bascule l'alias. Donc tant
> que les 4 tâches précédentes ne sont pas vertes, l'API continue de servir
> l'ancienne version. La promotion en production est **atomique** et conditionnée
> au succès du pipeline complet — exactement ce que ne permettait pas le V1.

### 4.4. MLflow — le hub central

Le conteneur `mlflow-server` (image Python 3.11 + `mlflow==3.11.1`) joue
trois rôles distincts :

1. **Tracking server** : stocke chaque run (paramètres, métriques, tags,
   artefacts) dans une base SQLite (`/mlflow/data/mlflow.db`).
2. **Artifact store** : stocke les fichiers liés à chaque run (modèle
   pickle, classification report, model card, etc.) dans
   `/mlflow/data/mlruns/`. Les clients (Airflow, API) y accèdent via le
   proxy HTTP MLflow grâce au flag `--artifacts-destination` + `--serve-artifacts`.
3. **Model Registry** : maintient un catalogue de **modèles nommés**
   (`rakuten_classifier`) avec leurs **versions** (v1, v2, v3…) et leurs
   **alias** (`@production`, `@staging`).

L'API ne charge **jamais** un fichier `.pkl` directement. Elle interroge
le registry :

```python
# src/api/utils.py
model_uri = "models:/rakuten_classifier@production"
return mlflow.pyfunc.load_model(model_uri)
```

Cette URI est **stable** : peu importe que la version courante en production
soit la v2 ou la v17, l'API la résout dynamiquement à chaque démarrage (ou,
ici, à chaque requête).

### 4.5. Le pipeline sklearn — défini une seule fois

Pour éviter la dérive entre l'entraînement en CLI et l'entraînement via Airflow,
le pipeline scikit-learn est défini dans un **seul endroit** :
`src/models/pipeline.py`, fonction `build_pipeline(config)`.

```
DataFrame[designation, description]
    │
    ▼
ColumnTransformer (6 sources de features en parallèle)
    ├─ TfidfVectorizer mots sur designation
    ├─ TfidfVectorizer caractères sur designation
    ├─ TfidfVectorizer mots sur description
    ├─ TfidfVectorizer caractères sur description
    ├─ TfidfVectorizer sur 3 premiers mots de designation
    └─ TfidfVectorizer sur nombres+unités extraits de designation
    │
    ▼
LinearSVC (C, class_weight=balanced) → int (code catégorie)
```

Cette factory est appelée :
- par le DAG Airflow (`dags/rakuten_ml_pipeline.py`),
- par le script CLI alternatif (`src/models/train.py`).

**Conséquence MLOps** : ce qui tourne en CLI pour itérer rapidement est
*exactement* ce qui sera entraîné par Airflow en mode pipeline. Plus de
divergence "ça marche sur mon poste".

### 4.6. L'API FastAPI — service d'inférence

Conteneur basé sur `python:3.11-slim`, expose deux endpoints :

- `GET /` → healthcheck (utilisé par Docker `HEALTHCHECK`).
- `POST /predict` → prédiction, protégée par header `x-token`.

Réponse enrichie par rapport au V1 :

```json
{
  "prediction_code": 23,
  "label": "Équipement piscine & spa",
  "run_id": null,
  "confidence": null,
  "inference_time_ms": 12.4,
  "model_uuid": "unknown",
  "model_version": "Production",
  "timestamp": "2026-05-22T08:12:45Z"
}
```

**Mode hybride** :
- Si `run_id` est `null` dans la requête → l'API charge le modèle
  `@production` (cas normal d'utilisation).
- Si `run_id` est fourni → l'API charge ce run précis (pour debug,
  comparaison, ou rollback ponctuel sans toucher au registry).

### 4.7. Cycle de re-entraînement V2 — un humain n'écrit rien

```
[Humain] modifie src/config/config.yaml (ex: C: 2.5)
            │
            │  docker compose build airflow && docker compose up -d airflow
            ▼
[Humain] clique "Trigger DAG" dans l'UI Airflow (ou CLI)
            │
            ▼
[Airflow] exécute les 5 tâches en série (~5 min en mode full)
            │
            ▼
[MLflow]  run #N créé, version v(N) du modèle créée,
          alias @production posé sur v(N) AUTOMATIQUEMENT
            │
            ▼
[API]     prochaine requête /predict → charge v(N) sans redémarrage
```

Aucune copie de fichier. Aucun édit de chemin. Aucun redémarrage manuel
d'API. Le seul rôle humain est de **décider** d'entraîner (ou de laisser un
scheduler le faire en cron).

---

## 5. Mapping point par point — Avant ↔ Après

### 5.1. Côté entraînement

| Aspect | AVANT (V1) | APRÈS (V2) |
|---|---|---|
| Commande | `python src/train.py --mode full` lancée à la main | Bouton "Trigger DAG" dans Airflow (ou cron) |
| Définition du modèle | Dans `train.py`, dupliqué partout | `build_pipeline()` factory, source unique |
| Suivi paramètres | Néant ou MLflow optionnel | `mlflow.log_params` systématique |
| Suivi métriques | Print console | `mlflow.log_metrics` (4 métriques + classification report) |
| Sortie modèle | `.pkl` sur disque local | Run MLflow + version registry + signature |
| Test du modèle | À l'œil, sur la console | Tâche `evaluate_model` dédiée, métriques tracées |

### 5.2. Côté serving

| Aspect | AVANT (V1) | APRÈS (V2) |
|---|---|---|
| Lancement API | `uvicorn app:app --reload` à la main | `docker compose up -d api` |
| Chemin du modèle | `r"C:\Users\Mproo\...\1.3_rakuten_model_final.pkl"` en dur | `models:/rakuten_classifier@production` |
| Bibliothèque de chargement | `joblib.load(MODEL_PATH)` | `mlflow.pyfunc.load_model(model_uri)` |
| Authentification | Aucune | Header `x-token` validé |
| Schéma de requête | `BaseModel` Pydantic minimal | Pydantic v2 strict (`PredictionRequest` / `PredictionResponse`) |
| Healthcheck | Aucun | `GET /` + Docker `HEALTHCHECK` |
| Métadonnées réponse | `prediction_encoded`, `label`, `input` | + `inference_time_ms`, `model_version`, `timestamp`, `run_id`, `confidence` |
| Promotion d'un nouveau modèle | Modifier `MODEL_PATH` dans le code, redémarrer | 0 ligne de code, 0 redémarrage |
| Rollback | Restaurer un ancien `.pkl` à la main | `client.set_registered_model_alias(..., version=N-1)` |

### 5.3. Côté reproductibilité

| Aspect | AVANT (V1) | APRÈS (V2) |
|---|---|---|
| Setup nouveau dev | Installer Python 3.10, venv, dépendances, MLflow local, configurer chemins | `git clone && docker compose up -d --build` |
| Dépendances | `requirements.txt` racine (mélangé Windows / Linux, `pywin32==311`) | 1 `requirements.txt` par service Docker, pins testés |
| OS du runtime | Windows du dev | Linux (Debian slim) reproductible |
| Versions clés | Variables selon poste | Verrouillées : `mlflow==3.11.1`, `airflow==2.8.4-python3.11`, `numpy==1.26.4` |
| Configuration | Constantes hardcodées dans le code | Variables `.env` injectées dans les conteneurs |

### 5.4. Côté observabilité

| Aspect | AVANT (V1) | APRÈS (V2) |
|---|---|---|
| Voir l'historique des runs | `ls mlruns/` à la main, si MLflow local a été lancé | Onglet "Experiments" sur http://localhost:8081 |
| Voir les versions d'un modèle | Aucune notion de version | Onglet "Models" → `rakuten_classifier` → v1, v2, v3… |
| Voir l'état d'un entraînement | Terminal qui scroll | Vue "Graph" / "Grid" sur http://localhost:8082 |
| Voir les logs d'une tâche | Stdout / stderr du shell | UI Airflow → clic sur la tâche → onglet "Log" |
| Mesurer la latence d'inférence | Impossible | Champ `inference_time_ms` dans chaque réponse |

---

## 6. Architecture détaillée des composants

### 6.1. Conteneur `mlflow` (`docker/mlflow/Dockerfile`)

- Base : `python:3.11-slim`.
- Installé : `mlflow==3.11.1`.
- Stockage backend : SQLite (`sqlite:////mlflow/data/mlflow.db`).
- Stockage artefacts : `/mlflow/data/mlruns/`, exposé via `--serve-artifacts`.
- Flag critique : `--allowed-hosts "mlflow:*,localhost:*,localhost"` (MLflow 3
  bloque par défaut les Host headers inconnus — protection anti-DNS-rebinding).
- Volume nommé `mlflow-data` monté sur `/mlflow/data/` → les runs et le registry
  survivent à `docker compose down`.

### 6.2. Conteneur `airflow` (`docker/airflow/Dockerfile`)

- Base : `apache/airflow:2.8.4-python3.11`.
- Mode : `airflow standalone` (scheduler + webserver + SQLite + admin user dans
  un seul conteneur — suffisant pour dev local).
- Installé : `numpy==1.26.4` (pin imposé par pyarrow d'Airflow),
  `scikit-learn`, `mlflow`, `email-validator==2.2.0`, `python-dotenv`.
- Code copié à la build : `dags/`, `src/`, `data/`, `models/`.
- Bind mounts dynamiques : `./dags`, `./data`, `./models` → édition à chaud
  des DAGs sans rebuild.
- Variables d'environnement critiques :
  - `MLFLOW_TRACKING_URI=http://mlflow:8080` (résolution par nom de service Docker).
  - `PYTHONPATH=/opt/airflow` (pour `from src.models.pipeline import ...`).
  - `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1` (évite
    le deadlock fork BLAS dans SequentialExecutor).

### 6.3. Conteneur `api` (`docker/api/Dockerfile`)

- Base : `python:3.11-slim`.
- Installé : `fastapi`, `uvicorn`, `mlflow`, `scikit-learn` (mêmes versions que
  côté entraînement, sinon l'unpickle échoue).
- Code copié : `src/api/`, `src/services/`, `src/utils/`, `src/features/`
  (ce dernier nécessaire au moment de l'unpickle car le pipeline référence
  `src.features.text_features`).
- Healthcheck Docker : `curl -fs http://localhost:8000/`.
- Démarrage : `uvicorn src.api.app:app --host 0.0.0.0 --port 8000`.

### 6.4. `docker-compose.yml` — orchestrateur des 3 services

- Réseau interne `mlops-net` (driver bridge).
- Volume nommé `mlflow-data` partagé entre les services qui en ont besoin.
- Ports exposés vers l'hôte (paramétrables via `.env`) :
  - 8000 → API FastAPI
  - 8081 → MLflow UI
  - 8082 → Airflow UI
- Dépendances : `api` et `airflow` ont `depends_on: mlflow` → MLflow démarre
  en premier.
- `restart: unless-stopped` partout → tolérance aux crashs.

---

## 7. Difficultés MLOps rencontrées et résolues

Cette section liste des bugs concrets traversés pendant la mise en place,
utiles pour démontrer que l'architecture finale n'est pas tombée du ciel.

| # | Symptôme | Cause | Solution |
|---|---|---|---|
| 1 | `pip install` échoue dans Docker | `requirements.txt` racine = freeze Windows avec `pywin32` | Un `requirements.txt` par service, sans deps Windows |
| 2 | `numpy.core.multiarray failed to import` | `pyarrow` d'Airflow compilé contre numpy 1.x, pandas tirait numpy 2.x | Pin `numpy==1.26.4` dans Airflow |
| 3 | `ImportError: email-validator version >= 2.0 required` | MLflow 3 charge `genai/gateway` qui touche EmailStr | Pin `email-validator==2.2.0` |
| 4 | `403 Invalid Host header` côté MLflow | MLflow 3 bloque les Host inconnus | Flag `--allowed-hosts "mlflow:*,localhost:*,localhost"` |
| 5 | `PermissionError: '/mlflow'` au log_artifact | `--default-artifact-root` envoyait un chemin local côté client | Remplacer par `--artifacts-destination` + `--serve-artifacts` |
| 6 | Tâche `train` hang 78 min puis OOM-kill | Deadlock fork sklearn / BLAS dans SequentialExecutor | `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1` |
| 7 | `/predict` ne trouve pas le modèle | Le DAG logguait via `log_artifact(pkl)` = blob opaque | Remplacer par `mlflow.sklearn.log_model(..., registered_model_name=...)` |
| 8 | `ModuleNotFoundError: src.features` côté API | `code_paths=[".../text_features.py"]` aplatit la structure ; image API n'incluait pas `src/features/` | `code_paths=["/opt/airflow/src"]` (directory) + `COPY src/features/` dans Dockerfile API |

Ces 8 incidents racontent à eux seuls la différence entre "scripts qui tournent
sur mon poste" et "chaîne MLOps reproductible". Chacun a forcé à expliciter
une dépendance ou une convention implicite.

---

## 8. Ce qui n'est pas (encore) fait — Limites et travaux futurs

À mentionner par honnêteté technique en soutenance :

- **Pas de CI/CD** : pas de GitHub Actions qui build + push les images, ni
  qui lance les tests à chaque commit.
- **Airflow standalone**, pas multi-conteneurs (pas de Postgres + scheduler +
  webserver + worker séparés). Suffisant en dev, à étendre en prod.
- **Pas de monitoring de dérive** (data drift, concept drift) : pas de
  comparaison entre distribution d'entraînement et flux de production.
- **Pas de cache modèle côté API** : `prediction_service.predict_product`
  recharge le modèle à chaque requête HTTP (lent mais toujours à jour). À
  remplacer par un chargement au démarrage + endpoint `/reload-model`.
- **Pas de probabilités** : LinearSVC ne fournit pas `predict_proba` →
  `confidence` reste `null`. À adresser en passant à un modèle calibré
  (`CalibratedClassifierCV`) ou un modèle bayésien.
- **Pas de déploiement cloud** : tout tourne en local. À porter sur un cluster
  Kubernetes (ou ECS / Cloud Run) pour passer à l'échelle.

---

## 9. Schéma de synthèse — Avant / Après en un seul visuel

```
┌──────────────────────────────────────────────────────────────────────┐
│                              AVANT (V1)                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│   [Humain] ─┬─▶  python train.py                                     │
│             │       │                                                │
│             │       └─▶  models/foo.pkl  ◀── chemin hardcodé         │
│             │                                                        │
│             └─▶  uvicorn app:app                                     │
│                     │                                                │
│                     └─▶  joblib.load("C:\...\foo.pkl")               │
│                                                                      │
│   3 actions humaines pour passer un nouveau modèle en prod           │
│   Aucune traçabilité, aucun rollback                                  │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                              APRÈS (V2)                              │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│                            ┌─────────────┐                           │
│                            │   MLflow    │                           │
│                            │   server    │                           │
│                            │             │                           │
│                            │  runs       │                           │
│                            │  metrics    │                           │
│                            │  artefacts  │                           │
│                            │  registry   │                           │
│                            │  + aliases  │                           │
│                            └──┬───────┬──┘                           │
│         log_model + register  │       │  models:/...@production      │
│                                │       │                              │
│   [Humain]  ──▶  Trigger      │       │       ┌───────────┐          │
│             ┌────────────┐    │       └──────▶│  FastAPI  │          │
│             │  Airflow    │   │               │           │          │
│             │   DAG       │───┘               │  /predict │          │
│             │             │                   └─────┬─────┘          │
│             │  load       │                          │                │
│             │  preprocess │                          ▼                │
│             │  train      │                    [Client HTTP]          │
│             │  evaluate   │                                            │
│             │  register ──┘ (pose alias @production)                  │
│             └────────────┘                                            │
│                                                                      │
│   1 seule action humaine : trigger. Le reste est automatique.        │
│   Versionning complet, rollback en 1 commande, prod atomique.        │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 10. Annexe — Fichiers à citer en soutenance

| Fichier | Pourquoi le montrer |
|---|---|
| `src/api/main_OLD.py` | Preuve concrète du V1 artisanal (chemins Windows hardcodés, `joblib.load`) |
| `src/api/app.py` | API V2 propre, typée, sécurisée |
| `src/api/utils.py` | Comment l'API charge le modèle depuis le registry (`models:/...@production`) |
| `src/services/prediction_service.py` | Couche métier : décodage du code en libellé, mesure latence |
| `dags/rakuten_ml_pipeline.py` | Cœur de la chaîne MLOps : le DAG 5 tâches |
| `src/models/pipeline.py` | Définition unique du pipeline sklearn (factory) |
| `docker-compose.yml` | Orchestration des 3 services et leur réseau interne |
| `docker/mlflow/Dockerfile` | Flags critiques de MLflow 3 (`--allowed-hosts`, `--artifacts-destination`) |
| `docker/airflow/Dockerfile` | Comment Airflow récupère le code projet + ses pinnings |
| `docker/api/Dockerfile` | Healthcheck, `src/features/` inclus pour l'unpickle |
| `changelog.md` | Historique formel V1 → V2 (Keep a Changelog) |
| `ONBOARDING.md` | Démontre que la chaîne est reproductible en < 30 min sur n'importe quelle machine |

---

## 11. Trois messages-clés à retenir pour la soutenance

1. **Le passage V1 → V2 n'est pas un changement de modèle, c'est un
   changement de *processus*.** Le modèle TF-IDF + LinearSVC est le même.
   Ce qui change, c'est qui le produit, comment il est versionné, et
   comment il atteint la production.

2. **La séparation Airflow / MLflow / API est non négociable.** C'est ce
   qui rend chaque brique remplaçable, et chaque étape testable. Sans cette
   séparation, on retombe dans le "script qui fait tout" du V1.

3. **L'industrialisation se mesure au nombre de gestes humains nécessaires
   pour mettre un modèle en prod.** Avant : ~5 gestes manuels + édition de
   code + redémarrage. Après : 1 clic dans Airflow. C'est la définition
   opérationnelle du MLOps.
