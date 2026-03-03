import torch
from django.apps import AppConfig

from Backend_URL_Analyzer.URL_model.model import Phishign_URL_CNN
from Backend_URL_Analyzer.URL_model.predict import MODEL_PATH


class BackendUrlAnalyzerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Backend_URL_Analyzer'

    def ready(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model = Phishign_URL_CNN.load_from_checkpoint(MODEL_PATH)
        model.to(device).eval()
