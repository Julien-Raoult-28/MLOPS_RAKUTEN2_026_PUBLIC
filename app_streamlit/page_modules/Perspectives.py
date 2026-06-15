import streamlit as st
from app_streamlit.core.utils import affiche_bandeau

def run():
    affiche_bandeau("Perspectives")

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
        "🏗️\n Industrialisation complète (CI/CD)",
        "📊\nMonitoring — Prometheus & Grafana"
    ])

#CI/CD

    with tabs[0]: 
     
        st.markdown("""
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI';
    width:85%;
">

<h4 style="color:#bf0000;text-align:center;">CI/CD & automatisation (perspective)</h4>

<h5 style="color:#bf0000;">État actuel</h5>

• Déploiement manuel des services  
• Exécution locale ou via Docker  
• Validation humaine des changements  

</div>


<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI';
    width:85%;
">

<h5 style="color:#bf0000;">Évolution envisagée : CI/CD complet</h5>

Pipeline cible :

• Push GitHub  
• Tests automatiques (unitaires + API)  
• Build Docker  
• Validation qualité modèle  
• Déploiement automatique  

</div>


<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI';
    width:85%;
">

<h5 style="color:#bf0000;">Bénéfices MLOps</h5>

• réduction des erreurs humaines  
• déploiement reproductible  
• gain de temps important  
• standard industriel  

<h5 style="color:#bf0000;">Trade-off</h5>

• complexité initiale élevée  
• mise en place d’infrastructure supplémentaire  

</div>
""", unsafe_allow_html=True)
 #  Monitoring (Prometheus / Grafana)     
    with tabs[1]:

        st.markdown("""
<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI';
    width:85%;
">

<h4 style="color:#bf0000;text-align:center;">Monitoring & observabilité (perspective)</h4>

<h5 style="color:#bf0000;">État actuel</h5>

• Logs applicatifs  
• Tracking MLflow des métriques offline  
• Pas de monitoring temps réel  

</div>


<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI';
    width:85%;
">

<h5 style="color:#bf0000;">Évolution envisagée</h5>

Intégration :

• Prometheus → collecte métriques API  
• Grafana → dashboards temps réel  

Métriques ciblées :

• latence API  
• taux d’erreur  
• volume de requêtes  
• dérive des prédictions  
• consommation ressources  

</div>


<div style="
    background: linear-gradient(135deg, #fdfdfd, #f0f0f0);
    padding:20px;
    border-left:6px solid #bf0000;
    border-radius:15px;
    margin: 20px auto;
    box-shadow: 0 8px 20px rgba(0,0,0,0.1);
    font-family: 'Segoe UI';
    width:85%;
">

<h5 style="color:#bf0000;">Valeur ajoutée</h5>

• détection rapide de dérive modèle  
• supervision production  
• meilleure fiabilité système  

<h5 style="color:#bf0000;">Limite actuelle</h5>

• absence de monitoring en continu  
• pas d’alerting automatique  

</div>
""", unsafe_allow_html=True)
        

