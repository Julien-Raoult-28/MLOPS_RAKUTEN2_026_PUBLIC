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
        "📊\nMonitoring — Prometheus & Grafana",
        "🚀\nPerspectives d'améliorations"
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
        
    with tabs[2]:
    # ---------------------------------------------------
    # STYLE PERSONNALISÉ
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
            font-size: 1.45rem;
            font-weight: 600;
            color: #1F4E79;
            margin-top: 1.8rem;
            margin-bottom: 0.6rem;
        }
        .box {
            padding: 1rem;
            border-radius: 12px;
            background-color: #F8F9FA;
            border: 1px solid #E5E7EB;
            margin-bottom: 1rem;
        }
        .small-note {
            font-size: 0.95rem;
            color: #666;
            margin-top: 0.5rem;
        }
        .roadmap-box {
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid #D9D9D9;
            background-color: #FFFFFF;
            min-height: 260px;
        }
    </style>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------
    # HEADER
    # ---------------------------------------------------
        st.title(":rocket: Perspectives d’amélioration – Projet MLOps Rakuten")

        st.markdown(
        """
        <div class="subtitle">
        Comment faire évoluer notre démonstrateur MLOps vers un système plus industrialisé,
        plus robuste et plus proche d’un contexte de production ?
        </div>
        """,
        unsafe_allow_html=True
    )

        st.info("""
    Cette partie montre non seulement ce qu’il reste à faire, mais surtout la trajectoire
    de montée en maturité du projet.
    """)

    # ---------------------------------------------------
    # POSITIONNEMENT ACTUEL
    # ---------------------------------------------------
    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.metric("Niveau actuel", "Démonstrateur MLOps")
    with col_b:
        st.metric("Pipeline industrialisé", "Texte")
    with col_c:
        st.metric("Objectif suivant", "Industrialisation")

        st.caption(
        "Positionnement retenu : démonstrateur MLOps avancé en environnement local, "
        "avec bases solides pour une montée en maturité."
    )

    # ---------------------------------------------------
    # SECTION 1 - CE QUI EST DÉJÀ FAIT
    # ---------------------------------------------------
    st.markdown(
        '<div class="section-title">✔️ 1. Ce que nous avons déjà construit</div>',
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.success("""
**Socle technique déjà en place**
- Pipeline texte validé
- Tracking MLflow
- Model Registry avec alias `production`
- API FastAPI pour l’inférence
- Environnement Docker reproductible
- Orchestration avec Airflow
""")

    with col2:
        st.success("""
**Qualité logicielle déjà mise en œuvre**
- Tests unitaires
- Tests d’intégration
- Tests end-to-end
- Mode hybride `run_id / version / production`
- Cache mémoire des modèles
- Contrôle d’accès simple par token
""")

    st.markdown(
        '<div class="small-note"><b>Message clé :</b> nous disposons déjà d’un démonstrateur MLOps complet, cohérent et démontrable en environnement local.</div>',
        unsafe_allow_html=True
    )

    # ---------------------------------------------------
    # SECTION 2 - CE QUI MANQUE ENCORE
    # ---------------------------------------------------
    st.markdown(
        '<div class="section-title">🟡 2. Ce qu’il manque pour aller vers une production plus mature</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.warning("""
**Industrialisation**
- CI/CD
- automatisation complète des tests
- build automatique des images
- déploiement automatisé
""")

    with col2:
        st.warning("""
**Observabilité**
- monitoring de l’API
- suivi des latences
- suivi des erreurs
- alertes
- logs centralisés
""")

    with col3:
        st.warning("""
**Sécurité & infrastructure**
- gestion industrielle des secrets
- configuration multi-environnements
- backend MLflow plus robuste
- meilleure montée en charge
""")

    st.markdown(
        '<div class="small-note"><b>Message clé :</b> les briques manquantes sont clairement identifiées ; elles relèvent d’une montée en maturité et non d’un changement de direction technique.</div>',
        unsafe_allow_html=True
    )

    # ---------------------------------------------------
    # SECTION 3 - ROADMAP
    # ---------------------------------------------------
    st.markdown(
        '<div class="section-title">🌍 3. Roadmap d’évolution</div>',
        unsafe_allow_html=True
    )

    st.write("Nous pouvons représenter l’évolution du projet en **trois étapes de maturité MLOps** :")

    st.info(
        "Cette roadmap illustre une progression réaliste : partir d’un démonstrateur local stable, "
        "puis renforcer l’automatisation, l’observabilité et la robustesse."
    )

    step1, step2, step3 = st.columns(3)

    with step1:
        st.markdown("""
        <div class="roadmap-box">
        <h4>:✅ Étape 1 — Démonstrateur</h4>
        <ul>
        <li>modèle texte validé</li>
        <li>tracking MLflow</li>
        <li>registry</li>
        <li>API FastAPI</li>
        <li>tests</li>
        <li>Docker</li>
        <li>Airflow</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with step2:
        st.markdown("""
        <div class="roadmap-box">
        <h4>🟡 Étape 2 — Industrialisation</h4>
        <ul>
        <li>CI/CD</li>
        <li>gestion des secrets</li>
        <li>standardisation des environnements</li>
        <li>logs plus structurés</li>
        <li>durcissement applicatif</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    with step3:
        st.markdown("""
        <div class="roadmap-box">
        <h4>🚀 Étape 3 — Production</h4>
        <ul>
        <li>monitoring & alerting</li>
        <li>infrastructure plus scalable</li>
        <li>gouvernance de versions</li>
        <li>observabilité complète</li>
        <li>extension vers d’autres modèles</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)

    st.progress(70)

    st.caption(
        "Positionnement actuel estimé : démonstrateur MLOps avancé, avec fondations solides pour aller vers l’industrialisation."
    )

    # ---------------------------------------------------
    # SECTION 4 - PRIORITÉS
    # ---------------------------------------------------
    st.markdown(
        '<div class="section-title">🎯 4. Priorités recommandées</div>',
        unsafe_allow_html=True
    )

    priority1, priority2 = st.columns(2)

    with priority1:
        st.markdown("""
        <div class="box">
        <b>Priorités court terme</b><br><br>
        1. Automatiser les tests via une CI/CD<br>
        2. Externaliser les secrets<br>
        3. Structurer les logs applicatifs<br>
        4. Consolider la visibilité des métriques MLflow
        </div>
        """, unsafe_allow_html=True)

    with priority2:
        st.markdown("""
        <div class="box">
        <b>Priorités moyen terme</b><br><br>
        1. Ajouter monitoring et alertes<br>
        2. Renforcer l’infrastructure MLflow<br>
        3. Préparer une séparation dev / test / prod<br>
        4. Étendre le périmètre si besoin
        </div>
        """, unsafe_allow_html=True)

    # ---------------------------------------------------
    # SECTION 5 - MESSAGE FINAL JURY
    # ---------------------------------------------------
    st.markdown(
        '<div class="section-title">💬 5. Message final pour le jury</div>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="box">
    Notre objectif n’était pas de tout faire en une seule étape, mais de poser des bases MLOps solides :
    un modèle versionné, exploitable, testé et orchestré.
    <br><br>
    La suite logique du projet consiste maintenant à renforcer l’automatisation, l’observabilité et la sécurité
    afin de transformer ce démonstrateur local en une plateforme plus mature.
    </div>
    """, unsafe_allow_html=True)

    # ---------------------------------------------------
    # SECTION 6 - FORMULATIONS ORALES
    # ---------------------------------------------------
    st.markdown(
        '<div class="section-title">🎤 6. Formulations orales possibles</div>',
        unsafe_allow_html=True
    )

    st.code(
        """1. "Nous avons construit les fondations MLOps du projet."
2. "La prochaine étape n’est plus la faisabilité, mais la montée en maturité."
3. "Nous savons précisément ce qu’il manque pour aller vers une production plus robuste."
4. "Notre démonstrateur local est déjà structuré ; l’enjeu suivant est l’industrialisation."
5. "Notre objectif n’était pas de tout faire, mais de poser les bonnes bases."
""",
        language="text"
    )

    # ---------------------------------------------------
    # SECTION 7 - CONCLUSION
    # ---------------------------------------------------
    st.markdown(
        '<div class="section-title">✅ 7. Conclusion</div>',
        unsafe_allow_html=True
    )

    st.success(
        "Le projet est déjà à un bon niveau de maturité pour un démonstrateur MLOps local. "
        "Les perspectives identifiées permettent de montrer une trajectoire crédible vers une solution plus industrialisée."
    )