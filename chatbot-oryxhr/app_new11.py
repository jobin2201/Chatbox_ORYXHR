from flask import Flask, request, jsonify
import os, json, secrets
import difflib
from spellchecker import SpellChecker
from dotenv import load_dotenv

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Load env vars
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Load predefined responses
with open("predefined_response.json", "r", encoding="utf-8") as file:
    data = json.load(file)
    predefined_responses = data.get("responses", {})
    variations = data.get("variations", {})

spell = SpellChecker()

def clean_and_match_query(msg):
    msg = msg.lower().strip()
    corrected = " ".join([spell.correction(w) or w for w in msg.split()])
    if corrected in predefined_responses:
        return corrected
    for k, vals in variations.items():
        if corrected in vals:
            return k
    all_keys = list(predefined_responses.keys()) + list(variations.keys())
    matches = difflib.get_close_matches(corrected, all_keys, n=1, cutoff=0.6)
    return matches[0] if matches else None

@app.route("/")
def index():
    return "Chatbot API is running! POST to /api/chat"

@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400
    msg = data["message"]
    matched_key = clean_and_match_query(msg)
    response = predefined_responses.get(matched_key, "Sorry, I couldn't understand.") if matched_key else "Sorry, I couldn't understand your question."
    return jsonify({"message": msg, "matched_key": matched_key, "response": response})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)

