# Onboarding — Pipeline MLOps Rakuten

> Guide pas-à-pas pour cloner le repo, comprendre l'architecture et faire
> tourner le cycle MLOps complet en local via Docker.
>
> Public visé : développeur·euse qui découvre le projet et veut, en moins
> de 30 minutes, **déclencher le DAG → obtenir un modèle promu en
> `@production` → tester l'API qui sert ce modèle**.
>
> Suivre les sections dans l'ordre. Chaque commande est donnée pour
> PowerShell (Windows) ; elle marche aussi sur Linux/Mac sauf mention.

---

## 1. Pré-requis

| Outil | Version min | Vérifier |
|---|---|---|
| Docker Desktop | 24+ | `docker --version` |
| Docker Compose | v2+ (intégré à Docker Desktop) | `docker compose version` |
| Git | n'importe | `git --version` |

### Mémoire à allouer à Docker (IMPORTANT)

Les 3 conteneurs ont des **limites mémoire** (garde-fou). Par défaut elles
totalisent **7 Go** (airflow 4G + mlflow 2G + api 1G). Docker Desktop doit
donc disposer d'au moins **~8 Go**.

Vérifier le budget mémoire de Docker :

```powershell
docker info --format '{{.MemTotal}}'
```

(résultat en octets ; diviser par 1024³ pour des Go — ex. `8160437760` ≈ 7.6 Go)

- **PC costaud** (32 Go RAM) : tu peux monter les limites (voir étape 4) pour
  accélérer l'entraînement.
- **PC modeste** (Docker < 8 Go) : augmente l'allocation Docker Desktop
  (Settings → Resources → Memory). Ne pas descendre les limites sous les
  défauts, sinon l'entraînement est tué (OOM — voir Dépannage §14).

### Ports utilisés (doivent être libres)

- `8000` : API FastAPI
- `8081` : MLflow UI
- `8082` : Airflow UI

Si un port est occupé, le surcharger via `.env` (étape 4).

---

## 2. Cloner le projet

```bash
git clone <URL_DU_REPO> rakutenmlops_claude
cd rakutenmlops_claude
```

> Windows / PowerShell : les commandes `docker compose ...` marchent telles
> quelles. Les commandes `curl` doivent être préfixées par `curl.exe` pour
> éviter l'alias PowerShell.

---

## 3. Comprendre l'architecture en 30 secondes

3 conteneurs Docker sur un réseau interne `mlops-net` :

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
│   Stocke runs, métriques, artefacts                          │
│   Gère versions de modèle + alias (production, staging)      │
└─────────────────┬────────────────────────────────────────────┘
                  │ sert le modèle @production
                  ▼
┌──────────────────────────────────────────────────────────────┐
│ FastAPI (serving)                                            │
│   POST /predict                                              │
│   Charge models:/rakuten_classifier@production (mis en cache)│
└──────────────────────────────────────────────────────────────┘
```

Le pipeline scikit-learn (TF-IDF + LinearSVC) est défini une seule fois
dans `src/models/pipeline.py` et réutilisé par :
- le DAG Airflow (`dags/rakuten_ml_pipeline.py`)
- le script CLI d'entraînement (`src/models/train.py`)

**Séparation stricte des responsabilités** : Airflow entraîne, MLflow stocke,
l'API sert. Aucun service ne fait le travail d'un autre.

Détails à connaître (à jour) :
- Le DAG **ne sauvegarde pas le modèle en pickle local** : il le loggue dans
  MLflow (flavor sklearn). `evaluate_model` **recharge le modèle depuis
  MLflow** (`runs:/{run_id}/model`), pas depuis un fichier.
- L'API **garde le modèle en cache mémoire** et le **précharge au démarrage**
  (1ʳᵉ prédiction quasi instantanée). Conséquence importante : après un
  nouvel entraînement, **il faut redémarrer l'API** pour qu'elle serve la
  nouvelle version (voir §10).

---

## 4. Configurer les variables d'environnement

Copier le template :

```powershell
copy .env.example .env
```

Linux/Mac :

```bash
cp .env.example .env
```

Le fichier `.env` (non versionné) contient :

- **Ports hôtes** (`MLFLOW_HOST_PORT`, `API_HOST_PORT`, `AIRFLOW_HOST_PORT`) —
  changer seulement en cas de conflit de port.
- **URI MLflow** (`MLFLOW_TRACKING_URI`) — défaut OK.
- **Limites mémoire des conteneurs** (`AIRFLOW_MEM`, `MLFLOW_MEM`, `API_MEM`) —
  adapter à ton PC.

### Régler les limites mémoire selon ta machine

Défauts (testés OK sur Docker ~8 Go) :

```
AIRFLOW_MEM=4G
MLFLOW_MEM=2G
API_MEM=1G
```

- **PC costaud** : monter pour accélérer, ex. `AIRFLOW_MEM=12G`, `MLFLOW_MEM=4G`.
  Mettre une valeur ≈ RAM de la machine revient à "illimité".
- **⚠️ Ne JAMAIS descendre `AIRFLOW_MEM` sous 4G ni `MLFLOW_MEM` sous 2G** :
  l'entraînement du DAG serait tué par OOM (constaté). Voir §14.

Vérifier la résolution finale des limites (avant de lancer) :

```powershell
docker compose config | findstr memory
```

---

## 5. Construire et lancer la stack

```powershell
docker compose up -d --build      # build des 3 images (5-10 min la 1re fois) + démarrage
```

Vérifier que tout est UP :

```powershell
docker compose ps
```

Sortie attendue (noms = `<projet>-<service>-1`) :

```
NAME                            STATUS                   PORTS
rakutenmlops_claude-mlflow-1    Up                       0.0.0.0:8081->8080
rakutenmlops_claude-airflow-1   Up                       0.0.0.0:8082->8080
rakutenmlops_claude-api-1       Up (healthy)             0.0.0.0:8000->8000
```

> Le service `api` peut rester `health: starting` ~30-60 s au 1ᵉʳ démarrage :
> il **précharge le modèle `@production`** depuis MLflow. S'il n'y a pas encore
> de modèle (jamais entraîné), le préchargement échoue silencieusement (best
> effort) et l'API démarre quand même.

Vérifier que les limites mémoire sont bien appliquées :

```powershell
docker stats --no-stream --format "table {{.Name}}\t{{.MemUsage}}"
```

(la colonne LIMIT doit afficher 4GiB / 2GiB / 1GiB, ou tes valeurs `.env`)

---

## 6. Récupérer le mot de passe Airflow

Régénéré à chaque (re)création du conteneur Airflow.

```powershell
docker compose exec airflow cat //opt/airflow/standalone_admin_password.txt
```

> Note Windows/Git Bash : le double-slash `//opt/...` évite la réécriture
> automatique du chemin.

Login : `admin`

---

## 7. Premier tour des UIs

| URL | Quoi y voir |
|---|---|
| http://localhost:8082 | Airflow : liste des DAGs, déclenchement manuel, logs |
| http://localhost:8081 | MLflow : experiments, runs, models registry |
| http://localhost:8000/docs | Swagger FastAPI : tester `/predict` |

Au démarrage, MLflow et Airflow sont vides (pas encore d'entraînement).

---

## 8. Déclencher le pipeline complet

### Option A — via UI Airflow

1. http://localhost:8082 → login `admin`.
2. Activer (toggle) puis cliquer le DAG `rakuten_ml_pipeline`.
3. Bouton "Trigger DAG" (en haut à droite).
4. Suivre via "Graph" ou "Grid".

### Option B — via CLI

```powershell
docker compose exec airflow airflow dags unpause rakuten_ml_pipeline
docker compose exec airflow airflow dags trigger rakuten_ml_pipeline
```

### Suivre l'état

```powershell
docker compose exec airflow airflow dags list-runs -d rakuten_ml_pipeline
```

État cible : **les 5 tâches en `success`**. Durée ~8 min en mode `full`.

Voir le détail tâche par tâche du dernier run :

```powershell
docker compose exec airflow airflow tasks states-for-dag-run rakuten_ml_pipeline <run_id>
```

(`<run_id>` = colonne `run_id` de la commande précédente, ex.
`manual__2026-06-08T17:32:31+00:00`)

---

## 9. Vérifier que le modèle est promu en `@production`

1. http://localhost:8081
2. **Experiments** → `rakuten_classification` → cliquer le run.
   - Parameters : `C`, `mode`, `max_features_word`, etc.
   - Metrics : `accuracy` (~0.84), `macro_f1`, `weighted_f1`, `n_test_samples`.
   - Artifacts : dossier `model/` (MLmodel, model.pkl, code/, requirements.txt).
3. **Models** (menu de gauche) → `rakuten_classifier` → la dernière version
   porte l'alias `@production` (posé automatiquement par la tâche
   `register_model`).

Vérif programmatique (note bien le numéro de version + run_id) :

```powershell
docker compose exec airflow python -c "from mlflow.tracking import MlflowClient; c=MlflowClient('http://mlflow:8080'); mv=c.get_model_version_by_alias('rakuten_classifier','production'); print(f'v{mv.version} status={mv.status} run_id={mv.run_id}')"
```

Sortie attendue, ex. : `v5 status=READY run_id=af31cfc8...`

---

## 10. Tester l'API avec le modèle issu de CE cycle DAG

> ⚠️ **Étape clé.** L'API garde le modèle `@production` en **cache mémoire**
> (chargé au démarrage). Si tu viens de (re)lancer le DAG, une **nouvelle
> version** a été promue, mais l'API sert encore l'ancienne tant qu'elle n'a
> pas été redémarrée.

### 10.1 Recharger le modèle frais dans l'API

```powershell
docker compose restart api
```

Au redémarrage, l'API précharge la version `@production` courante (celle que
ton DAG vient de promouvoir). Attendre qu'elle soit `healthy` :

```powershell
docker compose ps api
```

### 10.2 Tester `/predict`

**Option A — Swagger UI** : http://localhost:8000/docs → `POST /predict` →
"Try it out". Header `x-token` = `RAKUTEN_SECRET_123`. Body :

```json
{
  "designation": "Piscine bestway 3m gonflable",
  "description": "Piscine ronde gonflable de 3 metres pour le jardin"
}
```

**Option B — curl** :

```powershell
curl.exe -X POST http://localhost:8000/predict `
  -H "x-token: RAKUTEN_SECRET_123" `
  -H "Content-Type: application/json" `
  -d '{\"designation\":\"PS5 console Sony\",\"description\":\"Console nouvelle generation 1To SSD\"}'
```

Réponse 200 attendue :

```json
{
  "prediction_code": 3,
  "label": "Consoles rétro",
  "run_id": null,
  "confidence": null,
  "inference_time_ms": 12.3,
  "model_version": "Production",
  "timestamp": "..."
}
```

Notes :
- `inference_time_ms` bas (~10-15 ms) et stable car le modèle est **caché**
  (pas de rechargement par requête).
- `confidence` est `null` : LinearSVC ne renvoie pas de probabilités. Normal.

---

## 11. Lancer les tests automatisés (optionnel)

Suite de tests : `tests/test_api_unit.py`, `test_api_integration.py`,
`test_api_e2e.py` (11 tests). Ils s'exécutent dans le conteneur `api`
(qui a tout le stack ML) ; `pytest` n'est pas inclus dans l'image, donc on
copie les tests et on installe `pytest` à la volée :

```powershell
docker compose cp tests api:/app/tests
docker compose cp pytest.ini api:/app/pytest.ini
docker compose exec api pip install -q pytest httpx
docker compose exec api bash -lc "cd /app && python -m pytest -q"
```

Attendu : `11 passed`.

> Les tests d'intégration utilisent le MLflow du réseau Docker ; lance-les
> après avoir au moins un modèle `@production` (étape 8).

---

## 12. Re-trigger après modification

### Scénario : changer un hyperparamètre (pas-à-pas complet)

But : modifier un hyperparamètre, ré-entraîner, et servir le nouveau modèle.

**Pourquoi pouvoir changer les hyperparamètres ?**

Une review technique du projet (voir `commentaires 08 06 2026.md`) a montré que
le pipeline était **trop lourd pour une machine 4 CPU** : les TF-IDF char en
`ngram_range=(3,6)` sans `max_features` font exploser le nombre de colonnes
(des centaines de milliers), la RAM et le temps d'entraînement ; et
`max_iter=20000` brûle du CPU alors que le modèle converge bien avant.

Ces réglages ont donc été **sortis du code et mis dans `config.yaml`**
(défauts = comportement historique). Objectif :
- **adapter le coût CPU/RAM à sa machine** sans modifier le code ;
- **mesurer l'impact accuracy** d'un réglage avant de le figer (re-entraîner,
  comparer dans MLflow).

**Exemple concret (alléger pour petite machine).** Le levier le plus rentable
identifié par la review : réduire les char n-grams de la description et borner
les features. Dans `src/config/config.yaml`, section `pipeline.char.description` :

```yaml
pipeline:
  char:
    description:
      ngram_min: 3
      ngram_max: 6          # <- passer à 4 : gain RAM énorme, accuracy ~ stable
      min_df: 3
      max_features: null    # <- passer à 10000 : borne l'explosion de features
```

Gros gain CPU/RAM, perte d'accuracy souvent négligeable — mais c'est
justement ce qu'on **vérifie** en ré-entraînant (étapes ci-dessous) plutôt
que de le supposer.

Le pas-à-pas ci-dessous utilise un exemple plus simple (`C`), mais la
procédure est identique quel que soit le paramètre changé.

**Étape 1 — Éditer `src/config/config.yaml`.**

Exemple : augmenter la régularisation `C` de `1` à `2`. Ouvre le fichier et
change la ligne :

```yaml
model:
  C: 1            # <- remplacer par : C: 2
```

> Autres leviers possibles dans ce fichier : `mode` (`fast`/`full`),
> `model.max_features_word_*`, et la section `pipeline:` (toggles de features,
> n-grammes char, `min_df`, `max_features`). Tout est paramétrable **sans
> toucher au code**.

**Étape 2 — Rien à faire ici. Aucun rebuild.**

`src/` (donc `config.yaml`) est bind-monté dans Airflow
(`./src:/opt/airflow/src` dans `docker-compose.yml`). La tâche `train` relit
le fichier à chaque exécution → ton changement est **pris en compte au
prochain trigger**, sans rebuild ni redémarrage d'Airflow. Passe directement
à l'étape 3.

> (Le « `src/` copié dans l'image au build » ne concerne QUE l'image de l'API
> pour le serving ; ça n'intervient pas dans le ré-entraînement par le DAG.)

**Étape 3 — Re-trigger le DAG.**

```powershell
docker compose exec airflow airflow dags trigger rakuten_ml_pipeline
```

**Étape 4 — Attendre la fin (~8 min en `full`) et vérifier les 5 tâches.**

```powershell
docker compose exec airflow airflow dags list-runs -d rakuten_ml_pipeline
```

Récupère le `run_id` de la dernière ligne, puis :

```powershell
docker compose exec airflow airflow tasks states-for-dag-run rakuten_ml_pipeline <run_id>
```

Cible : les 5 tâches en `success`. Une **nouvelle version**
`rakuten_classifier v(N+1)` est créée et l'alias `@production` bascule
automatiquement dessus.

**Étape 5 — Vérifier la nouvelle version promue.**

```powershell
docker compose exec airflow python -c "from mlflow.tracking import MlflowClient; c=MlflowClient('http://mlflow:8080'); mv=c.get_model_version_by_alias('rakuten_classifier','production'); print(f'v{mv.version} status={mv.status}')"
```

Le numéro de version doit avoir augmenté de 1.

**Étape 6 — Recharger le modèle dans l'API et tester.**

```powershell
docker compose restart api
```

Puis tester `/predict` comme au §10.2. L'API sert maintenant le modèle
ré-entraîné avec ton nouvel hyperparamètre.

### Scénario : modifier le DAG seulement

`./dags/` est bind-monté → pas de rebuild :

1. Éditer `dags/rakuten_ml_pipeline.py`.
2. Attendre ~30 s qu'Airflow rescanne.
3. Re-trigger.

### Comportement du cache API (à retenir)

- Le modèle `@production` est chargé **une fois** (au démarrage) puis réutilisé.
- Un modèle ciblé par `run_id` (champ `run_id` dans la requête) est aussi caché.
- **Après un ré-entraînement, l'API ne voit pas la nouvelle version tant
  qu'on ne l'a pas redémarrée** (`docker compose restart api`). Il n'y a pas
  d'endpoint `/reload` ; la fonction `clear_model_cache()` n'est utilisée que
  par les tests.

---

## 13. Réinitialisation

### Arrêter sans perdre les données

```powershell
docker compose down
```

Runs MLflow + registry conservés dans le volume `mlflow-data`.

### Tout réinitialiser (⚠️ destructif)

```powershell
docker compose down -v
docker compose up -d --build
```

`-v` supprime le volume MLflow → runs et registry repartis de zéro.

---

## 14. Dépannage

| Symptôme | Cause probable | Solution |
|---|---|---|
| `docker compose up` → "port already in use" | Port 8000/8081/8082 pris | Modifier `.env` (`*_HOST_PORT`) |
| Airflow UI ne répond pas | Pas encore démarré (1re fois) | Attendre 30-60 s |
| DAG `rakuten_ml_pipeline` absent | Bug d'import du fichier | `docker compose exec airflow airflow dags list-import-errors` |
| **Tâche `train` échoue ~1-2 min, log `return code -9`** | **OOM-kill (SIGKILL) : `AIRFLOW_MEM` trop bas** | **Augmenter `AIRFLOW_MEM` dans `.env` (≥4G), `docker compose up -d airflow`** |
| **`train` échoue à `log_model` : `Connection reset by peer` vers mlflow** | **OOM du serveur MLflow : `MLFLOW_MEM` trop bas** | **Augmenter `MLFLOW_MEM` dans `.env` (≥2G), `docker compose up -d mlflow`** |
| Tâche `train` hang plusieurs minutes (sans OOM) | Deadlock fork BLAS | Vérifier `OMP_NUM_THREADS=1` etc. dans `docker-compose.yml` |
| **`/predict` renvoie un ancien modèle après ré-entraînement** | **Cache API non rafraîchi** | **`docker compose restart api`** |
| `/predict` → `ModuleNotFoundError: src.features` | Image API pas à jour | `docker compose build api && docker compose up -d api` |
| `/predict` → `MLmodel not found` / 500 au chargement | Aucun modèle `@production`, ou DAG jamais lancé | Lancer le DAG (§8) puis `docker compose restart api` |
| Modèle dans MLflow mais pas d'alias `@production` | Tâche `register_model` a échoué | `docker compose logs airflow` puis re-trigger |

Vérifier si un conteneur a été OOM-killed :

```powershell
docker inspect rakutenmlops_claude-airflow-1 --format "OOMKilled={{.State.OOMKilled}}"
docker inspect rakutenmlops_claude-mlflow-1 --format "OOMKilled={{.State.OOMKilled}}"
```

Inspecter les logs d'un service :

```powershell
docker compose logs --tail 100 -f airflow
docker compose logs --tail 100 -f mlflow
docker compose logs --tail 100 -f api
```

Logs d'une tâche Airflow précise : via l'UI Airflow, clic sur la tâche → "Log".

---

## 15. Problèmes rencontrés & leçons

Historique des problèmes réels rencontrés sur le projet et comment ils ont
été résolus. Utile pour comprendre certains choix d'architecture.

### 15.1 Problèmes de mémoire (OOM)

Les limites mémoire Docker (vague d'optimisation) ont d'abord été fixées trop
bas et ont **cassé l'entraînement** :

| Limite trop basse | Symptôme observé | Conséquence |
|---|---|---|
| `airflow` à 2G | Tâche `train` tuée à ~80 s, log `return code -9` (SIGKILL) | Pipeline KO |
| `mlflow` à 1G | `log_model` échoue : `Connection reset by peer` (serveur MLflow OOM en recevant l'artefact modèle) | Pipeline KO |

**Cause** : l'entraînement (TF-IDF sur tout le dataset + LinearSVC) a un pic
mémoire élevé, et l'upload de l'artefact modèle fait monter la RAM du serveur
MLflow.

**Solution** :
- Limites right-sizées : `AIRFLOW_MEM=4G`, `MLFLOW_MEM=2G`, `API_MEM=1G`
  (total 7G, tient sur un Docker ~8G).
- Limites rendues **paramétrables via `.env`** (chacun ajuste selon son PC,
  sans modifier le code versionné). Voir §4.
- Garde-fou documenté : ne jamais descendre `AIRFLOW_MEM` < 4G ni
  `MLFLOW_MEM` < 2G.

Diagnostic d'un OOM : `docker inspect <conteneur> --format "{{.State.OOMKilled}}"`.

### 15.2 Factorisation : URL MLflow dupliquée

**Problème** : l'URL du serveur MLflow était réécrite en dur à plusieurs
endroits (API, train, evaluate, scripts). Chaque changement d'URL ou de port
obligeait à modifier plusieurs fichiers → source d'erreurs et d'incohérences.

**Solution** : une **seule source de vérité**, le module
`src/utils/mlflow_config.py` :

```python
from src.utils.mlflow_config import get_tracking_uri
mlflow.set_tracking_uri(get_tracking_uri())
```

- `get_tracking_uri()` lit `MLFLOW_TRACKING_URI` depuis l'environnement
  (`.env` en local, `environment:` du compose en conteneur), avec fallback
  `http://localhost:8081`.
- Plus aucune URL MLflow en dur dans le code. Pour changer d'URI : un seul
  endroit, le `.env`.

Même logique de factorisation pour le **chargement du modèle** : centralisé
dans `src/api/utils.py` (`load_model_from_registry` / `load_model_from_run`)
avec cache mémoire partagé, au lieu d'être recodé à chaque appel.

### 15.3 MLflow : "Invalid Host header - possible DNS rebinding attack"

**Problème** : ouvrir http://localhost:8081 affichait
`Invalid Host header - possible DNS rebinding attack detected`.

**Cause** : MLflow 3.x valide le header HTTP `Host` contre une liste blanche
(`--allowed-hosts`). Le navigateur envoie `localhost:8081` (port hôte mappé),
qui n'était pas dans la liste (elle ne contenait que `localhost` sans port et
`mlflow:8080`).

**Solution** : ajouter le couple host:port mappé dans les **deux** sources de
config du service mlflow (`docker-compose.yml`) :
- env `MLFLOW_SERVER_ALLOWED_HOSTS=...,localhost:8081,127.0.0.1:8081`
- flag `--allowed-hosts ...,localhost:8081,127.0.0.1:8081`

Puis `docker compose up -d mlflow`. Si tu changes `MLFLOW_HOST_PORT`, pense à
ajouter le nouveau `localhost:<port>` à ces listes.

> Rappel : ce même mécanisme `--allowed-hosts` règle aussi les `403 Invalid
> Host header` sur les appels internes (host `mlflow:8080`).

---

## 16. Aller plus loin

### Entraîner via CLI (sans Airflow)

```powershell
docker compose exec airflow python -m src.models.train
```

Pratique pour itérer sans l'UI. Produit le même type de run/version dans MLflow.

### Mode `fast` pour itérer rapidement

Dans `src/config/config.yaml` : `mode: fast` réduit `max_features_word_fast`,
`max_iter_fast` et entraîne sur un échantillon (`sample_size_fast: 2000`).
Train passe de ~8 min à <1 min.

### Mesurer l'impact d'une feature

Dans `config.yaml`, section `pipeline.features`, passer un bloc à `false`
(ex. `description_char: false`), re-trigger, comparer l'`accuracy` dans MLflow.

---

## 17. Fichiers de référence

| Fichier | Pour comprendre / modifier |
|---|---|
| `docker-compose.yml` | Orchestration des 3 services, ports, env vars, limites mémoire |
| `.env.example` | Template `.env` (ports, URI MLflow, limites mémoire) |
| `dags/rakuten_ml_pipeline.py` | Logique d'entraînement orchestrée par Airflow |
| `src/models/pipeline.py` | Définition du modèle scikit-learn (factory) |
| `src/features/text_features.py` | Fonctions d'extraction de features texte |
| `src/config/config.yaml` | Hyperparamètres + section `pipeline:` paramétrable |
| `src/api/app.py` | Routes FastAPI + préchargement modèle au démarrage |
| `src/api/utils.py` | Chargement + **cache mémoire** du modèle MLflow |
| `src/services/prediction_service.py` | Logique métier de prédiction |

---

## TL;DR pour aller vite

```powershell
git clone <repo> && cd rakutenmlops_claude
copy .env.example .env                 # ajuster *_MEM selon ton PC
docker compose up -d --build
docker compose exec airflow cat //opt/airflow/standalone_admin_password.txt
# → http://localhost:8082, login admin, trigger rakuten_ml_pipeline
# → attendre les 5 tâches vertes (~8 min)
docker compose exec airflow python -c "from mlflow.tracking import MlflowClient; c=MlflowClient('http://mlflow:8080'); mv=c.get_model_version_by_alias('rakuten_classifier','production'); print('v'+str(mv.version), mv.status)"
docker compose restart api             # l'API sert le modèle du cycle DAG
# → http://localhost:8000/docs, tester POST /predict (x-token: RAKUTEN_SECRET_123)
```
