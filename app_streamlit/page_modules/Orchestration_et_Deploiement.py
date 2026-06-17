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

<div style="text-align:center;margin-bottom:50px;"><img src="data:image/png;base64,{encoded}" style="width:100%; object-fit:contain;"/></div>  
 
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
                                 
<h5 style="color:#bf0000; margin-top:0;">D'un programme Python à un vrai système</h5>     
                 
**Au départ** : un programme Python lancé à la main qui entraîne un modèle et s'arrête là. Ça marche, mais ce n'est ni traçable, ni automatisé, ni déployable.  
  
**Objectif du projet** : transformer ce programme en chaîne MLOps.  

**AVANT / APRÈS** :      
•	Lancement Script lancé à la main  
•	Pipeline automatisé (Airflow)  
•	Suivi des essais  
•	Aucun Historique centralisé (MLflow)  
•	Mise à disposition  
•	Le modèle reste sur la machine  
•	Modèle exposé en API (FastAPI)  
•	Environnement  
  
**« Ça marche chez moi » Identique partout (Docker)**                
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
                                 
<h5 style="color:#bf0000; margin-top:0;">Les 4 briques, et pourquoi</h5>    
  
•	**Airflow** — automatise les étapes et permet de les relancer sans tout reprendre.  
•	**MLflow** — garde la mémoire des essais et gère les versions du modèle.  
•	**FastAPI** — rend le modèle interrogeable par un simple appel.  
•	**Docker** — garantit que tout tourne à l'identique, partout.  

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
                 
<h5 style="color:#bf0000; margin-top:0;">Rendre le modèle utilisable</h5> 

Un modèle n'a de valeur que s'il est **interrogeable**. L'API est la porte d'entrée : on lui envoie un texte produit, elle renvoie une catégorie.  
On utilise FastAPI, qui apporte :  
  
•	la **vérification automatique** des données reçues,
•	une **documentation interactive** générée toute seule (/docs),
•	de bonnes **performances**.                
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
                 
<h5 style="color:#bf0000; margin-top:0;">Les points d'accès</h5> 
  
<table style="width:100%; margin-top:10px; border-collapse: collapse;">
    <tr>
        <th style="text-align:center; padding:8px;">Méthode</th>
        <th style="text-align:center; padding:8px;">Adresse</th>
        <th style="text-align:center; padding:8px;">Rôle</th>
    </tr>
    <tr>
        <td style="text-align:center;">GET</td>
        <td style="text-align:center;">/</td>
        <td style="text-align:center;">Vérifie que le service répond</td>
    </tr>
    <tr>
        <td style="text-align:center;">GET</td>
        <td style="text-align:center;">/models</td>
        <td style="text-align:center;">affiche la liste des modèles disponibles</td>
    </tr>
    <tr>
        <td style="text-align:center;">GETtd>
        <td style="text-align:center;">/predict</td>
        <td style="text-align:center;">Renvoie la catégorie d'un produit</td>
    </tr>
</table> 

**Exemple d'appel** (POST /predict) :  
json  
<pre><code>{  
  "designation": "Coque silicone iPhone 13 transparente",  
  "description": "Protection antichoc, compatible recharge sans fil"  
}</code></pre>  
                 
**Réponse** :    
json   
<pre><code>{  
  "prediction_code": 1280,  
  "confidence": 0.94,  
  "model_version": "4"  
}</code></pre>               

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
                 
<h5 style="color:#bf0000; margin-top:0;">Un modèle toujours à jour</h5> 
                  
L'API **ne contient aucun modèle en dur**. Au démarrage, elle récupère depuis MLflow la version marquée « Production ».

•	Déployer un nouveau modèle = le promouvoir dans MLflow. Rien à redéployer côté API.
•	Le champ `model_version` dans chaque réponse assure la traçabilité : on sait toujours quel modèle a produit quelle prédiction.

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