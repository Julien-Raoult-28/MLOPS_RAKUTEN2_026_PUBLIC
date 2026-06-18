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
Cette architecture illustre comment les briques MLOps s’articulent pour transformer un pipeline de Machine Learning en système exploitable. 
                    
  
  
                    
                    
<div style="text-align:center;margin-bottom:50px;"><img src="data:image/png;base64,{encoded}" style="width:100%; object-fit:contain;"/></div>  
  
**Vue d’ensemble**  
  
•	Une seule machine locale orchestrant trois services : Airflow, MLflow et FastAPI.  
•	Communication interne via le réseau `mlops-net`.  
•	Persistance des artefacts et métadonnées dans le volume `mlflow-data`.  
•	Chaque service est conteneurisé et isolé dans Docker.  
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
                                     
                 
**Flux de données**  
       
•	1. Airflow orchestre le pipeline d’entraînement (load → preprocess → train → evaluate → register).   
•	2. MLflow trace les runs, stocke les artefacts et gère le Model Registry.  
•	3. FastAPI recharge dynamiquement la version active du modèle via l’alias `production`.  
•	4. Le client interagit avec l’API pour obtenir des prédictions en temps réel.  
 
  
👉 Airflow et FastAPI ne communiquent jamais directement : leur point de contact unique est MLflow, garant de la cohérence entre expérimentation et exploitation.                
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
  
Le modèle retenu est un SVM linéaire (LinearSVC) entraîné sur des représentations TF-IDF mots et caractères.  
                                 
Nous sommes reparti avec notre modèle du projet DS qui avait obtenu un score de 87% sur le challenge Rakuten.

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
        import base64
        with open("app_streamlit/assets/images/MLFLOW.png", "rb") as img_file:
                img_bytes = img_file.read()
                encoded2 = base64.b64encode(img_bytes).decode()
        st.markdown(f"""
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
<h5 style="color:#bf0000; margin-top:0;">MLflow, la mémoire du projet</h5>   
  
Quand on entraîne plusieurs versions d'un modèle, une question revient : « laquelle est la meilleure, et laquelle est en production ? »  
Sans outil, la réponse se perd. MLflow enregistre automatiquement chaque entraînement et son résultat, et garde tout au même endroit, consultable.  
  
•	On retrouve d'un coup d'œil quelle version a donné le meilleur score.  
•	Plus de fichiers modele_final_v2_vraiment_final.pkl.  

<div style="text-align:center;margin-bottom:50px;"><img src="data:image/png;base64,{encoded2}" style="width:100%; object-fit:contain;"/></div>                              
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
<h5 style="color:#bf0000; margin-top:0;">Du modèle entraîné au modèle servi</h5>          
  
MLflow ne fait pas que noter les résultats : il gère les versions du modèle  
Entraînement  →  version enregistrée (v1, v2, v3…)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;promue en « Production »  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;↓  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;l'API utilise cette version   
  
**Le point clé : l'API ne pointe jamais vers un fichier en dur.**   
Elle demande simplement « le modèle en Production ».   
Changer de modèle = promouvoir une nouvelle version dans MLflow, **sans toucher au code de l'API.**
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
                 
**Compromis**  
                 
Complexité supplémentaire mais gain important en industrialisation et en reproductibilité.  
</div>


""", unsafe_allow_html=True) 
     
###  FastAPI — serving ML --------------------------------------------------------------------------------------------
    with tabs[4]:
        import base64
        with open("app_streamlit/assets/images/api.png", "rb") as img_file:
                img_bytes = img_file.read()
                encoded3 = base64.b64encode(img_bytes).decode()
        st.markdown(f"""
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
                 
<h5 style="color:#bf0000; margin-top:0;text-align:center;">Schéma FastAPI MLOps Rakuten</h5>  
                    
<div style="text-align:center;margin-bottom:50px;"><img src="data:image/png;base64,{encoded3}" style="width:100%; object-fit:contain;"/></div> 

FastAPI est la brique qui rend le modèle réellement exploitable.  
Elle relie le registre de modèles MLflow à l’usage métier, en servant les prédictions en temps réel.  
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
                 

<div style="margin-top:20px;background-color:#e8f2ff; padding:15px; border-left:4px solid #bf0000; border-radius:5px;">
    <strong>L’objectif : offrir une API claire, rapide et traçable, capable de servir n’importe quelle version du modèle selon le besoin.</strong>
</div>

<table style="width:100%; margin-top:10px; border-collapse: collapse;background-color:white;">
    <tr>
        <th style="text-align:center; padding:8px;">Endpoints principaux</th>
        <th style="text-align:center; padding:8px;">Mode hybride de chargement</th>
    </tr>
    <tr>
        <td style="text-align:left;"><strong>/</strong> : healthcheck</td>
        <td style="text-align:left;"> Si un `run_id` est fourni → recharge le modèle exact du run</td>
    </tr>
    <tr>
        <td style="text-align:left;"><strong>/models</strong> : liste des versions disponibles</td>
        <td style="text-align:left;">Si une `model_version` est précisée → charge cette version spécifique</td>
    </tr>
    <tr>
        <td style="text-align:left;"><strong>/predict</strong> : prédiction en temps réel</td>
        <td style="text-align:left;">Sinon → utilise la version pointée par l’alias `production`</td>
    </tr>
    <tr>
        <td style="text-align:left;"><strong>Chaque endpoint est documenté via Swagger et testé automatiquement. </strong></td>
        <td style="text-align:left;"><strong>Ce mode garantit une traçabilité complète entre expérimentation et exploitation.</strong></td>
    </tr>
</table> 
                 
**Exemple de réponse JSON** :  
<pre><code>{{
"code": "C123",  
"libelle": "Accessoires audio",  
"version": "v2",  
"run_id": "a1b2c3",  
"latence_ms": 12.4,  
"timestamp": "2026-06-17T17:05:00"  
}}</code></pre>
   
  
**✅ Cette API n’est pas un simple wrapper : elle incarne la séparation entre entraînement et exploitation, avec un service versionné, testé et documenté.**
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
<h5 style="color:#bf0000; margin-top:0;">Pourquoi Docker</h5> 
                 
Le problème classique — « ça marche sur ma machine » — disparaît avec Docker : l'environnement complet (système, dépendances, versions) est **figé dans une image reproductible** qui tourne à l'identique partout.  
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
                 
<h5 style="color:#bf0000; margin-top:0;">Plusieurs services qui coopèrent</h5> 

Le projet n'est pas un seul conteneur, mais **plusieurs services coordonnés** par `docker-compose` :
                               

<table style="width:100%; margin-top:10px; border-collapse: collapse;">
    <tr>
        <th style="text-align:center; padding:8px;">Service</th>
        <th style="text-align:center; padding:8px;">Rôle</th>
    </tr>
    <tr>
        <td style="text-align:center;">AIRFLOW</td>
        <td style="text-align:center;">Automatise le pipeline</td>
    </tr>
    <tr>
        <td style="text-align:center;">MLFLOW</td>
        <td style="text-align:center;">Suit les essais et stocke les versions</td>
    </tr>
    <tr>
        <td style="text-align:center;">API</td>
        <td style="text-align:center;">Sert le modèle (FastAPI)</td>
    </tr>
</table> 
                 
**Une seule commande lance tout** : `docker-compose up`. Aucune installation Python requise pour faire tourner la chaîne.

</div>
""", unsafe_allow_html=True) 