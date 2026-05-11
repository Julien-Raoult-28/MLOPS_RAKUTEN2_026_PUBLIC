# Conventions Docker du projet

Ce dossier contient un sous-dossier par service conteneurisé. L'orchestration
de l'ensemble se fait depuis `docker-compose.yml` à la racine du projet.

## Structure

```
docker/
├── mlflow/    → Dockerfile du tracking server MLflow      (Dimitri)
├── api/       → Dockerfile de l'API FastAPI + guide        (Dimitri)
├── airflow/   → Dockerfile d'Airflow + guide de test      (Dimitri)
└── README.md  → ce fichier
```

### Guides spécifiques par service

- **Airflow** : voir [`docker/airflow/README.md`](airflow/README.md)
  pour lancer Airflow + MLflow et exécuter le DAG `rakuten_ml_pipeline`.
- **API FastAPI** : voir [`docker/api/README.md`](api/README.md) pour
  lancer le service d'inférence et tester `POST /predict`.

## Ajouter un nouveau service — checklist

1. Créer `docker/<nom-service>/Dockerfile`.
2. Décommenter (ou ajouter) la section correspondante dans
   `docker-compose.yml` à la racine, en suivant le modèle du service `mlflow`.
3. Si le service a besoin de variables d'environnement, les ajouter dans
   `.env.example` (pour servir de référence aux coéquipiers).
4. Brancher le service sur le réseau `mlops-net`.
5. Tester avec :
   ```bash
   docker compose up -d <nom-service>
   docker compose logs -f <nom-service>
   ```

## Conventions

### Ports hôtes réservés

| Service       | Port hôte | Port interne | Variable .env       |
|---------------|-----------|--------------|---------------------|
| MLflow UI     | 8081      | 8080         | `MLFLOW_HOST_PORT`  |
| API FastAPI   | 8000      | 8000         | `API_HOST_PORT`     |
| Airflow web   | 8082      | 8080         | `AIRFLOW_HOST_PORT` |

> Si un port est déjà pris sur ta machine, change-le dans **ton** `.env` local.
> Pas besoin de modifier `docker-compose.yml`.

### Volumes

Toujours nommés `<service>-data` (ex : `mlflow-data`, `airflow-data`).
Déclarés dans la section `volumes:` à la fin de `docker-compose.yml`.

### Communication entre services

Depuis l'intérieur du réseau Docker, les services s'appellent par leur **nom
de service** et leur **port interne**, jamais par `localhost` ni par le port
hôte.

| Contexte d'exécution                  | URL pour joindre MLflow         |
|---------------------------------------|---------------------------------|
| Script lancé sur la machine hôte      | `http://localhost:8081`         |
| Conteneur API ou Airflow              | `http://mlflow:8080`            |

### Variables d'environnement

- Le code applicatif **ne hardcode jamais d'URL**. Il lit
  `os.getenv("MLFLOW_TRACKING_URI", "<fallback-local>")`.
- En local : la valeur vient du fichier `.env` chargé via `python-dotenv`.
- En conteneur : la valeur est injectée par `environment:` dans
  `docker-compose.yml`.

## Commandes utiles

```bash
# Construction & démarrage
docker compose build                  # construit toutes les images
docker compose build mlflow           # juste un service
docker compose up -d                  # tout lancer en arrière-plan
docker compose up -d mlflow           # juste un service

# Inspection
docker compose ps                     # état des services
docker compose logs -f <service>      # logs en suivi temps réel

# Arrêt
docker compose stop                   # arrête sans supprimer
docker compose down                   # arrête + supprime conteneurs
docker compose down -v                # ⚠️ + supprime les VOLUMES (données perdues)
```
