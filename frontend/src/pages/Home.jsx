import { useEffect, useState } from "react";
import Navbar from "../components/Navbar";
import Classifier from "../components/Classifier";
import Report from "../components/Report";
import BusinessImpact from "../components/BusinessImpact";

const API_URL = "http://localhost:5000/predict";

export default function Home() {
  const [darkMode, setDarkMode] = useState(false);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);

  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode);
  }, [darkMode]);

  const handleClassify = async () => {
    if (!text.trim()) {
      setError("Please provide OCR text before classification.");
      setResult(null);
      return;
    }

    try {
      setLoading(true);
      setError("");
      setResult(null);

      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
      });

      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.error || "Prediction failed. Try again.");
      }

      setResult({
        prediction: payload.predicted_category || payload.prediction || "Unknown",
        confidence: payload.confidence_score ?? payload.confidence ?? 0,
      });
    } catch (requestError) {
      setError(
        requestError.message ||
          "Unable to connect to backend. Ensure Flask API is running on localhost:5000."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-full">
      <Navbar darkMode={darkMode} onToggleDarkMode={() => setDarkMode((prev) => !prev)} />
      <main className="mx-auto flex max-w-7xl flex-col gap-6 px-4 py-6 sm:px-6 lg:px-8">
        <Classifier
          text={text}
          onTextChange={setText}
          onClassify={handleClassify}
          loading={loading}
          error={error}
          result={result}
          onUseSample={(sample) => setText(sample)}
        />
        <Report />
        <BusinessImpact />
      </main>
    </div>
  );
}
