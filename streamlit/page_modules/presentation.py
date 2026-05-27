import streamlit as st
from core.utils import affiche_bandeau

def run():
    affiche_bandeau("Présentation du projet")

    st.write("Contenu de la page présentation...")
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
        "🏢\nContexte Rakuten",
        "🏁\nObjectif du projet",
        "💼\nContexte métier",
        "⚙️\nContexte technique",
        "💶\nContexte économique",
        "🔬\nContexte scientifique"
    ])
  
###  Contexte Rakuten --------------------------------------------------------------------------------------------
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
 

Rakuten est un des plus grands acteurs mondiaux du e-commerce, créé en 1997, 
avec plus de **1,3 milliard d’utilisateurs** dans son écosystème international.  
                
Le **Rakuten Institute of Technology (RIT)** mène des recherches en apprentissage automatique,
vision par ordinateur, NLP et HCI, avec des équipes à Tokyo, Paris, Boston, Singapour et Bengaluru.  
</div>
""", unsafe_allow_html=True)    
          
### Objectif du projet  ------------------------------------------------------------------------------------------------
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
                       
Créer un modèle capable de **classer automatiquement les produits** du catalogue Rakuten France
dans leur code type produit (prdtypecode), en utilisant du texte (titre, description) et/ou des images.
C’est un problème de **classification à grande échelle**.  
                
L'objectif est d'obtenir un F1-score supérieur à **0,8113 sur les données textuelles**.  
Pour les **images**, l'objectif est d'atteindre un F1-score supérieur à **0,5534**.  
</div>
""", unsafe_allow_html=True)    
            
### Contexte métier  ------------------------------------------------------------------------------------------------
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
                  
Le challenge Rakuten vise à automatiser la classification de produits e‑commerce à partir
d’images et de descriptions textuelles.  
                
**Dans un contexte opérationnel, cette automatisation permet :**  

<ul style="list-style: none; padding-left: 0;">                          
<li><span style="color:#bf0000; font-size:18px;">⬥</span> D’accélérer la mise en ligne des produits.  
<li><span style="color:#bf0000; font-size:18px;">⬥</span> De réduire les erreurs de catégorisation.  
<li><span style="color:#bf0000; font-size:18px;">⬥</span> D’améliorer la qualité des listings.  
<li><span style="color:#bf0000; font-size:18px;">⬥</span> D’optimiser le référencement interne et la navigation client.   
</ul>
</div>
""", unsafe_allow_html=True) 
               
### Contexte technique------------------------------------------------------------------------------------------------
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
                   
<strong>Le projet repose sur :</strong>  
           
<ul style="list-style: none; padding-left: 0;">                          
<li><span style="color:#bf0000; font-size:18px;">⬥</span> Un dataset de <strong>84 916 annonces et images</strong>.  
<li><span style="color:#bf0000; font-size:18px;">⬥</span> Une variable cible (prdtypecode) comportant <strong>27 classes déséquilibrées</strong>.  
<li><span style="color:#bf0000; font-size:18px;">⬥</span> Des descriptions textuelles de longueur très variable (de 0 à 12 451 caractères),
incluant des balises HTML, des langues multiples et des stopwords, ce qui
complexifie leur traitement direct.  
<li><span style="color:#bf0000; font-size:18px;">⬥</span> Des images hétérogènes souvent bruitées, floues ou sombres.  
<li><span style="color:#bf0000; font-size:18px;">⬥</span> Un environnement limité ( <strong>CPU 4 cœurs, pas de GPU</strong>), nécessitant des solutions
optimisées pour garantir des performances élevées malgré les ressources restreintes.  
</ul>
</div>
""", unsafe_allow_html=True) 
               
### Contexte économique  ------------------------------------------------------------------------------------------------
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
                    
**La catégorisation manuelle est coûteuse :**  
           
<ul style="list-style: none; padding-left: 0;">                          
<li><span style="color:#bf0000; font-size:18px;">⬥</span><strong>Charge humaine</strong> : Processus chronophage nécessitant une intervention manuelle
pour chaque produit.  
<li><span style="color:#bf0000; font-size:18px;">⬥</span><strong>Risque d’erreur</strong> : Taux d’erreur élevé en raison de la subjectivité et de la complexité
des 27 classes.  
<li><span style="color:#bf0000; font-size:18px;">⬥</span><strong>Impact direct</strong> : Les erreurs de catégorisation réduisent la visibilité des produits,
affectant la conversion et la satisfaction client.  
</ul>
</div>
""", unsafe_allow_html=True) 
    
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
                      
**Un modèle performant permet de :**  
           
<ul style="list-style: none; padding-left: 0;">                          
<li><span style="color:#bf0000; font-size:18px;">⬥</span> Réduire les coûts opérationnels liés à la catégorisation manuelle.  
<li><span style="color:#bf0000; font-size:18px;">⬥</span> Améliorer la qualité et la cohérence des listings.  
<li><span style="color:#bf0000; font-size:18px;">⬥</span> Augmenter le taux de conversion grâce à un référencement interne optimisé.  
<li><span style="color:#bf0000; font-size:18px;">⬥</span> Offrir une meilleure expérience utilisateur via une navigation intuitive.  
</ul> 
</div>
""", unsafe_allow_html=True)  
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
                                    
**Bénéfices d’un modèle automatisé :**  
           
<ul style="list-style: none; padding-left: 0;">                          
<li><span style="color:#bf0000; font-size:18px;">⬥</span> Gain de temps significatif : Réduction du temps de traitement.  
<li><span style="color:#bf0000; font-size:18px;">⬥</span> Réallocation des ressources : Les équipes peuvent se concentrer sur des tâches
à plus forte valeur ajoutée (ex : optimisation des fiches produits, stratégie marketing).  
<li><span style="color:#bf0000; font-size:18px;">⬥</span> Réduction des coûts opérationnels : Moins d’heures consacrées à la
catégorisation manuelle et aux corrections.  
<li><span style="color:#bf0000; font-size:18px;">⬥</span> Amélioration de la réactivité : Mise en ligne plus rapide des nouveaux produits,
ce qui booste la compétitivité et la satisfaction client.  
</ul>
</div>
""", unsafe_allow_html=True) 
    
### Contexte scientifique------------------------------------------------------------------------------------------------
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
                 
**Le projet s’inscrit dans plusieurs domaines clés du machine learning et de la data science :**  
           
<ul style="list-style: none; padding-left: 0;">                          
<li><span style="color:#bf0000; font-size:18px;">⬥</span><strong>Vision par ordinateur</strong> : pour analyser des images hétérogènes et extraire des
features visuelles robustes.  
<li><span style="color:#bf0000; font-size:18px;">⬥</span><strong> Transfer learning</strong> : pour adapter des modèles pré-entraînés (ex : MobileNetV2) aux
contraintes du projet (27 classes, pas de GPU).  
<li><span style="color:#bf0000; font-size:18px;">⬥</span><strong> Détection d’outliers</strong> : pour identifier et écarter les images inutilisables (floues,
sombres, mal cadrées) et les doublons, améliorant ainsi la qualité du dataset.  
<li><span style="color:#bf0000; font-size:18px;">⬥</span><strong> Analyse de qualité d’images</strong>.  
<li><span style="color:#bf0000; font-size:18px;">⬥</span><strong> Classification supervisée multiclasse</strong> : pour prédire la catégorie produit avec une
métrique adaptée au déséquilibre des classes (F1-score pondéré).  
</ul>
</div>
""", unsafe_allow_html=True) 