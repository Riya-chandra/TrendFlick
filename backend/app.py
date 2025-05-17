from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
from dotenv import load_dotenv
import os
import requests

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_gemini_hashtags(text):
    api_key = os.getenv('GEMINI_API_KEY')

    if not api_key:
        print("Error: GEMINI_API_KEY not found in environment variables.")
        return ["#Trending"]

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    prompt = f"Suggest 10 trending and relevant hashtags for this text:\n\"{text}\"\nOnly return hashtags separated by spaces. No explanation."

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ],
            "generationConfig": {
        "temperature": 0.7,
        "maxOutputTokens": 128,  # Increased token limit
        "topP": 0.8,
        "topK": 40
            },
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        print("Gemini raw response:", result)

        candidates = result.get("candidates", [])
        if not candidates:
            raise ValueError("No candidates returned by Gemini.")

        raw_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
        if not raw_text:
            raise ValueError("No output text returned by Gemini.")

        print("Gemini returned text:", raw_text)

        hashtags = [tag.strip() for tag in raw_text.split() if tag.startswith("#")]
        return hashtags if hashtags else ["#Trending"]

    except Exception as e:
        print("Parsing or API error:", str(e))
        return ["#Trending"]



vectorizer = joblib.load('../ml_model/vectorizer.joblib')
clf = joblib.load('../ml_model/sentiment_model.joblib')
reg_likes = joblib.load('../ml_model/likes_model.joblib')
reg_retweets = joblib.load('../ml_model/retweet_model.joblib')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get('text', '').strip()

    if not text:
        return jsonify({'error': 'No input text provided'}), 400

    try:
        X = vectorizer.transform([text])
        sentiment_pred = clf.predict(X)[0]
        likes_pred = reg_likes.predict(X)[0]
        retweet_pred = reg_retweets.predict(X)[0]

        sentiment_label = 'Positive' if sentiment_pred == 1 else 'Negative'

        hashtags = get_gemini_hashtags(text)

        return jsonify({
            'sentiment': sentiment_label,
            'likes': float(likes_pred),
            'retweets': float(retweet_pred),
            'hashtags': hashtags
        })

    except Exception as e:
        print("Prediction error:", e)
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
