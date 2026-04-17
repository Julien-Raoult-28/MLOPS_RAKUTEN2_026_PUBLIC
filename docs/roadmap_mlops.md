Roadmap MLOps — Vision court, moyen et long terme

Projet Rakuten Classification — Version 2

🟦 1. Introduction
Cette roadmap présente l’évolution prévue du projet Rakuten Classification après la Version 2, qui constitue une base stable, testée, sécurisée et industrialisable.

Elle est organisée en 4 phases, correspondant aux niveaux de maturité MLOps :

Stabilisation (court terme)

Industrialisation (moyen terme)

Scalabilité & Observabilité (long terme)

Maturité entreprise (vision avancée)

Chaque phase contient :

les objectifs

les tâches

les bénéfices MLOps

les impacts pour l’équipe

🟩 2. Phase 1 — Stabilisation & Sécurisation (court terme)
🎯 Objectif : renforcer la fiabilité, la sécurité et la qualité du système

🔐 2.1. Sécurisation avancée de l’API
Tâches
Remplacer le token statique par une variable d’environnement

Ajouter un système de rotation de secrets

Préparer l’intégration future de JWT ou OAuth2

Bénéfices
Séparation des secrets et du code

API prête pour un déploiement cloud

Conformité aux bonnes pratiques DevSecOps

🧪 2.2. Couverture de tests étendue
Tâches
Ajouter des tests unitaires pour :

prediction_service

utils.load_model

mapping CSV

CLI Typer (via CliRunner)

tests de performance (latence API)

Bénéfices
Réduction des régressions

Confiance dans les évolutions

Base solide pour CI/CD

❤️ 2.3. Healthchecks & introspection API
Tâches
Créer deux endpoints :

/health → “API OK”

/model-info → version, run_id, date d’entraînement

Bénéfices
Indispensable pour le monitoring

Compatible load balancers / orchestrateurs

Facilite le debug

🧹 2.4. Standardisation du code
Tâches
Ajouter ruff ou flake8

Ajouter black pour le formatage

Typage complet (typing)

Bénéfices
Code propre

Contributions facilitées

Préparation à la CI/CD

🟧 3. Phase 2 — Industrialisation & Automatisation (moyen terme)
🎯 Objectif : rendre le système déployable, scalable et automatisé

🐳 3.1. Dockerisation complète
Tâches
Créer deux images :

rakuten-api

rakuten-cli

Avec :

multi-stage build

image légère (Slim / Alpine)

configuration via variables d’environnement

Bénéfices
Portabilité

Reproductibilité

Déploiement cloud-ready

🔄 3.2. CI/CD (GitHub Actions)
Tâches
Pipeline complet :

tests unitaires

linting

build Docker

push vers registry

déploiement automatique (staging)

Bénéfices
Automatisation de la qualité

Réduction des erreurs humaines

Releases rapides et fiables

📦 3.3. Promotion automatique des modèles
Tâches
Workflow MLflow :

entraînement

évaluation

comparaison automatique

promotion en Staging

validation humaine

promotion en Production

Bénéfices
Gouvernance des modèles

Traçabilité

Processus reproductible

📈 3.4. Monitoring API & modèle
Tâches
logs structurés (JSON)

métriques API (latence, taux d’erreur)

métriques ML (distribution des prédictions)

Bénéfices
Détection des dérives

Alerte en cas d’incident

Observabilité complète

🟦 4. Phase 3 — Scalabilité & Observabilité (long terme)
🎯 Objectif : transformer le projet en plateforme MLOps complète

🧭 4.1. Orchestration (Airflow / Prefect)
Tâches
Automatiser :

ingestion des données

entraînement régulier

évaluation automatique

archivage des modèles

Bénéfices
Pipeline automatisé

Réduction des interventions humaines

Scalabilité

🧠 4.2. Monitoring de dérive (Data & Concept Drift)
Tâches
suivi des distributions

alerte si dérive détectée

déclenchement automatique d’un réentraînement

Bénéfices
Modèle performant dans le temps

Maintenance proactive

🏪 4.3. Feature Store (Feast)
Tâches
Stocker :

features textuelles

embeddings

transformations réutilisables

Bénéfices
Standardisation des features

Réutilisation

Cohérence entre train & predict

🎛️ 4.4. Dashboard métier (Streamlit / Gradio)
Tâches
Interface pour :

tester le modèle

visualiser les prédictions

afficher les métriques

explorer les runs MLflow

Bénéfices
Accessibilité pour les équipes non techniques

Communication facilitée

🟪 5. Phase 4 — Vision long terme : MLOps niveau entreprise
🎯 Objectif : atteindre un niveau de maturité MLOps avancé

🔄 5.1. Continuous Training (CT)
Tâches
réentraînement automatique basé sur la dérive

validation automatique

promotion automatique

Bénéfices
Modèle toujours à jour

Automatisation complète

🚀 5.2. Continuous Deployment (CD)
Tâches
déploiement automatique de l’API

blue/green deployment

canary release

Bénéfices
Zéro interruption

Déploiements sûrs

🧩 5.3. Microservices ML
Tâches
Découper :

API prédiction

API modèle

API monitoring

API données

Bénéfices
Scalabilité

Résilience

Maintenance facilitée

☁️ 5.4. Déploiement Cloud
Tâches
Azure ML

AWS Sagemaker

GCP Vertex AI

Bénéfices
Scalabilité infinie

Infrastructure managée

Monitoring intégré

🟫 6. Synthèse — Vision MLOps globale
Phase	Objectif	Livrables
1. Stabilisation	Fiabilité & sécurité	tests, healthchecks, validation stricte
2. Industrialisation	Automatisation	Docker, CI/CD, promotion modèles
3. Scalabilité	Observabilité & orchestration	Airflow, monitoring, dérive
4. Maturité entreprise	CT/CD, cloud	déploiement avancé, microservices

🟦 7. Conclusion
Cette roadmap montre que :

la V2 est une base stable, sécurisée, versionnée

l’équipe a posé les fondations d’un vrai système MLOps

les prochaines phases sont claires, réalistes et progressives

chaque étape a un intérêt métier, technique et opérationnel

Ce document sert de boussole pour guider l’évolution du projet.

