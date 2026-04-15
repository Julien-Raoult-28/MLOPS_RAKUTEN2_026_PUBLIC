# 📘 **Projet MLOps – Classification Rakuten**  
### **API FastAPI hybride MLflow + SQLite – Version stable v1.0.0**

---

## 🧭 **1. Présentation du projet**

Ce projet implémente une **API de classification de produits Rakuten**, basée sur un modèle MLflow et une architecture MLOps moderne.  
L’API permet de prédire la catégorie d’un produit à partir de sa description textuelle, avec un pipeline complet :

- **FastAPI** pour l’exposition du service  
- **MLflow Tracking + Model Registry** pour la gestion des modèles  
- **SQLite** pour le mapping métier (catégorie → libellé)  
- **Pydantic v2** pour la validation stricte des entrées  
- **Sécurité par token**  
- **Tests unitaires complets (pytest)**  

La version **v1.0.0** est la première version stable, testée et prête pour la soutenance.

---

## 🏗️ **2. Architecture du projet**

```
project/
│
├── api/
│   ├── main.py               # API FastAPI
│   ├── schemas.py            # Pydantic v2
│   ├── security.py           # Token
│   ├── mlflow_loader.py      # Chargement modèle MLflow
│   ├── sqlite_backend.py     # Mapping métier
│   └── utils.py              # Fonctions auxiliaires
│
├── tests/
│   └── test_api.py           # 9 tests unitaires
│
├── mlruns/                   # MLflow Tracking (ignoré par Git)
├── mlflow.db                 # Base SQLite MLflow
├── data/                     # Données (ignorées par Git)
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ **3. Installation**

### **Créer un environnement virtuel**

```
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

### **Installer les dépendances**

```
pip install -r requirements.txt
```

---

## 🚀 **4. Lancer l’API**

```
uvicorn api.main:app --reload
```

L’API sera disponible sur :

👉 `http://127.0.0.1:8000` [(127.0.0.1 in Bing)](https://www.bing.com/search?q="http%3A%2F%2F127.0.0.1%3A8000%2F")  
👉 Documentation Swagger : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🔐 **5. Sécurité – Token obligatoire**

Toutes les requêtes doivent inclure :

```
x-token: RAKUTEN_SECRET_123
```

Sinon → **401 Unauthorized**

---

## 🧪 **6. Endpoints**

### **POST /predict**

#### **Entrée :**

```json
{
  "description": "Chaussures de sport pour homme",
  "run_id": "optional"
}
```

#### **Sortie :**

```json
{
  "prediction": 10,
  "label": "Sportswear",
  "model_version": "v1.0.0",
  "run_id_used": "xxxx"
}
```

---

## 🧠 **7. Fonctionnement du modèle (hybride)**

### ✔ **Cas 1 — run_id fourni**
L’API charge **le modèle MLflow correspondant**.

### ✔ **Cas 2 — run_id absent**
L’API charge **le modèle en Production** depuis le Model Registry.

### ✔ **Cas 3 — run_id invalide**
Retourne une erreur propre :

```
400 — Invalid run_id
```

---

## 🗄️ **8. Backend SQLite**

Le fichier `sqlite_backend.py` gère :

- le mapping catégorie → libellé  
- la récupération des labels  
- la robustesse en cas de catégorie inconnue  

---

## 🧪 **9. Tests unitaires (pytest)**

### ✔ 9 tests PASS :

- healthcheck  
- token valide / invalide  
- validation Pydantic (422)  
- prédiction simple  
- prédiction avec run_id  
- prédiction sans run_id (fallback)  
- erreurs MLflow  
- robustesse texte long  
- structure JSON complète  

Lancer les tests :

```
pytest -q
```

---

## 🧱 **10. Workflow Git**

### ✔ Branches utilisées

- `main` → stable, production  
- `angella-dev` → développement, tests, corrections  

### ✔ Processus

1. Développement sur `angella-dev`  
2. Tests unitaires  
3. Tests manuels  
4. PR vers `main`  
5. Merge  
6. Release v1.0.0  

---

## 🏷️ **11. Release v1.0.0**

La release inclut :

- API stable  
- Architecture hybride MLflow + SQLite  
- Sécurité token  
- Tests unitaires complets  
- `.gitignore` finalisé  
- Code propre, modulaire, maintenable  

👉 Disponible ici :  
[https://github.com/DataScientest-Studio/FEV26-CMLOPS-RAKUTEN/releases/tag/v1.0.0](https://github.com/DataScientest-Studio/FEV26-CMLOPS-RAKUTEN/releases/tag/v1.0.0)

---

## 🎓 **12. Soutenance – Points clés à présenter**

- Architecture MLOps moderne  
- API robuste et sécurisée  
- MLflow Tracking + Registry  
- Tests unitaires complets  
- Workflow Git professionnel  
- Release versionnée  
- Code propre et maintenable  


