## 📁 Structure du projet
```
FEV26-CMLOPS-RAKUTEN/
│
├── api/
│
├── data/
│   ├── processed/              # données préparées
│   │   └── Y_train_encode.csv
│   │
│   └── raw/                   # données d'origine
│       ├── X_test_update.csv
│       ├── X_train_update.csv
│       └── Y_train_CVw08PX.csv
│
├── models/                    # modèles (.pkl / .joblib)
│   └── 1.3_rakuten_model_final.pkl
│
├── notebooks/
│   ├── Entrainement_test.ipynb
│   └── grid_search.ipynb
│
├── src/
│   ├── data/                  # code de préparation des données
│   │
│   └── models/                # code de génération des modèles
│       └── 1.2_model_prediction.py
│
├── requirements.txt
├── LICENSE
├── .gitignore
└── README.md
```