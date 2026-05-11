# Airflow — guide de test local

Procédure pour lancer Airflow + MLflow ensemble via `docker-compose` et
exécuter le DAG `rakuten_ml_pipeline`.

> Pour tester Airflow **en isolation totale** (sans MLflow), voir la section
> *Annexe — mode standalone seul* en bas de ce document.

---

## Prérequis

- Docker Desktop lancé (baleine verte dans la barre des tâches).
- ≥ 4 Go de RAM alloués à Docker (Settings → Resources).
- Fichier `.env` présent à la racine (copier depuis `.env.example` si besoin).
- Datasets présents :
  - `data/raw/X_train_update.csv`
  - `data/processed/Y_train_encode.csv`

Vérification rapide :

```powershell
docker --version
docker ps
dir .env
dir data\raw\X_train_update.csv
dir data\processed\Y_train_encode.csv
```

---

## 1. Construire l'image Airflow

Depuis la **racine du projet** :

```powershell
docker compose build airflow
```

Long au premier coup (téléchargement image de base + install pip).
Les fois suivantes : quasi instantané (cache Docker).

---

## 2. Démarrer Airflow + MLflow

```powershell
docker compose up -d
```

`-d` = détaché (background). Lance MLflow **et** Airflow sur le réseau
partagé `mlops-net`. Airflow joint MLflow via `http://mlflow:8080`.

Vérifier l'état :

```powershell
docker compose ps
```

Attendre que les deux services soient `Up`.

---

## 3. Récupérer le mot de passe admin Airflow

Le mode `standalone` régénère un mot de passe à chaque démarrage :

```powershell
docker exec airflow cat //opt/airflow/standalone_admin_password.txt
```

> Le double slash `//opt/...` est nécessaire sous Git Bash / MSYS. En CMD
> classique, `/opt/...` suffit.

Aussi visible dans les logs :

```powershell
docker compose logs airflow | Select-String "password"
```

---

## 4. Ouvrir les UIs

| Service     | URL                       | Identifiants                |
|-------------|---------------------------|-----------------------------|
| Airflow     | http://localhost:8082     | `admin` / mdp étape 3        |
| MLflow      | http://localhost:8081     | (pas d'auth)                 |

> Ports configurables via `.env` (`AIRFLOW_HOST_PORT`, `MLFLOW_HOST_PORT`).

---

## 5. Lancer le DAG

1. Sur http://localhost:8082, repérer le DAG `rakuten_ml_pipeline`.
2. Cliquer sur ▶ **Trigger DAG**.
3. Onglet **Graph** : suivre les 4 tâches
   `load → preprocess → train → evaluate_model`.
4. Cliquer sur une tâche → **Logs** pour voir la sortie.

---

## 6. Vérifier les résultats

### Fichiers générés (volumes bind montés sur l'hôte)

```powershell
dir models\1.3_rakuten_model_final.pkl
dir models\metrics.json
type models\metrics.json
```

### Run MLflow

Sur http://localhost:8081, ouvrir l'expérience correspondante → un run
doit apparaître avec params, métriques et artefacts (cf. section
*Instrumentation MLflow* du DAG).

---

## 7. Arrêter

```powershell
docker compose stop          # arrêt propre, conteneurs conservés
docker compose down          # arrêt + suppression conteneurs (volumes nommés gardés)
docker compose down -v       # ⚠️ + suppression des volumes (artefacts MLflow perdus)
```

---

## Dépannage

| Symptôme                                                          | Cause probable                                                                       | Action                                                                                |
|-------------------------------------------------------------------|--------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| `failed to compute cache key: ... not found`                      | Build context incorrect                                                              | Lancer le build depuis la **racine** du projet.                                       |
| `pywin32==... No matching distribution`                           | Mauvais `requirements.txt` utilisé                                                   | Vérifier que `docker/airflow/Dockerfile` pointe sur `docker/airflow/requirements.txt`.|
| Port `8082` indisponible                                          | Service local déjà sur ce port                                                       | Modifier `AIRFLOW_HOST_PORT` dans `.env`.                                             |
| DAG absent de l'UI                                                | Scheduler n'a pas encore scanné                                                      | Attendre 30 s, ou `docker exec airflow airflow dags list`.                            |
| Tâche `load` échoue                                               | CSV manquant dans `data/`                                                            | Voir section *Prérequis*.                                                             |
| Conteneur OOM-killed                                              | RAM Docker insuffisante (LinearSVC + TF-IDF)                                         | Settings Docker Desktop → augmenter à 6–8 Go.                                         |
| `Broken DAG: ImportError: numpy.core.multiarray failed to import` | `pyarrow` d'Airflow compilé contre numpy 1.x, mais `pandas` récent tire numpy 2.x    | Garder `numpy==1.26.4` épinglé dans `docker/airflow/requirements.txt`.                |
| Airflow ne contacte pas MLflow                                    | URL ou réseau incorrects                                                             | Vérifier `MLFLOW_TRACKING_URI=http://mlflow:8080` dans `docker-compose.yml`.          |
| Mot de passe admin perdu après `compose down`                     | DB SQLite Airflow vit dans le conteneur (pas de volume nommé)                        | Normal en dev. Récupérer le nouveau via étape 3.                                      |
| `ImportError: email-validator version >= 2.0 required` au `import mlflow` | mlflow 3.x charge `genai`/`gateway` au top-level → tire fastapi → exige `email-validator` | Garder `email-validator==2.2.0` épinglé dans `docker/airflow/requirements.txt`.        |
| `403 'Invalid Host header'` lors d'un appel MLflow                       | MLflow 3.x bloque les Host headers non listés (anti DNS rebinding)                 | Ajouter le host dans `--allowed-hosts` du Dockerfile MLflow, **avec wildcard pour le port** (ex: `mlflow:*,localhost:*`). |
| `PermissionError: [Errno 13] Permission denied: '/mlflow'` au `log_artifact` | MLflow renvoie une URI artefact en chemin local au lieu de `mlflow-artifacts:/`  | Utiliser `--artifacts-destination` (pas `--default-artifact-root`) dans `docker/mlflow/Dockerfile`. Si une expérience legacy garde un mauvais `artifact_location`, supprimer le volume `mlflow-data` ou renommer l'expérience. |
| Tâche `train` qui hang plusieurs dizaines de minutes puis OOM-killed     | Deadlock fork sklearn / BLAS dans SequentialExecutor                                | Variables d'env dans le service Airflow du compose : `OMP_NUM_THREADS=1`, `OPENBLAS_NUM_THREADS=1`, `MKL_NUM_THREADS=1`. |

---

## Tester la connectivité Airflow → MLflow

```powershell
docker exec airflow curl -sf http://mlflow:8080/health
```

Attendu : `OK`.

---

## Annexe — mode standalone seul (sans MLflow)

Pour itérer sur le DAG sans MLflow en parallèle :

```powershell
docker build -f docker/airflow/Dockerfile -t airflow-rakuten .

docker run -it --rm -p 8080:8080 `
  -v ${PWD}/dags:/opt/airflow/dags `
  -v ${PWD}/data:/opt/airflow/data `
  -v ${PWD}/models:/opt/airflow/models `
  --name airflow-test `
  airflow-rakuten airflow standalone
```

UI sur http://localhost:8080. `Ctrl+C` pour arrêter (`--rm` supprime auto).
