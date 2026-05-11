# Onboarding — Pipeline MLOps Rakuten

> Guide pas-à-pas pour cloner le repo, comprendre l'architecture et tester
> le cycle MLOps complet en local via Docker.
>
> Public visé : développeur·euse qui découvre le projet et veut le faire
> tourner sur sa machine en moins de 30 minutes.

---

## 1. Pré-requis

| Outil | Version min | Vérifier |
|---|---|---|
| Docker Desktop | 24+ | `docker --version` |
| Docker Compose | v2+ (intégré à Docker Desktop) | `docker compose version` |
| Git | n'importe | `git --version` |
| Mémoire RAM | 8 Go libres recommandés | — |
| Disque | 5 Go libres (images + volume MLflow) | — |

Ports utilisés en local (doivent être libres) :
- `8000` : API FastAPI
- `8081` : MLflow UI
- `8082` : Airflow UI

Si un port est occupé, on peut le surcharger via `.env` (voir étape 4).

---

## 2. Cloner le projet

```bash
git clone <URL_DU_REPO> rakutenmlops_claude
cd rakutenmlops_claude
```

> Sur Windows : si tu utilises PowerShell, toutes les commandes
> `docker compose ...` marchent telles quelles. Les commandes `curl`
> doivent être préfixées par `curl.exe` pour éviter l'alias PowerShell.

---

## 3. Comprendre l'architecture en 30 secondes

3 conteneurs Docker tournent sur un réseau interne `mlops-net` :

```
┌──────────────────────────────────────────────────────────────┐
│ Airflow (orchestrateur)                                      │
│   DAG rakuten_ml_pipeline = 5 tâches :                       │
│   load → preprocess → train → evaluate_model → register_model│
└─────────────────┬────────────────────────────────────────────┘
                  │ envoie params/metrics/modèle
                  ▼
┌──────────────────────────────────────────────────────────────┐
│ MLflow (tracking + Model Registry)                           │
│   Stocke les runs, métriques, artefacts                      │
│   Gère les versions de modèle + alias (production, staging)  │
└─────────────────┬────────────────────────────────────────────┘
                  │ sert le modèle @production
                  ▼
┌──────────────────────────────────────────────────────────────┐
│ FastAPI (serving)                                            │
│   POST /predict                                              │
│   Charge models:/rakuten_classifier@production et prédit     │
└──────────────────────────────────────────────────────────────┘
```

Le pipeline scikit-learn (TF-IDF + LinearSVC) est défini une seule fois
dans `src/models/pipeline.py` et réutilisé par :
- le DAG Airflow (`dags/rakuten_ml_pipeline.py`)
- le script CLI d'entraînement (`src/models/train.py`)

**Séparation stricte des responsabilités** : Airflow entraîne, MLflow stocke,
l'API sert. Aucun service ne fait le travail d'un autre.

---

## 4. Configurer les variables d'environnement

Copier le template :

```powershell
copy .env.example .env
```

ou sur Linux/Mac :

```bash
cp .env.example .env
```

Le fichier `.env` contient les ports et l'URI MLflow. Valeurs par défaut OK
pour 99% des cas. À modifier seulement si :
- un port est déjà pris (changer `MLFLOW_HOST_PORT`, `AIRFLOW_HOST_PORT`,
  `API_HOST_PORT`).
- on veut pointer une instance MLflow distante (non-recommandé en local).

---

## 5. Construire et lancer la stack

```powershell
docker compose build      # construit les 3 images (5-10 min la 1re fois)
docker compose up -d      # démarre les 3 conteneurs en arrière-plan
```

Vérifier que tout est UP :

```powershell
docker compose ps
```

Sortie attendue :

```
NAME            STATUS                    PORTS
mlflow-server   Up                        0.0.0.0:8081 → 8080
airflow         Up                        0.0.0.0:8082 → 8080
api-server      Up (healthy)              0.0.0.0:8000 → 8000
```

Note : Airflow met ~30 sec à démarrer la première fois. Si tu vois `Up`
mais que `http://localhost:8082` ne répond pas, attends.

---

## 6. Récupérer le mot de passe Airflow

Le mot de passe admin est régénéré à chaque création du conteneur Airflow.

```powershell
docker exec airflow cat //opt/airflow/standalone_admin_password.txt
```

> Note Windows : le double-slash `//opt/...` est volontaire pour éviter
> que Git Bash transforme le chemin.

Login : `admin`

---

## 7. Premier tour des UIs

| URL | Quoi y voir |
|---|---|
| http://localhost:8082 | Airflow : liste des DAGs, déclenchement manuel, logs |
| http://localhost:8081 | MLflow : experiments, runs, models registry |
| http://localhost:8000/docs | Swagger FastAPI : tester `/predict` interactivement |

Au démarrage, MLflow et Airflow sont vides (pas encore d'entraînement).

---

## 8. Déclencher le pipeline complet

### Option A — via UI Airflow

1. http://localhost:8082 → login admin.
2. Clic sur le DAG `rakuten_ml_pipeline`.
3. Bouton "Trigger DAG" (en haut à droite).
4. Suivre l'avancement via "Graph" ou "Grid" view.

### Option B — via CLI

```powershell
docker exec airflow airflow dags trigger rakuten_ml_pipeline
```

### Suivre l'état

```powershell
docker exec airflow airflow dags list-runs -d rakuten_ml_pipeline | head -5
```

État cible : `state = success` en bas. Durée totale ~5 min en mode `full`.

---

## 9. Vérifier les résultats côté MLflow

1. http://localhost:8081
2. **Experiments** → `rakuten_ml_pipeline` → cliquer sur le run.
   - Onglet Parameters : voir `C`, `mode`, `max_features_word`, etc.
   - Onglet Metrics : `accuracy`, `macro_f1`, `weighted_f1`, `n_test_samples`.
   - Onglet Artifacts : dossier `model/` (MLmodel, model.pkl, code/, requirements.txt).
3. **Models** (menu de gauche) → `rakuten_classifier`.
   - La dernière version a un badge `@production`.

Vérif programmatique :

```powershell
docker exec airflow python -c "
from mlflow.tracking import MlflowClient
c = MlflowClient('http://mlflow:8080')
mv = c.get_model_version_by_alias('rakuten_classifier', 'production')
print(f'name=rakuten_classifier v{mv.version} status={mv.status}')
print(f'run_id={mv.run_id}')
"
```

---

## 10. Tester l'inférence via l'API

### Option A — via Swagger UI

1. http://localhost:8000/docs
2. Endpoint `POST /predict` → "Try it out".
3. Body :
   ```json
   {
     "designation": "Piscine bestway 3m gonflable",
     "description": "Piscine ronde gonflable de 3 metres pour le jardin"
   }
   ```
4. Header `x-token` : `RAKUTEN_SECRET_123`.
5. Execute → réponse 200 :
   ```json
   {
     "prediction_code": 23,
     "label": "Équipement piscine & spa",
     "run_id": null,
     "confidence": null,
     "inference_time_ms": 12.3,
     "model_version": "Production",
     "timestamp": "..."
   }
   ```

### Option B — via curl

```powershell
curl.exe -X POST http://localhost:8000/predict `
  -H "x-token: RAKUTEN_SECRET_123" `
  -H "Content-Type: application/json" `
  -d '{\"designation\":\"PS5 console Sony\",\"description\":\"Console nouvelle generation 1To SSD\"}'
```

`confidence` est `null` car le modèle (LinearSVC) ne renvoie pas de probabilités.
C'est normal, pas un bug.

---

## 11. Re-trigger après modification

### Scénario : changer un hyperparamètre

1. Éditer `src/config/config.yaml` (ex : `C: 2.5` au lieu de `1`).
2. Rebuild l'image Airflow car `src/` y est copié au build :
   ```powershell
   docker compose build airflow
   docker compose up -d airflow
   ```
3. Re-trigger le DAG (étape 8).
4. Nouveau run dans MLflow, nouvelle version `rakuten_classifier v(N+1)`,
   l'alias `production` bascule automatiquement dessus.

### Scénario : modifier le DAG seulement

`./dags/` est bind-monté, pas besoin de rebuild :

1. Éditer `dags/rakuten_ml_pipeline.py`.
2. Attendre ~30s qu'Airflow rescanne.
3. Re-trigger.

### Cache de l'API

L'API recharge le modèle depuis MLflow à chaque requête `/predict` (lent mais
toujours à jour). Pas besoin de redémarrer l'API après un re-entraînement.

---

## 12. Réinitialisation

### Arrêter sans perdre les données

```powershell
docker compose down
```

Les runs MLflow + le registry sont conservés dans le volume `mlflow-data`.

### Tout réinitialiser (⚠️ destructif)

```powershell
docker compose down -v
docker compose up -d
```

`-v` supprime aussi le volume MLflow → runs et registry repartis de zéro.

---

## 13. Dépannage

| Symptôme | Cause probable | Solution |
|---|---|---|
| `docker compose up` échoue avec "port already in use" | Port 8000/8081/8082 pris | Modifier `.env` (MLFLOW_HOST_PORT, etc.) |
| Airflow UI ne répond pas | Pas encore démarré (1re fois) | Attendre 30-60 sec |
| DAG `rakuten_ml_pipeline` absent | Bug d'import dans le fichier | `docker exec airflow airflow dags list-import-errors` |
| Tâche `train` hang plusieurs minutes | Deadlock fork BLAS | Vérifier que `OMP_NUM_THREADS=1` etc. sont bien dans `docker-compose.yml` |
| `/predict` → `ModuleNotFoundError: src.features` | Image API pas à jour | `docker compose build api && docker compose up -d api` |
| `/predict` → `MLmodel not found` | DAG a logué via `log_artifact` au lieu de `log_model` | Vérifier `dags/rakuten_ml_pipeline.py` utilise bien `mlflow.sklearn.log_model` |
| Le modèle est dans MLflow mais pas d'alias `production` | Tâche `register_model` a échoué | Voir logs : `docker compose logs airflow` puis re-trigger |

Inspecter les logs d'un service :

```powershell
docker compose logs --tail 100 -f airflow
docker compose logs --tail 100 -f mlflow
docker compose logs --tail 100 -f api
```

Inspecter les logs d'une tâche Airflow spécifique : via l'UI Airflow,
clic sur la tâche → "Log".

---

## 14. Aller plus loin

### Entraîner via CLI (sans Airflow)

```powershell
docker exec airflow python -m src.models.train
```

Pratique pour itérer rapidement sans passer par l'UI Airflow. Produit
exactement le même type de run/version dans MLflow.

### Mode `fast` pour itérer rapidement

Éditer `src/config/config.yaml` : `mode: fast` réduit
`max_features_word` à 500, `max_iter` à 500, et entraîne sur un échantillon
de 2000 lignes. Train passe de ~5 min à <30 sec.

### Ajouter une métrique

1. Éditer `dags/rakuten_ml_pipeline.py`, fonction `evaluate_model`.
2. Ajouter dans `mlflow.log_metrics({...})` la nouvelle clé.
3. Re-trigger. Visible dans MLflow UI.

---

## 15. Fichiers de référence

| Fichier | Pour comprendre / modifier |
|---|---|
| `docker-compose.yml` | Orchestration des 3 services, ports, env vars |
| `dags/rakuten_ml_pipeline.py` | Logique d'entraînement orchestrée par Airflow |
| `src/models/pipeline.py` | Définition du modèle scikit-learn (factory) |
| `src/features/text_features.py` | Fonctions d'extraction de features texte |
| `src/config/config.yaml` | Hyperparamètres (mode, C, max_features…) |
| `src/api/app.py` | Routes FastAPI (`/`, `/predict`, …) |
| `src/services/prediction_service.py` | Logique métier de prédiction |
| `src/api/utils.py` | Chargement du modèle depuis MLflow |

---

## TL;DR pour aller vite

```powershell
git clone <repo> && cd rakutenmlops_claude
copy .env.example .env
docker compose up -d --build
docker exec airflow cat //opt/airflow/standalone_admin_password.txt
# → ouvrir http://localhost:8082, login admin, trigger rakuten_ml_pipeline
# → attendre ~5 min que les 5 tâches passent vertes
# → ouvrir http://localhost:8000/docs, tester POST /predict
```
