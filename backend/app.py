from flask import Flask, jsonify, request
from flask_cors import CORS

try:
    from .model_service import ModelService
except ImportError:
    from model_service import ModelService

app = Flask(__name__)
CORS(
    app,
    resources={r"/predict": {"origins": ["http://localhost:5173", "http://127.0.0.1:5173"]}},
)
model_service = ModelService()


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "Loan Document Classifier API is running"})


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(silent=True)
        if not data or "text" not in data:
            return jsonify({"error": "Request body must contain 'text' field."}), 400

        result = model_service.predict(data["text"])
        return jsonify(result), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except FileNotFoundError as exc:
        return jsonify({"error": str(exc)}), 500
    except Exception as exc:  # pragma: no cover
        return jsonify({"error": f"Unexpected error: {str(exc)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
