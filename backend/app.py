from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

# Load models
vectorizer = joblib.load('../ml_model/vectorizer.joblib')
clf = joblib.load('../ml_model/sentiment_model.joblib')
reg_likes = joblib.load('../ml_model/likes_model.joblib')
reg_retweets = joblib.load('../ml_model/retweet_model.joblib')  # NEW

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No input text provided'}), 400

    X = vectorizer.transform([text])
    sentiment_pred = clf.predict(X)[0]
    likes_pred = reg_likes.predict(X)[0]
    retweet_pred = reg_retweets.predict(X)[0]  # NEW

    sentiment_label = 'Positive' if sentiment_pred == 1 else 'Negative'

    return jsonify({
        'sentiment': sentiment_label,
        'likes': float(likes_pred),
        'retweets': float(retweet_pred)  # NEW
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
