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
        "📊\nMonitoring — Prometheus & Grafana",
        "🐳\nDocker & infrastructure"
    ])

###  Architecture globale du système --------------------------------------------------------------------------------------------
    with tabs[0]:
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
 

<h5 style="color:#bf0000; margin-top:0;">Vue macro (production simulée)</h5>  
                 
Airflow (orchestration)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**↓**    
MLflow (tracking + registry)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**↓**   
FastAPI (serving)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**↓**   
Prometheus (metrics)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**↓**   
Grafana (visualisation)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**↓**   
Streamlit (UI métier)  
  
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
     


###  Architecture globale du système --------------------------------------------------------------------------------------------
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
•	dépend fortement du preprocessing  
                 
**✔ LinearSVC**  
                 
•	très performant en haute dimension  
•	rapide à entraîner  
•	stable en production  
                 
**❌ Limite critique**  
                 
•	pas de predict_proba natif  
                 
**👉 impact direct sur :**  
                 
•	absence de score de confiance  
•	limitation monitoring avancé  
        
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
                 
**❌ Inconvénients**  
                 
•	pipeline complexe à maintenir  
•	debugging difficile  
•	forte dépendance au schéma input  
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
 

<h5 style="color:#bf0000; margin-top:0;">DAG principal</h5>    
                 
•	load  
•	preprocess  
•	train  
•	evaluate  
•	register_model  

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
                 
<h5 style="color:#bf0000; margin-top:0;">Décision clé : séparation stricte des tâches</h5>    
                 
**✔ Avantages**  
                 
•	maintenabilité  
•	testabilité  
•	re-exécution partielle  
                 
**❌ Inconvénients**  
                 
•	overhead orchestration  
•	complexité debugging multi-tâches  
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
                 
<h5 style="color:#bf0000; margin-top:0;">Limite actuelle</h5>    
  
•	stockage intermédiaire local (/tmp)  
                 
**👉 Non scalable (vs S3 / Data Lake)**
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
     
###  Monitoring — Prometheus & Grafana --------------------------------------------------------------------------------------------
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
 

<h5 style="color:#bf0000; margin-top:0;">Métriques suivies</h5>   
                 
•	latence API  
•	taux d’erreur  
•	nombre requêtes  
•	santé conteneurs  
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
               
<h5 style="color:#bf0000; margin-top:0;">Absence de :</h5>  
                 
•	drift data  
•	drift concept  
•	monitoring modèle  

</div>

""", unsafe_allow_html=True) 
     
###  Docker & infrastructure --------------------------------------------------------------------------------------------
    with tabs[6]:
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