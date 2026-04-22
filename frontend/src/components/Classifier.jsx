import { useMemo } from "react";
import Loader from "./Loader";

const samples = [
  "monthly payslip with gross salary net pay pf and tds deduction",
  "bank statement opening balance neft transfer upi debit and closing balance",
  "income tax return acknowledgement with assessment year taxable income and refund",
  "registered sale deed with survey number stamp duty and property details",
  "aadhaar card uid number date of birth and address details",
];

const categoryColors = {
  Salary_Slip: "bg-emerald-100 text-emerald-800 dark:bg-emerald-900/50 dark:text-emerald-200",
  Bank_Statement: "bg-blue-100 text-blue-800 dark:bg-blue-900/50 dark:text-blue-200",
  IT_Return: "bg-purple-100 text-purple-800 dark:bg-purple-900/50 dark:text-purple-200",
  Property_Paper: "bg-amber-100 text-amber-800 dark:bg-amber-900/50 dark:text-amber-200",
  ID_Proof: "bg-rose-100 text-rose-800 dark:bg-rose-900/50 dark:text-rose-200",
};

export default function Classifier({
  text,
  onTextChange,
  onClassify,
  loading,
  error,
  result,
  onUseSample,
}) {
  const confidencePercentage = useMemo(() => {
    if (!result?.confidence) return 0;
    return Math.round(result.confidence * 100);
  }, [result]);

  const categoryClass =
    categoryColors[result?.prediction] ||
    "bg-slate-100 text-slate-800 dark:bg-slate-800 dark:text-slate-200";

  return (
    <section id="classifier" className="glass-card scroll-mt-24">
      <div className="mb-4">
        <h2 className="text-xl font-bold">Document Classifier</h2>
        <p className="mt-1 text-sm text-slate-600 dark:text-slate-300">
          Paste OCR-extracted text and run AI-based category prediction.
        </p>
      </div>

      <textarea
        value={text}
        onChange={(event) => onTextChange(event.target.value)}
        placeholder="Paste document text (OCR output)..."
        className="min-h-40 w-full rounded-xl border border-slate-300 bg-white p-4 text-sm outline-none ring-brand-500 transition focus:ring-2 dark:border-slate-700 dark:bg-slate-900"
      />

      <div className="mt-4 flex flex-wrap gap-2">
        {samples.map((sample, index) => (
          <button
            key={sample}
            onClick={() => onUseSample(sample)}
            className="rounded-full border border-slate-300 px-3 py-1 text-xs font-semibold text-slate-700 transition hover:bg-slate-100 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
          >
            Sample {index + 1}
          </button>
        ))}
      </div>

      <button
        onClick={onClassify}
        disabled={loading}
        className="mt-5 w-full rounded-xl bg-brand-600 px-4 py-3 text-sm font-bold text-white transition hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-70"
      >
        Classify Document
      </button>

      <div className="mt-5 space-y-3">
        {loading && <Loader message="Classifying document..." />}
        {error && (
          <p className="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700 dark:bg-red-900/40 dark:text-red-200">
            {error}
          </p>
        )}

        {result && !loading && (
          <div className="space-y-3 rounded-xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-700 dark:bg-slate-800/60">
            <div className="flex items-center justify-between gap-3">
              <span className="text-sm text-slate-600 dark:text-slate-300">Predicted Category</span>
              <span className={`rounded-full px-3 py-1 text-sm font-semibold ${categoryClass}`}>
                {result.prediction}
              </span>
            </div>
            <div>
              <div className="mb-1 flex items-center justify-between text-sm">
                <span className="text-slate-600 dark:text-slate-300">Confidence Score</span>
                <span className="font-semibold">{confidencePercentage}%</span>
              </div>
              <div className="h-3 w-full rounded-full bg-slate-200 dark:bg-slate-700">
                <div
                  className="h-3 rounded-full bg-brand-600 transition-all duration-700"
                  style={{ width: `${confidencePercentage}%` }}
                />
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
