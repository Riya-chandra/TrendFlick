import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression, LogisticRegression
import joblib

# Load dataset
data = pd.read_csv('sentimentdataset.csv')

# Clean and prepare data
data['Sentiment'] = data['Sentiment'].str.strip().str.lower()
data['sentiment_label'] = data['Sentiment'].apply(lambda x: 1 if x == 'positive' else 0)

X = data['Text']
y_sentiment = data['sentiment_label']
y_likes = data['Likes'].astype(float)
y_retweets = data['Retweets'].astype(float)  # NEW

# Vectorize text
vectorizer = TfidfVectorizer(max_features=5000)
X_vec = vectorizer.fit_transform(X)

# Train models
clf = LogisticRegression(class_weight='balanced')
clf.fit(X_vec, y_sentiment)

reg_likes = LinearRegression()
reg_likes.fit(X_vec, y_likes)

reg_retweets = LinearRegression()  # NEW
reg_retweets.fit(X_vec, y_retweets)

# Save models
joblib.dump(vectorizer, 'vectorizer.joblib')
joblib.dump(clf, 'sentiment_model.joblib')
joblib.dump(reg_likes, 'likes_model.joblib')
joblib.dump(reg_retweets, 'retweet_model.joblib')  # NEW

print("All models trained and saved!")
