# 📦 Rakuten MLOps Pipeline - Airflow

## 🎯 Objectif du projet

Ce projet a pour objectif de construire un pipeline **MLOps complet** pour la classification de produits Rakuten en utilisant :

- Airflow (orchestration)
- Docker (environnement reproductible)
- Scikit-learn (modèle ML)
- TF-IDF (feature engineering texte)
- LinearSVC (modèle de classification)

---

## 🏗️ Architecture du pipeline

Le DAG `rakuten_ml_pipeline` est composé de 4 étapes :

1. **Load Data**
   - Chargement des datasets RAW
   - Fusion X / Y via `Unnamed: 0`
   - Sélection des colonnes utiles

2. **Preprocessing**
   - Nettoyage du texte
   - Lowercase
   - Création de la variable `text`

3. **Training**
   - Split train/test (80/20 stratifié)
   - Vectorisation TF-IDF :
     - Word n-grams (1–2)
     - Char n-grams (3–5)
   - Modèle : LinearSVC (class_weight balanced)
   - Sauvegarde du modèle + test set

4. **Evaluation**
   - Prédictions sur test set
   - Calcul des métriques :
     - Accuracy
     - Classification report
   - Sauvegarde dans `metrics.json`

---

## 🧠 Choix techniques

### 🔹 TF-IDF
Permet une représentation robuste du texte :
- mots (word n-grams)
- sous-mots (char n-grams)

### 🔹 LinearSVC
- performant sur texte haute dimension
- rapide à entraîner
- bon compromis précision / vitesse

### 🔹 Train/Test Split
- évite le data leakage
- garantit une évaluation réaliste du modèle

---

## 🐳 Infrastructure Docker

Le projet est exécuté dans un environnement Docker :

```bash
docker run -it -p 8080:8080 \
-v ${PWD}/dags:/opt/airflow/dags \
-v ${PWD}/data:/opt/airflow/data \
-v ${PWD}/models:/opt/airflow/models \
airflow-rakuten airflow standalone




FEV26-CMLOPS-RAKUTEN/
│
├── dags/
│   ├── rakuten_ml_pipeline.py
│   └── test.py
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   ├── 1.3_rakuten_model_final.pkl
│   ├── test_data.pkl
│   └── metrics.json
│
└── Dockerfile