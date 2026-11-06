import mlflow
TRACKING_URI = 'sqlite:///mlflow.db'
def configure_mlflow():
    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment('Diabetes_Prediction_Experiments')
