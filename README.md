Angella…  
Voici **la version mise à jour, complète, propre, professionnelle et friendly** de ton **README officiel**.  
Il est structuré, clair, pédagogique, et reflète parfaitement ton pipeline MLOps actuel (avec API, prédiction enrichie, mapping métier, etc.).

Tu peux le coller tel quel dans ton repo GitHub.

---

# 📘 **README — Projet MLOps Rakuten Classification**  
### *Pipeline complet : entraînement, évaluation, prédiction, MLflow, CLI Typer, API FastAPI*  
---

# 🟦 1. Présentation du projet

Ce projet implémente un **pipeline MLOps complet** pour classifier les produits Rakuten à partir de texte (désignation + description).

Il inclut :

- un pipeline **TF‑IDF + modèle linéaire** encapsulé dans sklearn  
- un suivi complet avec **MLflow** (params, metrics, artefacts, modèle)  
- un mode **FAST/FULL** pour accélérer le développement  
- un **CLI professionnel (Typer)** pour entraîner, évaluer et prédire  
- une **API FastAPI** pour exposer le modèle  
- une **réponse JSON enrichie** (label métier, temps d’inférence, métadonnées…)  
- une architecture **modulaire, propre, industrialisable**

Ce projet est conçu pour être **pédagogique**, **reproductible**, **traçable**, et **prêt pour la production**.

---

# 🟩 2. Architecture du projet

```
FEV26-CMLOPS-RAKUTEN/
│
├── data/                     # Données brutes / intermédiaires / finales
├── mlruns/                   # Tracking MLflow (runs, artefacts, modèles)
│
├── src/
│   ├── data/
│   │   └── load_data.py
│   │
│   ├── features/
│   │   └── text_features.py
│   │
│   ├── models/
│   │   ├── train.py          # Entraînement + MLflow
│   │   ├── evaluate.py       # Évaluation via run_id
│   │   └── predict.py        # Prédiction enrichie
│   │
│   ├── services/
│   │   └── prediction_service.py  # Logique métier API
│   │
│   ├── api/
│   │   └── app.py            # API FastAPI
│   │
│   ├── utils/
│   │   └── config_loader.py
│   │
│   └── cli.py                # ⭐ CLI complet (Typer)
│
├── config.yaml               # Configuration globale
└── README.md
```

---

# 🟧 3. Architecture MLOps (pipeline visuel)

```
config.yaml
     │
     ▼
Chargement des données (load_data.py)
     │
     ▼
Feature engineering (TF-IDF + features custom)
     │
     ▼
Pipeline sklearn (TF-IDF + modèle linéaire)
     │
     ▼
Entraînement (train.py)
     │
     ▼
Évaluation (evaluate.py)
     │
     ▼
MLflow tracking (params, metrics, artefacts, modèle)
     │
     ▼
Prédiction (predict.py / CLI / API FastAPI)
```

---

# 🟨 4. Installation & Configuration

## 1. Cloner le projet

```bash
git clone <repo>
cd FEV26-CMLOPS-RAKUTEN
```

## 2. Créer et activer l’environnement virtuel

```powershell
python -m venv .venv
.\.venv\Scripts\activate
```

## 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## 4. Définir PYTHONPATH (IMPORTANT)

### PowerShell :

```powershell
$env:PYTHONPATH = (Get-Location)
```

### Pourquoi ?

Parce que Python ne sait pas automatiquement où se trouve `src/`.

👉 *“Voici la racine du projet, cherche les modules ici.”*

Sans cette ligne, les imports `from src...` échouent.

---

# 🟦 5. Configuration du projet (config.yaml)

Exemple :

```yaml
mode: fast

mlflow:
  tracking_uri: "file:./mlruns"
  experiment_name: "rakuten_classification"
```

### Modes disponibles :

| Mode | Description |
|------|-------------|
| **fast** | Petit échantillon → rapide pour tester |
| **full** | Dataset complet → métriques réelles |

---

# 🟩 6. Lancer MLflow UI

Depuis **CMD (pas PowerShell)** :

```cmd
mlflow ui
```

Puis ouvrir :

👉 [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

# 🟧 7. Utilisation du CLI complet (Typer)

Le CLI est le **point d’entrée officiel** du projet.

Toutes les commandes se lancent depuis la racine :

```
python -m src.cli <commande>
```

---

## ⭐ 1. Entraîner un modèle

### Mode FAST

```bash
python -m src.cli train-cmd --mode fast
```

### Mode FULL

```bash
python -m src.cli train-cmd --mode full
```

---

## ⭐ 2. Évaluer un modèle MLflow

```bash
python -m src.cli evaluate-cmd <run_id>
```

Exemple :

```bash
python -m src.cli evaluate-cmd 6c6634389c2a42f09befd37794ae299a
```

---

## ⭐ 3. Faire une prédiction (CLI)

```bash
python -m src.cli predict-cmd \
    --designation "Chaise en bois massif" \
    --description "Chaise robuste en bois naturel" \
    --run_id <run_id>
```

---

# 🟣 8. Utiliser l’API FastAPI

## 1. Lancer l’API

```bash
uvicorn src.api.app:app --reload
```

## 2. Ouvrir Swagger

👉 `http://127.0.0.1:8000/docs` [(127.0.0.1 in Bing)](https://www.bing.com/search?q="http%3A%2F%2F127.0.0.1%3A8000%2Fdocs")

## 3. Tester `/predict`

Entrer :

- designation  
- description  
- run_id  

Résultat :  
Une réponse JSON **professionnelle** :

```json
{
  "designation": "chaise bois",
  "description": "chaise bois massif",
  "prediction": {
    "prediction_code": 13,
    "label": "Maison",
    "confidence": null,
    "inference_time_ms": 57.3,
    "timestamp": "2026-04-10T15:16:37Z"
  },
  "run_id": "1eb81543c0cc4b9c8d9cd5352d1fe57c"
}
```

---

# 🟫 9. Scripts principaux

## 1. Entraînement (train.py)

- charge config  
- charge données  
- construit pipeline TF‑IDF + modèle  
- entraîne  
- évalue  
- logge dans MLflow :  
  - paramètres  
  - métriques  
  - artefacts  
  - modèle  

## 2. Évaluation (evaluate.py)

- recharge un modèle MLflow via run_id  
- calcule les métriques  
- logge les artefacts d’évaluation  

## 3. Prédiction (predict.py)

- recharge un modèle MLflow  
- applique preprocessing + modèle  
- renvoie :  
  - code prédictif  
  - libellé métier  
  - temps d’inférence  
  - timestamp  
  - métadonnées modèle  

---

# 🟪 10. Tips & Astuces MLOps

### ✔ Toujours utiliser FAST pour tester  
### ✔ Toujours définir PYTHONPATH  
### ✔ Toujours logger params + metrics + artefacts  
### ✔ Toujours encapsuler preprocessing + modèle dans un pipeline sklearn  
### ✔ Toujours tester une prédiction manuelle  
### ✔ Toujours séparer train / evaluate / predict  
### ✔ Toujours utiliser un venv  
### ✔ Toujours vérifier MLflow UI après un run  
### ✔ Toujours convertir numpy.int64 → int avant JSON  
### ✔ Toujours utiliser Path() pour les chemins  

---

# 🟥 11. Erreurs fréquentes (et comment les éviter)

❌ Lancer MLflow UI dans PowerShell  
→ utiliser CMD

❌ Oublier PYTHONPATH  
→ imports cassés

❌ Ne pas utiliser FAST  
→ perte de temps énorme

❌ Ne pas logger les artefacts  
→ impossible de diagnostiquer

❌ Mélanger preprocessing et modèle  
→ impossible de déployer

❌ Chemins absolus d’un autre PC  
→ utiliser Path() + chemins relatifs

---

# ⭐ 12. Roadmap MLOps (améliorations futures)

### 🔥 API FastAPI (déjà implémentée)  
→ prochaine étape : monitoring & authentification

### 📦 Dockerfile  
→ containerisation du pipeline + API

### 🪶 Airflow DAG  
→ automatiser entraînement + évaluation

### 🧪 Tests unitaires (pytest)  
→ sécuriser le code

### 🧩 Validation Pydantic  
→ sécuriser les inputs API

### 📊 Monitoring dérive de données  
→ alerter en cas de drift

---

# 🎉 13. Conclusion

Ce projet implémente un pipeline MLOps **complet**, **propre**, **professionnel**, incluant :

- architecture modulaire  
- pipeline sklearn encapsulé  
- MLflow tracking  
- modes FAST/FULL  
- évaluation indépendante  
- prédiction enrichie  
- CLI complet Typer  
- API FastAPI  

Il est prêt pour :

- la production  
- la démonstration  
- l’enseignement  
- l’industrialisation  

