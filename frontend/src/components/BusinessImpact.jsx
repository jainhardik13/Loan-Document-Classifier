import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip, XAxis, YAxis, CartesianGrid, BarChart, Bar } from "recharts";

const summaryCards = [
  { label: "Documents / Day", value: "500", icon: "📄" },
  { label: "Manual Time / Document", value: "2 min", icon: "⏱️" },
  { label: "Daily Time Saved", value: "16.67 hrs", icon: "⚡" },
  { label: "Monthly Time Saved", value: "500 hrs", icon: "📈" },
  { label: "Optional Monthly Cost Saved", value: "₹125,000", icon: "💰" },
];

const barData = [
  { name: "Manual (Daily)", hours: 16.67 },
  { name: "AI Assisted (Daily)", hours: 2.1 },
];

const pieData = [
  { name: "Time Saved", value: 14.57, color: "#3b82f6" },
  { name: "Time Used", value: 2.1, color: "#94a3b8" },
];

export default function BusinessImpact() {
  return (
    <section id="impact" className="glass-card scroll-mt-24">
      <div className="mb-4">
        <h2 className="text-xl font-bold">Business Impact Dashboard</h2>
        <p className="mt-1 text-sm text-slate-600 dark:text-slate-300">
          Estimated operational improvement after document auto-classification.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
        {summaryCards.map((card) => (
          <div key={card.label} className="rounded-xl border border-slate-200 p-4 dark:border-slate-700">
            <p className="text-xl">{card.icon}</p>
            <p className="mt-2 text-xs text-slate-500 dark:text-slate-300">{card.label}</p>
            <p className="text-lg font-bold text-brand-600">{card.value}</p>
          </div>
        ))}
      </div>

      <div className="mt-6 grid gap-6 lg:grid-cols-2">
        <div className="h-72 rounded-xl border border-slate-200 p-3 dark:border-slate-700">
          <p className="mb-2 text-sm font-semibold">Daily Processing Hours Comparison</p>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={barData}>
              <CartesianGrid strokeDasharray="4 4" strokeOpacity={0.25} />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="hours" fill="#2563eb" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="h-72 rounded-xl border border-slate-200 p-3 dark:border-slate-700">
          <p className="mb-2 text-sm font-semibold">AI Adoption Time Split</p>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie data={pieData} dataKey="value" nameKey="name" outerRadius={100} label>
                {pieData.map((entry) => (
                  <Cell key={entry.name} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>
    </section>
  );
}
