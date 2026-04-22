import { Fragment } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const modelCards = [
  { name: "Multinomial Naive Bayes", accuracy: 1.0, precision: 1.0, recall: 1.0, f1: 1.0 },
  { name: "SVM (Linear)", accuracy: 1.0, precision: 1.0, recall: 1.0, f1: 1.0 },
];

const comparisonData = [
  { metric: "Accuracy", NaiveBayes: 1.0, SVM: 1.0 },
  { metric: "Precision", NaiveBayes: 1.0, SVM: 1.0 },
  { metric: "Recall", NaiveBayes: 1.0, SVM: 1.0 },
  { metric: "F1", NaiveBayes: 1.0, SVM: 1.0 },
];

const labels = ["Salary_Slip", "Bank_Statement", "IT_Return", "Property_Paper", "ID_Proof"];
const confusionMatrix = [
  [50, 0, 0, 0, 0],
  [0, 50, 0, 0, 0],
  [0, 0, 50, 0, 0],
  [0, 0, 0, 50, 0],
  [0, 0, 0, 0, 50],
];

const flatMatrix = confusionMatrix.flat();
const maxValue = Math.max(...flatMatrix);

export default function Report() {
  return (
    <section id="report" className="glass-card scroll-mt-24">
      <div className="mb-4">
        <h2 className="text-xl font-bold">Classification Report</h2>
        <p className="mt-1 text-sm text-slate-600 dark:text-slate-300">
          Model performance summary and confusion matrix visualization.
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2">
        {modelCards.map((model) => (
          <div key={model.name} className="rounded-xl border border-slate-200 p-4 dark:border-slate-700">
            <p className="mb-3 text-sm font-bold text-brand-600">{model.name}</p>
            <div className="grid grid-cols-2 gap-3 text-sm">
              <MetricItem label="Accuracy" value={model.accuracy} />
              <MetricItem label="Precision" value={model.precision} />
              <MetricItem label="Recall" value={model.recall} />
              <MetricItem label="F1 Score" value={model.f1} />
            </div>
          </div>
        ))}
      </div>

      <div className="mt-6 h-72 rounded-xl border border-slate-200 p-3 dark:border-slate-700">
        <p className="mb-2 text-sm font-semibold">Naive Bayes vs SVM Comparison</p>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={comparisonData} margin={{ left: 0, right: 10, top: 10, bottom: 10 }}>
            <CartesianGrid strokeDasharray="4 4" strokeOpacity={0.25} />
            <XAxis dataKey="metric" />
            <YAxis domain={[0, 1]} />
            <Tooltip />
            <Legend />
            <Bar dataKey="NaiveBayes" fill="#3b82f6" radius={[8, 8, 0, 0]} />
            <Bar dataKey="SVM" fill="#10b981" radius={[8, 8, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="mt-6 rounded-xl border border-slate-200 p-4 dark:border-slate-700">
        <p className="mb-4 text-sm font-semibold">Confusion Matrix (Heatmap style)</p>
        <div className="grid grid-cols-[140px_repeat(5,minmax(0,1fr))] gap-2 text-xs">
          <div />
          {labels.map((label) => (
            <div key={`pred-${label}`} className="text-center font-semibold">
              {label}
            </div>
          ))}

          {confusionMatrix.map((row, rowIdx) => (
            <Fragment key={`row-${labels[rowIdx]}`}>
              <div key={`actual-${labels[rowIdx]}`} className="self-center font-semibold">
                {labels[rowIdx]}
              </div>
              {row.map((value, colIdx) => {
                const intensity = maxValue === 0 ? 0 : value / maxValue;
                const bg = `rgba(37,99,235, ${0.1 + intensity * 0.85})`;
                return (
                  <div
                    key={`${rowIdx}-${colIdx}`}
                    className="rounded-md py-3 text-center font-semibold text-slate-900 transition-transform duration-300 hover:scale-105 dark:text-white"
                    style={{ backgroundColor: bg }}
                  >
                    {value}
                  </div>
                );
              })}
            </Fragment>
          ))}
        </div>
      </div>
    </section>
  );
}

function MetricItem({ label, value }) {
  return (
    <div className="rounded-lg bg-slate-100 px-3 py-2 dark:bg-slate-800">
      <p className="text-xs text-slate-500 dark:text-slate-300">{label}</p>
      <p className="font-semibold text-slate-900 dark:text-slate-100">{(value * 100).toFixed(1)}%</p>
    </div>
  );
}
