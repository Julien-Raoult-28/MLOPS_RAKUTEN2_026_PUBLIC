## 📁 Structure du projet
```
FEV26-CMLOPS-RAKUTEN/
├── .gitignore
├── GITHUB.txt
├── README.md
├── data
│   ├── processed  # données modifiées
│   │   └── Y_train_encode.csv
│   └── raw  # ici les données brut
│       ├── X_test_update.csv
│       ├── X_train_update.csv
│       └──  Y_train_CVw08PX.csv
├── models   #ici seront stocké les fichiers .pkl et .joblib
│   └── 1.3_rakuten_model_final.pkl
├── notebook
│   ├── Entrainement_test.ipynb
│   ├── arborescence.py
│   ├── grid_search.ipynb
└── src
    ├── api
    │   ├── api.txt
    │   └── main.py
    ├── data  # code python du pre processing data
    │   └── 
    ├── features
    │   └── text_features.py   #fonction pour TF-IDF
    └── models
        ├── 1_2_model_prediction.py
        └── src_models.txt
```