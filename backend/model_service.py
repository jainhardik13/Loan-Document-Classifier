from pathlib import Path
from typing import Dict

import joblib

try:
    from .preprocessing import preprocess_text
except ImportError:
    from preprocessing import preprocess_text

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "best_model.pkl"


class ModelService:
    """Service class for loading model and running predictions."""

    def __init__(self) -> None:
        self.model = None

    def load_model(self) -> None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Trained model not found at {MODEL_PATH}. Run backend/train.py first."
            )
        self.model = joblib.load(MODEL_PATH)

    def predict(self, text: str) -> Dict[str, object]:
        if self.model is None:
            self.load_model()

        if not isinstance(text, str) or not text.strip():
            raise ValueError("Text must be a non-empty string.")

        processed_text = preprocess_text(text)
        prediction = self.model.predict([processed_text])[0]
        confidence = float(self.model.predict_proba([processed_text]).max())

        return {
            "input_text": text,
            "processed_text": processed_text,
            "predicted_category": prediction,
            "confidence_score": round(confidence, 4),
        }
