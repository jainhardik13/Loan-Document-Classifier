# Frontend (React + Tailwind)

## Folder Structure

```text
frontend/
├── index.html
├── package.json
├── postcss.config.js
├── tailwind.config.js
├── vite.config.js
└── src/
    ├── index.css
    ├── main.jsx
    ├── components/
    │   ├── Navbar.jsx
    │   ├── Classifier.jsx
    │   ├── Report.jsx
    │   ├── BusinessImpact.jsx
    │   └── Loader.jsx
    └── pages/
        └── Home.jsx
```

## Install and Run

```bash
cd frontend
npm install
npm run dev
```

The app runs on `http://localhost:5173`.

## Backend Connection

The frontend calls:

- `POST http://localhost:5000/predict`

Expected request:

```json
{
  "text": "sample document text"
}
```

Supported response keys (either style works):

- `predicted_category` + `confidence_score` (current backend)
- `prediction` + `confidence` (generic API style)

## Demo Screens (description)

1. **Classifier section**: textarea, sample autofill chips, classify button, loader, confidence progress bar.
2. **Report section**: model metric cards, comparison bar chart, confusion matrix heatmap-style grid.
3. **Business impact section**: KPI cards, daily hours bar chart, time split pie chart.
