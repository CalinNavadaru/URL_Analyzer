import torch
from .processing import process_url
from .model import Phishign_URL_CNN

MODEL_PATH = "Backend_URL_Analyzer/URL_model/best-phishing-url.ckpt"
device = "cuda" if torch.cuda.is_available() else "cpu"
model = Phishign_URL_CNN.load_from_checkpoint(MODEL_PATH)
model.to(device).eval()

def predict(url: str) -> str:
    processed_url = process_url(url)
    url_tok = torch.tensor(processed_url).to(device).unsqueeze(0)
    with torch.no_grad():
        logits = model(url_tok)
        p_phish = torch.sigmoid(logits)
        label = int(p_phish >= 0.5)
    return "Safe" if label == 0 else "Phishing"