from pathlib import Path
import sys

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.preprocessing import preprocess_text

MODEL_PATH = BASE_DIR / "models" / "best_model.pkl"
DATASET_PATH = Path(__file__).resolve().parent / "noisy_loan_documents.csv"
OUTPUT_REPORT_PATH = Path(__file__).resolve().parent / "noisy_classification_report.txt"
OUTPUT_CM_PATH = Path(__file__).resolve().parent / "noisy_confusion_matrix.csv"


def main() -> None:
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model missing. Run training first: python main.py train")
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            "Noisy dataset missing. Run: python unseen_evaluation/generate_noisy_dataset.py"
        )

    model = joblib.load(MODEL_PATH)
    df = pd.read_csv(DATASET_PATH)
    required_cols = {"Document_Text", "Category"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"Dataset must contain columns: {required_cols}")

    df["processed_text"] = df["Document_Text"].apply(preprocess_text)
    y_true = df["Category"]
    y_pred = model.predict(df["processed_text"])

    accuracy = accuracy_score(y_true, y_pred)
    report = classification_report(y_true, y_pred, digits=4, zero_division=0)
    labels = sorted(y_true.unique())
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    cm_df.to_csv(OUTPUT_CM_PATH)

    with open(OUTPUT_REPORT_PATH, "w", encoding="utf-8") as file:
        file.write("Noisy Dataset Evaluation\n")
        file.write(f"Total samples: {len(df)}\n")
        file.write(f"Accuracy: {accuracy:.4f}\n\n")
        file.write(report)

    print("=== Noisy Dataset Classification Report ===")
    print(f"Total samples: {len(df)}")
    print(f"Accuracy: {accuracy:.4f}\n")
    print(report)
    print(f"Report saved to: {OUTPUT_REPORT_PATH}")
    print(f"Confusion matrix saved to: {OUTPUT_CM_PATH}")


if __name__ == "__main__":
    main()
