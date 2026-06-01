
FEV26-CMLOPS-RAKUTEN/
│
|──.stremlit/config.toml
|
|── streamlit/
|    ├── app.py   👈 lancé ici
|    ├── core/
|    │    ├── config.py
│    |    ├── layout.py        # TON bandeau + styles
│    |    ├── sidebar.py       # menu + radio
│    |    └── utils.py         # fonctions comme affiche_bandeau
|    ├── page_modules/
|    │    ├── presentation.py
|    │    ├── exploration.py
|    └── assets/
|    |    ├──images/
|    |    │    ├── rakuten.png
|    |    │    ├── favicon_Rakuten.png

Pour lancer streamlit
streamlit run streamlit_app.py

git add streamlit/
git commit -m "Update Streamlit app"
git push origin main