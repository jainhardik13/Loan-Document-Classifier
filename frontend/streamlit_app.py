import requests
import streamlit as st

API_URL = "http://127.0.0.1:5000/predict"

st.set_page_config(page_title="Loan Document Classifier", page_icon="📄", layout="centered")
st.title("Loan Document Classifier")
st.write("Enter a document description and classify it into the loan document category.")

user_text = st.text_area(
    "Document Description",
    placeholder="Example: Monthly payslip with gross salary, net salary, PF and TDS deductions",
    height=140,
)

if st.button("Classify"):
    if not user_text.strip():
        st.error("Please enter some text before classification.")
    else:
        try:
            response = requests.post(API_URL, json={"text": user_text}, timeout=20)
            if response.status_code == 200:
                result = response.json()
                st.success("Classification completed.")
                st.write(f"**Predicted Category:** {result['predicted_category']}")
                st.write(f"**Confidence Score:** {result['confidence_score']:.4f}")
                st.caption(f"Processed Text: {result['processed_text']}")
            else:
                st.error(f"API error ({response.status_code}): {response.json().get('error')}")
        except requests.RequestException as exc:
            st.error(
                "Unable to connect to backend API. Start Flask server first.\n\n"
                f"Error: {str(exc)}"
            )
