export default function Loader({ message = "Predicting..." }) {
  return (
    <div className="flex items-center gap-3 rounded-xl bg-brand-50 px-4 py-3 text-brand-700 dark:bg-slate-800 dark:text-brand-100">
      <span className="h-4 w-4 animate-spin rounded-full border-2 border-brand-500 border-t-transparent" />
      <span className="text-sm font-medium">{message}</span>
    </div>
  );
}
