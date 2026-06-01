import streamlit as st
from app_streamlit.core.utils import affiche_bandeau

def run():
    affiche_bandeau("Objectif et Contexte")

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
        "🎯\nContexte métier et problématique",
        "🏁\nObjectifs techniques et pédagogiques",
    ])

###  Contexte métier et problématique --------------------------------------------------------------------------------------------
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
 

<h5 style="color:#bf0000; margin-top:0;">Cas d’usage industriel</h5>  
                 
Le projet Rakuten consiste à résoudre un problème réel de classification automatique de produits e-commerce à partir de texte :  
•	designation produit  
•	description produit  
                   
L’objectif est de prédire une catégorie produit parmi plusieurs classes afin de :  
•	automatiser le référencement catalogue  
•	réduire les erreurs humaines de classification  
•	accélérer le time-to-market des produits  
•	standardiser les données e-commerce  
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
                                                 
<h5 style="color:#bf0000; margin-top:0;">Transformation du problème en système MLOps</h5>      
                 
Nous avons volontairement dépassé le cadre “modèle ML” pour construire un système de production simulé, intégrant :  
•	entraînement reproductible  
•	tracking d’expériences  
•	versioning de modèles  
•	API de serving  
•	orchestration des pipelines  
•	conteneurisation  
•	monitoring  
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
                                                
**👉 Le projet est donc conçu comme une mini-plateforme MLOps industrielle.**  
  
</div>
""", unsafe_allow_html=True) 
     



###  Contexte métier et problématique --------------------------------------------------------------------------------------------
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
                 
<h5 style="color:#bf0000; margin-top:0;">Objectif global</h5>    
                 
Construire un système complet répondant aux principes MLOps :  
                  
•	Reproductibilité  
•	Traçabilité  
•	Automatisation  
•	Modularité   
•	Observabilité  
•	Evolutivité  
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
                 
<h5 style="color:#bf0000; margin-top:0;">Lecture par phase</h5>  

<table style="width:100%; margin-top:10px; border-collapse: collapse;">
    <tr>
        <th style="text-align:left; padding:8px;">Phase</th>
        <th style="text-align:left; padding:8px;">Objectif</th>
    </tr>
    <tr><td>Phase 1</td><td>Pipeline ML robuste</td></tr>
    <tr><td>Phase 2</td><td>Tracking & API</td></tr>
    <tr><td>Phase 3</td><td>Orchestration</td></tr>
    <tr><td>Phase 4</td><td>CI/CD & monitoring</td></tr>
    <tr><td>Phase 5</td><td>Interface Streamlit</td></tr>
</table> 
                
</div>
""", unsafe_allow_html=True) 