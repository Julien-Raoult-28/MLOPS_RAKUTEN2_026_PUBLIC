---
# 🧾 **README_MLOPS.md — Projet Rakuten (Pipeline Texte)**  
### *Orchestration & Déploiement — Phase 3*

---

## 🎯 1. Objectif du système

Ce projet met en place un pipeline MLOps complet permettant de :

- charger automatiquement les données,
- prétraiter les textes,
- entraîner un modèle TF‑IDF + LinearSVC,
- évaluer ses performances,
- enregistrer le modèle dans MLflow Model Registry,
- exposer une API FastAPI pour l’inférence,
- orchestrer l’ensemble via Airflow,
- conteneuriser tous les services via Docker Compose.

Ce README explique **comment lancer l’infrastructure**, **comment exécuter le pipeline**, et **comment tester l’API**.

---

## 🏗️ 2. Architecture générale

```
+------------------+        +------------------+        +------------------+
|     Airflow      | -----> |      MLflow      | -----> |     FastAPI      |
|  (orchestration) |        | (tracking + reg.)|        |  (inférence)     |
+------------------+        +------------------+        +------------------+
         |                           |                           |
         +----------- Docker Compose orchestration --------------+
```

### Services inclus

| Service | Rôle |
|--------|------|
| **airflow** | Orchestration du pipeline ML |
| **mlflow** | Tracking + Model Registry |
| **api** | Service d’inférence |
| **docker-compose** | Orchestration des microservices |

---

## 📦 3. Prérequis

Avant de commencer, installer :

- **Docker Desktop**  
- **Git**  
- **Python 3.11** (optionnel, uniquement pour tests locaux)  

Ports requis :

- MLflow UI → **8081**
- Airflow UI → **8082**
- API FastAPI → **8000**

---

## 📁 4. Cloner le projet

```bash
git clone <URL_DU_REPO>
cd FEV26-CMLOPS-RAKUTEN
```

---

## 🐳 5. Lancer l’infrastructure (Docker Compose)

### 5.1. Build + lancement

```bash
docker compose up -d --build
```

### 5.2. Vérifier les conteneurs

```bash
docker ps
```

Vous devez voir :

- fev26-cmlops-rakuten-airflow-1  
- fev26-cmlops-rakuten-mlflow-1  
- fev26-cmlops-rakuten-api-1  

---

## 🔧 6. Vérifier MLflow

### 6.1. Logs MLflow

```bash
docker logs fev26-cmlops-rakuten-mlflow-1 | head
```

Vous devez voir :

```
Allowed hosts: mlflow, mlflow:8080, localhost, ...
```

### 6.2. Interface MLflow

Ouvrir :

```
http://localhost:8081
```

---

## 🔧 7. Vérifier Airflow

Ouvrir :

```
http://localhost:8082
```

Identifiants :

- **user** : airflow  
- **password** : airflow  

---

## 🚀 8. Lancer le pipeline ML (DAG Airflow)

### 8.1. Trigger du DAG

```bash
docker exec -it fev26-cmlops-rakuten-airflow-1 airflow dags trigger rakuten_ml_pipeline
```

### 8.2. Vérifier les runs

```bash
docker exec -it fev26-cmlops-rakuten-airflow-1 airflow dags list-runs -d rakuten_ml_pipeline
```

### 8.3. Suivre les logs d’une tâche

```bash
docker exec -it fev26-cmlops-rakuten-airflow-1 bash -c \
"tail -f /opt/airflow/logs/dag_id=rakuten_ml_pipeline/run_id=<RUN_ID>/task_id=train/*"
```

---

## 🧠 9. Pipeline ML (texte uniquement)

Le pipeline Airflow exécute les étapes suivantes :

1. **load**  
   - Chargement des données brutes  
   - Vérification des colonnes  

2. **preprocess**  
   - Nettoyage HTML  
   - Suppression des stopwords  
   - Uniformisation linguistique  
   - Extraction de features  
   - Vectorisation TF‑IDF (120k features)  

3. **train**  
   - Modèle : LinearSVC(class_weight="balanced")  
   - Logging MLflow  

4. **evaluate**  
   - F1-score pondéré  
   - Logging MLflow  

5. **register_model**  
   - Enregistrement dans MLflow Model Registry  
   - Alias : `production`  

---

## 🧪 10. Tester l’API FastAPI

### 10.1. Interface Swagger

```
http://localhost:8000/docs
```

### 10.2. Exemple de requête

```json
{
  "designation": "Lot de 3 livres de cuisine",
  "description": "Recettes faciles et rapides pour tous les jours"
}
```

---

## 🧹 11. Réinitialiser complètement l’infrastructure

```bash
docker compose down -v
docker compose up -d --build
```

---

## 🛠️ 12. Dépannage (FAQ interne)

### ❌ Airflow → MLflow : erreur 403 “Invalid Host Header”
Solution :

Dans `docker-compose.yml` :

```
--allowed-hosts mlflow,mlflow:8080,localhost,127.0.0.1,0.0.0.0
```

Puis :

```
docker compose down -v
docker compose up -d --build
```

### ❌ L’API ne répond pas
Vérifier :

```bash
docker logs fev26-cmlops-rakuten-api-1
```

### ❌ Le DAG ne s’exécute pas
Vérifier :

```bash
docker logs fev26-cmlops-rakuten-airflow-1
```

---

## 📌 13. Points importants pour l’équipe

- **Ne jamais modifier les Dockerfiles sans rebuild complet.**  
- **Toujours vérifier MLflow avant de lancer un DAG.**  
- **Toujours utiliser `docker compose down -v` en cas de comportement étrange.**  
- **L’API consomme le modèle depuis MLflow, pas depuis un fichier local.**  

---

## 🎉 14. Conclusion

Ce README permet à n’importe quel membre de l’équipe de :

- lancer l’infrastructure,  
- exécuter le pipeline ML,  
- suivre les runs dans MLflow,  
- tester l’API,  
- comprendre l’architecture globale.

C’est la base d’un système MLOps **réel, robuste et industrialisab
