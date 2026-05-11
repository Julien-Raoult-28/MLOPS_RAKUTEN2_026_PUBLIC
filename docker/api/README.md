# API FastAPI — guide de test local

Service d'inférence Rakuten. Charge un modèle MLflow et expose `POST /predict`.

---

## Prérequis

- Stack MLflow + Airflow déjà lancée (au moins MLflow).
- Au moins **un modèle disponible** dans MLflow, soit :
  - via un `run_id` (mode RUN),
  - soit enregistré dans le Model Registry sous le nom `rakuten_classifier`
    avec un alias `production` (mode REGISTRY par défaut).

---

## 1. Construire et lancer

Depuis la racine du projet :

```powershell
docker compose build api
docker compose up -d api
```

Vérifier l'état :

```powershell
docker compose ps
docker compose logs -f api
```

Attendre `Uvicorn running on http://0.0.0.0:8000`.

---

## 2. Endpoints disponibles

| Méthode | URL                              | Description                         |
|---------|----------------------------------|-------------------------------------|
| GET     | `http://localhost:8000/`         | Healthcheck (sans auth)             |
| POST    | `http://localhost:8000/predict`  | Prédiction (header `x-token` requis)|
| GET     | `http://localhost:8000/docs`     | Swagger UI                          |
| GET     | `http://localhost:8000/redoc`    | ReDoc                               |

---

## 3. Test rapide

### Healthcheck

```powershell
curl http://localhost:8000/
```

Attendu : `{"message":"API Rakuten opérationnelle"}`.

### Prédiction — mode REGISTRY (modèle Production)

```powershell
curl.exe -X POST http://localhost:8000/predict `
  -H "x-token: RAKUTEN_SECRET_123" `
  -H "Content-Type: application/json" `
  -d '{\"designation\":\"Piscine bestway tubulaire\",\"description\":\"Piscine de 3m de diamètre avec filtre et perche\"}'
```

> Sous PowerShell, préférer `curl.exe` (le `curl` natif est un alias
> vers `Invoke-WebRequest` à la syntaxe différente).

### Prédiction — mode RUN (run_id MLflow)

```powershell
curl.exe -X POST http://localhost:8000/predict `
  -H "x-token: RAKUTEN_SECRET_123" `
  -H "Content-Type: application/json" `
  -d '{\"designation\":\"Piscine bestway tubulaire\",\"description\":\"Piscine de 3m\",\"run_id\":\"<RUN_ID_MLFLOW>\"}'
```

Récupérer un `run_id` depuis MLflow UI (http://localhost:8081) → onglet Runs.

---

## 4. Architecture réseau

```
┌────────────┐         ┌────────────┐         ┌────────────┐
│  Airflow   │         │   MLflow   │         │    API     │
│  :8082     │────────▶│   :8081    │◀────────│   :8000    │
└────────────┘  log    └────────────┘  load   └────────────┘
                model        │           model
                             │
                         backend
                         SQLite + artifacts
                         (volume mlflow-data)
```

- Airflow et API utilisent `MLFLOW_TRACKING_URI=http://mlflow:8080`
  (nom de service Docker + port **interne**).
- Hôte utilise `http://localhost:8081` (port hôte mappé).

---

## 5. Arrêter

```powershell
docker compose stop api         # arrêt propre
docker compose down             # arrêt + suppression conteneurs
```

---

## Dépannage

| Symptôme                                                     | Cause probable                                                              | Action                                                                                |
|--------------------------------------------------------------|------------------------------------------------------------------------------|---------------------------------------------------------------------------------------|
| `Erreur lors du chargement du modèle en Production`          | Aucun modèle dans le Model Registry, ou alias `production` non posé        | Enregistrer un modèle via `mlflow.register_model(...)` + poser l'alias dans MLflow UI.|
| `Token invalide ou manquant`                                 | Header `x-token` absent ou incorrect                                        | Ajouter `-H "x-token: RAKUTEN_SECRET_123"` à la requête.                              |
| `Connection refused mlflow:8080`                             | API démarrée avant MLflow / service MLflow down                             | `docker compose up -d mlflow` puis `docker compose restart api`.                      |
| `FileNotFoundError: Y_train_encode.csv`                      | Mapping métier absent du build context                                       | Vérifier que `data/processed/Y_train_encode.csv` existe et n'est PAS dans `.dockerignore`.|
| Incompatibilité modèle (`AttributeError`, `dtype mismatch`)  | Versions numpy/sklearn différentes entre training (Airflow) et inférence (API) | Aligner les pins dans `docker/api/requirements.txt` et `docker/airflow/requirements.txt`.|

---

## Notes

- **Token API** : actuellement codé en dur dans `src/api/app.py`
  (`API_TOKEN = "RAKUTEN_SECRET_123"`). À externaliser via variable
  d'environnement avant toute mise en production.
- Le code applicatif **n'est pas monté en bind mount** : toute modif de
  `src/` nécessite `docker compose build api`. C'est volontaire (image
  reproductible). Pour itérer plus vite en dev, ajouter temporairement
  `volumes: - ./src:/app/src` dans le bloc `api:` du compose.
