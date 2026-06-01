
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

git add app_streamlit/
git commit -m "Update Streamlit app"
git push origin main




------------------------------------------------------------------------------
Mettre à jour les références du dépôt distant :
git fetch origin

Récupérer uniquement le dossier et le fichier :
git restore --source=origin/main app_streamlit streamlit_app.py

Vérifier les modifications :
git status

Tu verras les fichiers récupérés comme modifiés dans ton working tree.