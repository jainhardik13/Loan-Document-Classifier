# Loan Document Classifier using NLP

This project classifies loan-related document text into:
- `Salary_Slip`
- `Bank_Statement`
- `IT_Return`
- `Property_Paper`
- `ID_Proof`

It includes:
- NLP preprocessing
- TF-IDF feature engineering
- Two ML models (Multinomial Naive Bayes and SVM)
- Evaluation metrics and confusion matrices
- Flask backend API (`POST /predict`)
- Streamlit frontend UI
- Business impact calculation

---

## 1) Step-by-Step Project Explanation

### Step 1: Load dataset
Dataset is read from `data/loan_documents.csv` with columns:
- `Document_Text`
- `Category`

### Step 2: Text preprocessing
Implemented in `backend/preprocessing.py`:
- Convert to lowercase
- Remove symbols/punctuation
- Tokenize words
- Remove stopwords
- Lemmatize tokens (optional, enabled by default)

### Step 3: Feature engineering (TF-IDF)
Used via `TfidfVectorizer` in each model pipeline:
- Converts processed text to numeric vectors
- Uses unigram + bigram (`ngram_range=(1, 2)`)

### Step 4: Model training
Implemented in `backend/train.py`:
- Split data into train/test (`80/20`, stratified)
- Train:
  - `MultinomialNB`
  - `SVC(kernel="linear", probability=True)`

### Step 5: Evaluation
For both models, generate:
- Accuracy
- Precision (weighted)
- Recall (weighted)
- F1-score (weighted)
- Classification report
- Confusion matrix plot

Reports are saved in `models/reports/`.

### Step 6: Save best model
Best model (based on weighted F1) is saved to:
- `models/best_model.pkl`

### Step 7: API and frontend
- Flask API in `backend/app.py`
- Streamlit UI in `frontend/streamlit_app.py`

### Step 8: Business impact
Calculated in training pipeline:
- `500` docs/day
- `2` minutes manual sorting/doc
- Daily and monthly time savings
- Optional monthly cost savings (example hourly cost)

---

## 2) Project Structure

```text
Project 5/
├── data/
│   └── loan_documents.csv
├── models/
│   └── reports/                      # created after training
├── notebooks/                        # optional
├── backend/
│   ├── app.py
│   ├── model_service.py
│   ├── preprocessing.py
│   └── train.py
├── frontend/
│   └── streamlit_app.py
├── main.py
├── requirements.txt
└── README.md
```

---

## 3) How to Run Locally

### A) Setup
```bash
python -m venv .venv
```

Windows PowerShell:
```bash
.venv\Scripts\Activate.ps1
```

Install dependencies:
```bash
pip install -r requirements.txt
```

### B) Train model + generate reports
```bash
python main.py train
```

### C) Start backend API
```bash
python main.py api
```

Runs at:
- `http://127.0.0.1:5000`
- Health check: `GET /health`
- Prediction: `POST /predict`

### D) Start frontend (new terminal)
```bash
python main.py ui
```

Streamlit opens in browser (usually `http://localhost:8501`).

---

## 4) API Usage

### Endpoint
`POST /predict`

### Input JSON
```json
{
  "text": "monthly salary payslip gross salary net pay PF and TDS deductions"
}
```

### Output JSON (example)
```json
{
  "input_text": "monthly salary payslip gross salary net pay PF and TDS deductions",
  "processed_text": "monthly salary payslip gross salary net pay pf tds deduction",
  "predicted_category": "Salary_Slip",
  "confidence_score": 0.9862
}
```

---

## 5) Sample Test Inputs and Expected Behavior

1. `monthly payslip with net salary and PF deduction` -> likely `Salary_Slip`
2. `savings account statement showing UPI debit and NEFT credit` -> likely `Bank_Statement`
3. `ITR acknowledgement with taxable income and refund details` -> likely `IT_Return`
4. `sale deed with survey number and stamp duty details` -> likely `Property_Paper`
5. `aadhaar card with uid and date of birth` -> likely `ID_Proof`

Actual predictions are generated and saved in:
- `models/reports/custom_test_predictions.csv`

---

## 6) Why TF-IDF is Better Than Raw Counts

Raw counts only track how many times words appear. Common words may dominate the vector even if they are not useful for classification.

TF-IDF improves this by:
- Increasing importance of terms frequent in a specific document
- Reducing importance of terms frequent across many documents
- Creating more discriminative features for classifiers

For example, domain keywords like `payslip`, `itr`, `encumbrance`, `aadhaar` become more influential than generic words.

---

## 7) How to Extend for Real PDF Documents (OCR Pipeline)

For production with actual scanned files:

1. **Ingestion**: Accept PDF/JPG uploads
2. **OCR Extraction**:
   - Use Tesseract, EasyOCR, or cloud OCR (AWS Textract / Google Vision / Azure OCR)
3. **Text Cleanup**:
   - Remove OCR noise, special chars, and layout artifacts
4. **Classification**:
   - Send extracted text to `/predict`
5. **Storage + Workflow**:
   - Save file metadata, predicted class, and confidence
   - Route to the loan processing queue automatically
6. **Human-in-the-loop**:
   - If confidence below threshold (e.g., <0.75), send for manual verification

---

## 8) What if a New Unseen Category Appears?

Current model is a closed-set classifier, so it will still force one of known 5 classes.

Practical handling:
- Use confidence threshold (if low confidence, mark as `Unknown`)
- Add anomaly detection / out-of-distribution checks
- Collect manually reviewed unknown samples
- Periodically retrain with new category labels

---

## 9) Screenshots Description (for demo report)

You can include:
1. **Training console output**: model comparison table + business impact numbers
2. **Confusion matrix images** in `models/reports/`
3. **Streamlit UI screen** showing:
   - input text
   - predicted class
   - confidence score

