from pathlib import Path
from typing import Dict, List, Tuple

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    precision_recall_fscore_support,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC

try:
    from .preprocessing import preprocess_text
except ImportError:
    from preprocessing import preprocess_text

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "loan_documents.csv"
MODELS_DIR = BASE_DIR / "models"
REPORTS_DIR = MODELS_DIR / "reports"


def load_data(file_path: Path) -> pd.DataFrame:
    """Load and validate dataset."""
    if not file_path.exists():
        raise FileNotFoundError(f"Dataset not found at: {file_path}")

    df = pd.read_csv(file_path)
    required_columns = {"Document_Text", "Category"}
    if not required_columns.issubset(df.columns):
        raise ValueError(
            f"Dataset must contain columns: {required_columns}. Found: {set(df.columns)}"
        )
    return df


def build_model_grids() -> Dict[str, Dict[str, object]]:
    """Create model pipelines and anti-overfitting hyperparameter grids."""
    nb_pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
            ("model", MultinomialNB()),
        ]
    )

    svm_pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer(ngram_range=(1, 2))),
            ("model", SVC(kernel="linear", probability=True, random_state=42)),
        ]
    )

    return {
        "MultinomialNB": {
            "pipeline": nb_pipeline,
            "param_grid": {
                "tfidf__max_features": [800, 1200, 2000],
                "tfidf__min_df": [1, 2, 3],
                "tfidf__max_df": [0.85, 0.95, 1.0],
                "model__alpha": [0.5, 1.0, 1.5],
            },
        },
        "SVM": {
            "pipeline": svm_pipeline,
            "param_grid": {
                "tfidf__max_features": [800, 1200, 2000],
                "tfidf__min_df": [1, 2, 3],
                "tfidf__max_df": [0.85, 0.95, 1.0],
                "model__C": [0.1, 0.5, 1.0],
            },
        },
    }


def tune_model_with_cv(
    model_name: str, pipeline: Pipeline, param_grid: Dict[str, object], x_train: pd.Series, y_train: pd.Series
) -> Dict[str, object]:
    """Tune model with stratified cross-validation to reduce overfitting risk."""
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    search = GridSearchCV(
        estimator=pipeline,
        param_grid=param_grid,
        scoring="f1_weighted",
        cv=cv,
        n_jobs=-1,
    )
    search.fit(x_train, y_train)
    return {
        "model": model_name,
        "best_estimator": search.best_estimator_,
        "best_cv_f1_weighted": search.best_score_,
        "best_params": search.best_params_,
    }


def evaluate_model(
    model_name: str, model: Pipeline, x_test: pd.Series, y_test: pd.Series
) -> Tuple[Dict[str, float], str, pd.DataFrame]:
    """Evaluate one model and return metrics."""
    y_pred = model.predict(x_test)
    accuracy = accuracy_score(y_test, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_test, y_pred, average="weighted", zero_division=0
    )

    report = classification_report(y_test, y_pred, zero_division=0)
    labels = sorted(y_test.unique())
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)

    metrics = {
        "model": model_name,
        "accuracy": accuracy,
        "precision_weighted": precision,
        "recall_weighted": recall,
        "f1_weighted": f1,
    }
    return metrics, report, cm_df


def save_confusion_matrix(model_name: str, cm_df: pd.DataFrame) -> None:
    """Save confusion matrix image."""
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm_df, annot=True, fmt="d", cmap="Blues")
    plt.title(f"{model_name} Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.tight_layout()

    output_path = REPORTS_DIR / f"{model_name.lower()}_confusion_matrix.png"
    plt.savefig(output_path)
    plt.close()


def run_custom_tests(best_model: Pipeline) -> pd.DataFrame:
    """Run required custom unseen test examples."""
    custom_inputs: List[str] = [
        "employee monthly payslip showing gross salary, net pay, PF deduction and TDS",
        "bank account statement with opening balance, UPI debits and NEFT credits",
        "income tax return acknowledgement for assessment year with taxable income and refund",
        "registered sale deed for residential plot with survey number and stamp duty",
        "aadhaar card copy containing uid number and date of birth",
    ]

    predictions = best_model.predict(custom_inputs)
    confidences = best_model.predict_proba(custom_inputs).max(axis=1)

    results = pd.DataFrame(
        {
            "input_text": custom_inputs,
            "predicted_category": predictions,
            "confidence_score": confidences.round(4),
        }
    )
    return results


def calculate_business_impact() -> Dict[str, float]:
    """Calculate daily/monthly time savings for business use case."""
    docs_per_day = 500
    manual_minutes_per_doc = 2

    manual_minutes_per_day = docs_per_day * manual_minutes_per_doc
    manual_hours_per_day = manual_minutes_per_day / 60
    monthly_hours_saved = manual_hours_per_day * 30

    optional_cost_per_hour = 250  # Example value in INR
    optional_monthly_cost_saved = monthly_hours_saved * optional_cost_per_hour

    return {
        "documents_per_day": docs_per_day,
        "manual_minutes_per_document": manual_minutes_per_doc,
        "daily_minutes_saved": manual_minutes_per_day,
        "daily_hours_saved": round(manual_hours_per_day, 2),
        "monthly_hours_saved": round(monthly_hours_saved, 2),
        "optional_cost_per_hour_inr": optional_cost_per_hour,
        "optional_monthly_cost_saved_inr": round(optional_monthly_cost_saved, 2),
    }


def save_reports(
    comparison_df: pd.DataFrame,
    model_reports: Dict[str, str],
    custom_results_df: pd.DataFrame,
    business_impact: Dict[str, float],
    tuning_results: List[Dict[str, object]],
) -> None:
    """Save model comparison and details to files."""
    comparison_df.to_csv(REPORTS_DIR / "model_comparison.csv", index=False)
    custom_results_df.to_csv(REPORTS_DIR / "custom_test_predictions.csv", index=False)

    with open(REPORTS_DIR / "classification_reports.txt", "w", encoding="utf-8") as f:
        for model_name, report in model_reports.items():
            f.write(f"========== {model_name} ==========\n")
            f.write(report)
            f.write("\n\n")

    with open(REPORTS_DIR / "business_impact.txt", "w", encoding="utf-8") as f:
        for key, value in business_impact.items():
            f.write(f"{key}: {value}\n")

    with open(REPORTS_DIR / "cv_tuning_results.txt", "w", encoding="utf-8") as f:
        for result in tuning_results:
            f.write(f"========== {result['model']} ==========\n")
            f.write(f"best_cv_f1_weighted: {result['best_cv_f1_weighted']:.4f}\n")
            f.write("best_params:\n")
            for key, value in result["best_params"].items():
                f.write(f"  - {key}: {value}\n")
            f.write("\n")


def main() -> None:
    MODELS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)

    df = load_data(DATA_PATH)
    df["processed_text"] = df["Document_Text"].apply(preprocess_text)

    x_train, x_test, y_train, y_test = train_test_split(
        df["processed_text"],
        df["Category"],
        test_size=0.2,
        random_state=42,
        stratify=df["Category"],
    )

    model_grids = build_model_grids()

    all_metrics = []
    all_reports = {}
    fitted_models = {}
    tuning_results: List[Dict[str, object]] = []

    for model_name, model_bundle in model_grids.items():
        tuning_result = tune_model_with_cv(
            model_name=model_name,
            pipeline=model_bundle["pipeline"],
            param_grid=model_bundle["param_grid"],
            x_train=x_train,
            y_train=y_train,
        )
        tuning_results.append(tuning_result)
        tuned_model = tuning_result["best_estimator"]
        metrics, report, cm_df = evaluate_model(model_name, tuned_model, x_test, y_test)

        all_metrics.append(metrics)
        all_reports[model_name] = report
        fitted_models[model_name] = tuned_model

        save_confusion_matrix(model_name, cm_df)

    comparison_df = pd.DataFrame(all_metrics).sort_values(
        by="f1_weighted", ascending=False
    )
    best_model_name = comparison_df.iloc[0]["model"]
    best_model = fitted_models[best_model_name]

    joblib.dump(best_model, MODELS_DIR / "best_model.pkl")
    joblib.dump(preprocess_text, MODELS_DIR / "preprocess_function.pkl")

    custom_results_df = run_custom_tests(best_model)
    business_impact = calculate_business_impact()

    save_reports(
        comparison_df,
        all_reports,
        custom_results_df,
        business_impact,
        tuning_results,
    )

    print("\nModel Comparison:")
    print(comparison_df.to_string(index=False))
    print("\nCross-Validation Tuning:")
    for result in tuning_results:
        print(f"- {result['model']} best CV f1_weighted: {result['best_cv_f1_weighted']:.4f}")
        print(f"  params: {result['best_params']}")
    print(f"\nBest model saved: {best_model_name}")
    print("\nCustom Test Predictions:")
    print(custom_results_df.to_string(index=False))
    print("\nBusiness Impact:")
    for key, value in business_impact.items():
        print(f"- {key}: {value}")


if __name__ == "__main__":
    main()
