import mlflow

# 1. Tracking URI (doit être sqlite pour activer le Model Registry)
mlflow.set_tracking_uri("sqlite:///mlflow.db")

# 2. Paramètres
run_id = "3cd771b4830740bf823fce572cea2e84"
model_name = "rakuten_classifier"

# 3. URI du modèle dans le run
model_uri = f"runs:/{run_id}/model"

print(">>> Enregistrement du modèle dans le Model Registry...")
result = mlflow.register_model(model_uri=model_uri, name=model_name)

version = result.version
print(f">>> Modèle enregistré : version {version}")

# 4. Promotion en Production
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name=model_name,
    version=version,
    stage="Production"
)

print(f">>> Modèle promu en stage 'Production' (version {version})")
