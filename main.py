from flask import Flask, request, render_template
import tensorflow as tf
import pickle
import os
import re
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from fuzzywuzzy import fuzz

# Initialize Flask app
app = Flask(__name__)

# Constants
MAX_LEN = 100
TRUSTED_DOMAINS = [
    "google.com", "facebook.com", "amazon.com", "microsoft.com", "apple.com",
    "paypal.com", "twitter.com", "linkedin.com", "instagram.com", "youtube.com"
]
SUSPICIOUS_KEYWORDS = [
    "free", "alert", "important", "gift", "prize", "offer", "win", 
    "malicious", "fake", "redirect", "ad", "malware", "attack", "alert", "target", "command", "false", "cmd"
]
MIRRORED_CHARACTERS = set("ɒɔɘʇϱįʞɿƨτγ")

# Load the model and tokenizer
MODEL_PATH = "cnn_lstm_model_12-01-2025-1.h5"
TOKENIZER_PATH = "tokenizer.pkl"

model = load_model(MODEL_PATH)
with open(TOKENIZER_PATH, "rb") as file:
    tokenizer = pickle.load(file)

# Helper functions
def is_typo_in_domain(domain, threshold=90):
    for trusted_domain in TRUSTED_DOMAINS:
        if domain == trusted_domain:
            return False
        similarity = fuzz.ratio(domain, trusted_domain)
        if similarity > threshold:
            return True
    return False

def contains_suspicious_keywords_in_url(url):
    url_lower = url.lower()
    for keyword in SUSPICIOUS_KEYWORDS:
        if keyword in url_lower:
            return True
    return False

def is_random_or_nonsense(url):
    if len(re.findall(r'\d', url)) > 5:
        return True
    if len(re.findall(r'[^\w\-.:/]', url)) > 10:
        return True
    if re.match(r'^[a-zA-Z0-9]{32,}$', url.split("//")[-1]):
        return True
    return False

def predict_url(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        regex_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        if not re.match(regex_pattern, url):
            return "Invalid URL format. Please enter a valid URL."

        if any(char in MIRRORED_CHARACTERS for char in url):
            return "Phishing"

        if is_random_or_nonsense(url):
            return "Not a proper URL"

        if contains_suspicious_keywords_in_url(url):
            return "Phishing"

        domain_match = re.search(r'://(?:www\.)?([a-zA-Z0-9.-]+)', url)
        if domain_match:
            domain = domain_match.group(1)
            if domain in TRUSTED_DOMAINS:
                return "Legitimate"
            if any(char.isdigit() for char in domain):
                return "Phishing"
            if is_typo_in_domain(domain, threshold=80):
                return "Phishing"

        if re.search(r'https?://(?:[^/]+/){2,}', url):
            return "Phishing"

        sequence = tokenizer.texts_to_sequences([url])
        input_vector = pad_sequences(sequence, maxlen=MAX_LEN, padding='post')
        prediction = model.predict(input_vector)[0][0]

        return "Phishing" if prediction >= 0.5 else "Legitimate"

    except Exception as e:
        return f"Error in prediction: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form["url"]
        result = predict_url(url)
        return render_template("index.html", url=url, result=result)

    return render_template("index.html", url=None, result=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5600)))
