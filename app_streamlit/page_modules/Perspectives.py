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
        "🚀\nPerspectives d'améliorations",
        "🏗️\n Industrialisation complète (CI/CD)",
        "📊\nMonitoring — Prometheus & Grafana"
    ])

#CI/CD

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
    with tabs[2]:

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
        
    with tabs[0]:
                # ---------------------------------------------------
        # STYLE LOCAL TAB 2
        # ---------------------------------------------------
        st.markdown("""
        <style>
            .main-title {
                font-size: 2.4rem;
                font-weight: 700;
                color: #1F4E79;
                margin-bottom: 0.3rem;
            }

            .subtitle {
                font-size: 1.15rem;
                color: #555;
                margin-bottom: 1.2rem;
            }

            .section-title {
                font-size: 1.55rem;
                font-weight: 650;
                color: #1F4E79;
                margin-top: 2.2rem;
                margin-bottom: 0.8rem;
                border-left: 6px solid #1F4E79;
                padding-left: 0.6rem;
            }

            .box, .roadmap-box {
                padding: 1rem;
                border-radius: 12px;
                background-color: #FFFFFF;
                border: 1px solid #E5E7EB;
                box-shadow: 0 2px 6px rgba(0,0,0,0.06);
            }

            .small-note {
                font-size: 0.95rem;
                color: #666;
                margin-top: 0.5rem;
            }

            ul li {
                margin-bottom: 0.25rem;
                line-height: 1.45;
            }

            .roadmap-box {
                background: linear-gradient(180deg, #FFFFFF 0%, #F7F9FB 100%);
                min-height: 260px;
            }
        </style>
        """, unsafe_allow_html=True)

        # ---------------------------------------------------
        # HEADER
        # ---------------------------------------------------
        st.title("🚀 Perspectives d’amélioration – Projet MLOps Rakuten")

        st.markdown(
            """
            <div class="subtitle">
            Comment faire évoluer notre démonstrateur MLOps vers un système plus industrialisé,
            plus robuste et plus proche d’un contexte de production ?
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info(
            "Cette partie montre non seulement ce qu’il reste à faire, "
            "mais surtout la trajectoire de montée en maturité du projet."
        )

        # ---------------------------------------------------
        # POSITIONNEMENT ACTUEL
        # ---------------------------------------------------
        col_a, col_b, col_c = st.columns(3)

        with col_a:
            st.metric("Niveau actuel", "Démonstrateur MLOps")

        with col_b:
            st.metric("Pipeline industrialisé", "En construction")

        with col_c:
            st.metric("Objectif suivant", "Industrialisation")

        st.caption(
            "Positionnement : démonstrateur MLOps local avec bases solides pour montée en maturité."
        )

        # ---------------------------------------------------
        # SECTION 1
        # ---------------------------------------------------
        st.markdown('<div class="section-title">✅ 1. Ce que nous avons déjà construit</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.success("""
**Socle technique**
- Pipeline NLP validé
- Tracking MLflow
- Model Registry (production)
- API FastAPI
- Docker
- Airflow
""")

        with col2:
            st.success("""
**Qualité logicielle**
- Tests unitaires
- Tests intégration
- Tests E2E
- Mode run_id / version / prod
- Cache modèle
- Auth token simple
""")

        st.markdown(
            '<div class="small-note"><b>Message clé :</b> démonstrateur complet et cohérent.</div>',
            unsafe_allow_html=True
        )

        # ---------------------------------------------------
        # SECTION 2
        # ---------------------------------------------------
        st.markdown('<div class="section-title">🟡 2. Ce qu’il manque pour aller vers une production</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.warning("""
**🔄 Industrialisation**
- CI/CD
- Tests automatisés
- Docker build auto
- Déploiement auto
""")

        with col2:
            st.warning("""
**📊 Observabilité**
- Monitoring API
- Latence
- Logs centralisés
- Alerting
""")

        with col3:
            st.warning("""
**🔐 Infrastructure**
- Secrets management
- Multi-env
- MLflow robuste
- Scalabilité
""")

        st.markdown(
            '<div class="small-note"><b>Message clé :</b> évolution naturelle vers industrialisation.</div>',
            unsafe_allow_html=True
        )

        # ---------------------------------------------------
        # SECTION 3
        # ---------------------------------------------------
        st.markdown('<div class="section-title">🗺️ 3. Roadmap</div>', unsafe_allow_html=True)

        st.info(
            "Progression : démonstrateur → industrialisation → production"
        )

        step1, step2, step3 = st.columns(3)

        with step1:
            st.markdown("""
            <div class="roadmap-box">
            <h4>✅ Démonstrateur</h4>
            <ul>
            <li>ML pipeline</li>
            <li>MLflow</li>
            <li>API</li>
            <li>Docker</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

        with step2:
            st.markdown("""
            <div class="roadmap-box">
            <h4>⚙️ Industrialisation</h4>
            <ul>
            <li>CI/CD</li>
            <li>Tests auto</li>
            <li>Secrets</li>
            <li>Logs</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

        with step3:
            st.markdown("""
            <div class="roadmap-box">
            <h4>🚀 Production</h4>
            <ul>
            <li>Monitoring</li>
            <li>Scalabilité</li>
            <li>Alerting</li>
            <li>Gouvernance</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

        st.progress(70)

        st.caption(
            "Position actuel : base solide prête à industrialisation"
        )

        # ---------------------------------------------------
        # SECTION 4
        # ---------------------------------------------------
        st.markdown('<div class="section-title">🎯 4. Priorités</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            <div class="box">
            <b>Court terme</b><br>
            - CI/CD<br>
            - Secrets<br>
            - Logs<br>
            - Tests
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="box">
            <b>Moyen terme</b><br>
            - Monitoring<br>
            - MLflow robuste<br>
            - Séparation env<br>
            - Scalabilité
            </div>
            """, unsafe_allow_html=True)

        # ---------------------------------------------------
        # SECTION 5
        # ---------------------------------------------------
        st.markdown('<div class="section-title">💬 5. Conclusion</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="box">
        Le projet est déjà un démonstrateur MLOps complet.
        <br><br>
        La prochaine étape logique est l’industrialisation :
        automatisation, monitoring et robustesse.
        </div>
        """, unsafe_allow_html=True)

