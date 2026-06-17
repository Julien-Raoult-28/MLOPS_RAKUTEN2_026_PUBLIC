import streamlit as st
from app_streamlit.core.utils import affiche_bandeau

def run():
    affiche_bandeau("Orchestration et Déploiement")

    st.markdown("""
<style>
/* Centrage horizontal des onglets */
div[data-baseweb="tab-list"] {
    justify-content: center;
    gap: 24px;   /* espace horizontal entre les onglets */
}

/* Bouton d’onglet */
button[data-baseweb="tab"] {
    padding-top: 8px;
    padding-bottom: 10px;
    min-height: 72px;
}

/* Texte des onglets */
button[data-baseweb="tab"] > div {
    font-size: 14px;
    font-weight: 600;
    text-align: center;
    white-space: pre-line;
    line-height: 1.2;
}

/* Onglet actif */
button[data-baseweb="tab"][aria-selected="true"] > div {
    font-weight: 800;
}
</style>
""", unsafe_allow_html=True)


    tabs = st.tabs([
        "🏗️\n Architecture globale du système",
        "🧠\nPipeline Machine Learning",
        "🔬\nMLflow — tracking et gouvernance modèle",
        "⚙️\nAirflow — orchestration ML",
        "🚀\nFastAPI — serving ML",
        "🐳\nDocker & infrastructure"
    ])

###  Architecture globale du système --------------------------------------------------------------------------------------------
    with tabs[0]: 
        import base64
        with open("app_streamlit/assets/images/architecture2.png", "rb") as img_file:
            img_bytes = img_file.read()
            encoded = base64.b64encode(img_bytes).decode()
        st.markdown(f"""
                    
<div style="
            background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
            padding:5px;
            border-left:6px solid #bf0000;
            border-radius:15px;
            margin: 20px auto;
            box-shadow: 0 8px 20px rgba(0,0,0,0.1);
            font-family: 'Segoe UI';
            width:85%;
">

<h4 style="color:#bf0000;text-align:center;">Architecture du projet</h4>
<div style="text-align:center;margin-bottom:50px;"><img src="data:image/png;base64,{encoded}" style="width:100%; object-fit:contain;"/></div>  
  
•	1 machine, 3 services orchestrés par `docker compose`  
•	Entraînement (offline) **découplé** de l'inférence (online)  
•	MLflow = point de contact unique → traçabilité  
</div>
                    


<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    "> 
                                 
<h5 style="color:#bf0000; margin-top:0;">Décision structurante : architecture microservices</h5>     
                 
**✔ Choix effectué**   
Architecture découplée en services indépendants.  
                  
**✔ Avantages**  
                 
•	scalabilité indépendante des composants  
•	simulation réaliste d’un système industriel  
•	meilleure maintenabilité  
•	séparation des responsabilités  
                 
**❌ Inconvénients**  
                 
•   complexité réseau Docker  
•	debugging distribué difficile  
•	latence inter-services  
                 
**👉 Trade-off assumé : complexité ↔ réalisme industriel**
             
 </div>

 

""", unsafe_allow_html=True)
     


###  Pipeline --------------------------------------------------------------------------------------------
    with tabs[1]:
     st.markdown("""
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    ">
 

<h5 style="color:#bf0000; margin-top:0;">Choix du modèle</h5>   
                 
**Modèle retenu :**  
•	TF-IDF  
•	LinearSVC  

</div>

<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    "> 
                                 
<h5 style="color:#bf0000; margin-top:0;">Justification technique</h5>   

**✔ TF-IDF**
                 
•	performant sur texte court  
•	faible coût computationnel  
•	robuste sans deep learning  
                 
**❌ Limites**  
                 
•	pas de compréhension sémantique  
                 
**✔ LinearSVC**  
                 
•	très performant en haute dimension  
•	rapide à entraîner  
•	stable en production  
                 
**❌ Limite critique**  
                 
•	pas de statistiques de confiance (probabilités) 
                 
**👉 impact direct sur :**  
                 
•	absence de score de confiance  
        
 </div>
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    "> 
                                 
<h5 style="color:#bf0000; margin-top:0;">Pipeline sklearn (design critique)</h5>  
                 
**Pipeline unifié :**  
                 
•	vectorisation TF-IDF  
•	features texte enrichies  
•	classifieur LinearSVC  

</div>
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    "> 
                                 
<h5 style="color:#bf0000; margin-top:0;">Décision clé : ColumnTransformer multi-features</h5>    
                 
**Nous avons combiné :**  
                 
•	TF-IDF mots  
•	TF-IDF caractères  
•	features heuristiques  
                 
**✔ Avantages**  
                 
•	robustesse bruit texte  
•	meilleure généralisation  
•	enrichissement sémantique  
                 
</div>

 
""", unsafe_allow_html=True) 

###  MLflow — tracking et gouvernance modèle --------------------------------------------------------------------------------------------
    with tabs[2]:
     st.markdown("""
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    ">
<table style="width:100%; margin-top:10px; border-collapse: collapse;">
    <tr>
        <th style="text-align:center; padding:8px;">Tracking</th>
        <th style="text-align:center; padding:8px;">Registry</th>
        <th style="text-align:center; padding:8px;">Gouvernance</th>
    </tr>
    <tr><td style="text-align:center;">runs - params - métriques</td><td style="text-align:center;">`rakuten_classifier` versionné</td><td style="text-align:center;"> alias `@production`</td></tr>
</table>                

                 
•	SQLite (métadonnées) + /mlruns (artefacts)  
•	Volume mlflow-data → persistant  


 `UI MLflow → http://localhost:8089`                
 </div>                
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    ">
 

<h5 style="color:#bf0000; margin-top:0;">Rôle</h5>    
                 
MLflow est utilisé comme :  
                 
•	système de tracking  
•	registre de modèles  
•	historique des expérimentations  

 </div>
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    ">
 

<h5 style="color:#bf0000; margin-top:0;">Décision clé : Model Registry + alias production</h5>      
                               
**✔ Avantages**  
                 
•	découplage train / serve  
•	rollback possible  
•	versioning propre  
                 
**❌ Inconvénients**  
                 
•	dépendance forte à MLflow server  
•	latence chargement modèle  
 </div>
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    ">
 

<h5 style="color:#bf0000; margin-top:0;">Point critique ingénierie</h5>     
                 
**👉 Le modèle embarque du code custom :** code_paths=["/opt/airflow/src"]
  
**✔ Avantage**  
                 
•	reproductibilité totale  
                 
**❌ Inconvénient**  
                 
•	couplage modèle ↔ code source  
                 
**👉 Trade-off classique MLOps réel**
</div>                

""", unsafe_allow_html=True) 
     
###  Airflow — orchestration ML --------------------------------------------------------------------------------------------
    with tabs[3]:
     st.markdown("""
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    ">
 

<h5 style="color:#bf0000; margin-top:0;">Objectif d'Airflow</h5>   
                    
Airflow est utilisé comme orchestrateur du pipeline ML afin d'automatiser, planifier et superviser les différentes étapes du cycle de vie du modèle.  

**Valeur ajoutée** :  

•	automatisation des traitements  
•	exécution reproductible  
•	traçabilité  
•	gestion des dépendances entre tâches  
•	monitoring des exécutions  

</div> 
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    ">
 

<h5 style="color:#bf0000; margin-top:0;">Description du DAG</h5>         

•	**load_data** : chargement des données brutes  
•	**preprocess_data** : prétraitement des données  
•	**train_model** : entraînement du modèle      
•	**evaluate_model** : évaluation du modèle  
•	**model registry** : enregistrement du modèle dans MLflow  
                 
Chacune de ces tâches est encapsulée dans une fonction Python distincte, ce qui permet de maintenir un code clair et modulaire.   
Les étapes sont orchestrées dans un DAG (Directed Acyclic Graph) qui définit l'ordre d'exécution et les dépendances entre les tâches.  
Elles ne démarrent que si la tâche précédente a été exécutée avec succès, assurant ainsi la cohérence du pipeline.  
                 
•	une tâche en échec bloque les suivantes  
•	possibilité de relancer uniquement la tâche concernée  
•	historique des exécutions conservé  
</div> 
                 
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    ">
 

<h5 style="color:#bf0000; margin-top:0;">Intégration avec MLflow</h5> 

Airflow  
&nbsp;&nbsp;&nbsp;&nbsp;↓  
Lance l'entraînement  
&nbsp;&nbsp;&nbsp;&nbsp;↓  
MLflow enregistre :  
- paramètres  
- métriques  
- artefacts  
&nbsp;&nbsp;&nbsp;&nbsp;↓  
Model Registry  
                 
</div>
                 
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    ">
                 
<h5 style="color:#bf0000; margin-top:0;">Choix d'architecture</h5>    
                 
**✔ Avantages**  
                 
•	standard industriel  
•	visualisation des workflows  
•	planification des exécutions  
•	reprise sur erreur  
                 
**Trade-off**  
                 
Complexité supplémentaire mais gain important en industrialisation et en reproductibilité.  
</div>


""", unsafe_allow_html=True) 
     
###  FastAPI — serving ML --------------------------------------------------------------------------------------------
    with tabs[4]:
     st.markdown("""
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    ">  
                 
**2 routes** :   

•	  `POST /predict` → catégorie + version utilisée  
•	  `GET /models` → versions disponibles    

 **Choix du modèle** :  

•	  **3 façons de choisir le modèle** : run précis · version · production (défaut)  
•	  **Cache RAM** → ~10-15 ms / requête  
•	  **Swagger auto** → http://localhost:8000/docs  
                 

`{ `   
`"designation": "...",`  
`"description": "...",`    
`"model_version": "2"`    
`}`   
language=`json`  
                 
</div>
                 
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    ">
 

<h5 style="color:#bf0000; margin-top:0;">Design</h5>  
                 
**Endpoint :**  
                   
POST /predict  
  
**Modes :**    
                 
•	production (MLflow registry)  
•	run_id (debug modèle)  
</div>

<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    ">
 

<h5 style="color:#bf0000; margin-top:0;">Décision clé : API hybride</h5>    
                 
**✔ Avantages**  
                 
•	A/B testing possible  
•	debug facilité  
•	flexibilité forte  
                 
**❌ Inconvénients**  
                 
•	complexité utilisateur  
•	risque erreur de modèle  
</div>
                 
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    ">
                 
<h5 style="color:#bf0000; margin-top:0;">Sécurité</h5>    
                 
•	token HTTP (x-token)  
•	validation Pydantic  
•	gestion erreurs centralisée  
                 
**Limite**  
                 
•	pas de JWT / OAuth2  
                 
**👉 Choix volontaire pédagogique**  

</div>

""", unsafe_allow_html=True) 

     

     
###  Docker & infrastructure --------------------------------------------------------------------------------------------
    with tabs[5]:
     st.markdown("""
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    ">
<h5 style="color:#bf0000; margin-top:0;">
    Infrastructure reproductible — <span style="color:green; font-size:0.85em;">docker compose up</span>
</h5>
 <table style="width:100%; margin-top:10px; border-collapse: collapse;">
    <tr>
        <th style="text-align:center; padding:8px;">Service</th>
        <th style="text-align:center; padding:8px;">Rôle</th>
        <th style="text-align:center; padding:8px;">Port</th>
    </tr>
    <tr>
        <td style="text-align:center;">mlflow</td>
        <td style="text-align:center;">tracking + registry</td>
        <td style="text-align:center;">8089</td>
    </tr>
    <tr>
        <td style="text-align:center;">api</td>
        <td style="text-align:center;">inférence</td>
        <td style="text-align:center;">8000</td>
    </tr>
    <tr>
        <td style="text-align:center;">airflow</td>
        <td style="text-align:center;">entraînement</td>
        <td style="text-align:center;">8082</td>
    </tr>
</table>  
                 
•	Réseau `mlops-net` : services joignables par nom  
•	Volume `mlflow-data` : persistance  
•	`.env` : ports & RAM configurables     
                                              
</div>
                                  
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    ">
 

<h5 style="color:#bf0000; margin-top:0;">Décision : Docker Compose full stack</h5>   
                 
**Services :**  
                 
•	API  
•	Airflow  
•	MLflow  
•	Prometheus  
•	Grafana  
</div>
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    ">
 

<h5 style="color:#bf0000; margin-top:0;">✔ Avantages</h5>   

•	reproductibilité totale  
•	onboarding simplifié  
•	environnement standardisé  
                   
</div>
</div>
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    width:85%;          
    ">
 

<h5 style="color:#bf0000; margin-top:0;">❌ Inconvénients</h5>     
                 
•	consommation RAM élevée  
•	startup lent  
•	debugging réseau complexe  
</div>

""", unsafe_allow_html=True) 