from flask import Flask, request, jsonify
import pickle
import numpy as np

from utils.preprocess import clean_text

app = Flask(__name__)

# load model
model = pickle.load(open("model/model.pkl", "rb"))
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))

def sentiment_score(pred):
    return 1 if pred == 1 else -1

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    # validation input
    if not data or "tweets" not in data:
        return jsonify({"error": "Missing 'tweets' field"}), 400

    tweets = data["tweets"]

    if not isinstance(tweets, list) or len(tweets) == 0:
        return jsonify({"error": "Tweets must be a non-empty list"}), 400

    results = {}

    for tweet in tweets:
        clean = clean_text(tweet)
        vec = vectorizer.transform([clean])
        pred = model.predict(vec)[0]

        results[tweet] = sentiment_score(pred)

    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)