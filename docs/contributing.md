🤝 Guide de contribution — Projet MLOps Rakuten (Version 2)
Bienvenue dans le projet Rakuten Classification !
Ce document explique pas à pas comment contribuer au code sans casser la V2.

Il complète le guide pédagogique, qui lui explique comment utiliser le projet.

🟦 1. Prérequis
Avant de contribuer, vous devez savoir :

utiliser Git au minimum (clone, add, commit, push)

lancer les tests avec pytest

lancer l’API FastAPI

comprendre la structure du projet (voir guide pédagogique)

Si ce n’est pas le cas → lisez d’abord le guide pédagogique.

🟩 2. Règles d’or (à lire absolument)
NE JAMAIS travailler directement sur main

TOUJOURS créer une branche pour chaque modification

TOUJOURS lancer les tests avant de pousser

TOUJOURS faire une Pull Request (PR)

NE JAMAIS modifier mlflow.db ou mlruns/

TOUJOURS mettre à jour le CHANGELOG

NE PAS supprimer ou modifier la V2 sans validation

🟧 3. Comment contribuer (pas à pas)
3.1. Cloner le projet
bash
git clone <URL_DU_REPO>
cd FEV26-CMLOPS-RAKUTEN
3.2. Créer une branche
Chaque contribution doit être faite dans une branche dédiée.

🔧 Nommage obligatoire :
Code
feature/<nom-tache>
fix/<nom-bug>
docs/<nom-doc>
tests/<nom-test>
Exemples :
Code
feature/ajout-endpoint-health
fix/correction-token
docs/ajout-guide-api
tests/test-prediction-service
Créer la branche :

bash
git checkout -b feature/ma-tache
🟦 4. Faire des modifications
Modifiez uniquement :

src/ → code API / modèle / utils

tests/ → tests unitaires / intégration / E2E

docs/ → documentation pédagogique

README.md → documentation professionnelle

CHANGELOG.md → résumé des changements

⚠️ Ne jamais modifier :

mlflow.db

mlruns/

fichiers générés automatiquement

🟩 5. Lancer les tests avant de pousser
Toujours vérifier que tout fonctionne :

bash
pytest -v
Si un test échoue → corrigez avant de pousser.

🟧 6. Commit propre
Un commit doit être clair, court et explicite.

Format obligatoire :
Code
feat: description
fix: description
docs: description
test: description
refactor: description
Exemples :
Code
feat: ajout endpoint /health
fix: correction du chargement du modèle MLflow
docs: ajout section API dans README
test: ajout tests E2E pour /predict
🟦 7. Pousser la branche
bash
git push origin feature/ma-tache
🟩 8. Créer une Pull Request (PR)
Sur GitHub :

Aller dans Pull Requests

Cliquer New Pull Request

Base : main

Compare : votre branche

Titre clair (ex : “feat: ajout endpoint /health”)

Description :

ce que vous avez fait

pourquoi

tests effectués

🟧 9. Validation de la PR
Une PR doit être :

relue

validée

testée

fusionnée proprement

⚠️ Ne jamais merger sans validation.

🟦 10. Mise à jour du CHANGELOG
Chaque PR doit ajouter une ligne dans :

Code
CHANGELOG.md
Exemple :

Code
## [2.1.0] - 2026-04-17
### Added
- Ajout endpoint /health
🟩 11. Bonnes pratiques de code
respecter PEP8

utiliser des noms explicites

ajouter des docstrings

ne pas laisser de code mort

ne pas laisser de prints

utiliser logging si nécessaire

garder les fonctions courtes et claires

🟧 12. Bonnes pratiques MLOps
ne jamais versionner les artefacts MLflow

ne jamais modifier un modèle Production sans validation

toujours tester un modèle en Staging avant promotion

toujours documenter les changements de modèle

🟦 13. En cas de doute
Avant de pousser, demandez :

“Est‑ce que ma modification casse la V2 ?”

“Est‑ce que j’ai lancé les tests ?”

“Est‑ce que j’ai mis à jour le changelog ?”

“Est‑ce que j’ai créé une branche propre ?”

Si vous ne savez pas → demandez à l’équipe.

🟩 14. Merci !
Merci de contribuer au projet Rakuten Classification !
Votre travail aide à maintenir un pipeline MLOps propre, stable et professionnel.