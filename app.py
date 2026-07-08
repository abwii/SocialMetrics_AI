from flask import Flask, request, jsonify
import pickle

from utils.preprocess import clean_text

app = Flask(__name__)

# chargement du modele et du vectorizer
model = pickle.load(open("model/model.pkl", "rb"))
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))


def sentiment_score(proba_positive):
    """Convertit une probabilite [0, 1] en score de sentiment [-1, 1]."""
    return round(2 * proba_positive - 1, 4)


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if not data or "tweets" not in data:
        return jsonify({"error": "Missing 'tweets' field"}), 400

    tweets = data["tweets"]

    if not isinstance(tweets, list) or len(tweets) == 0:
        return jsonify({"error": "Tweets must be a non-empty list"}), 400

    results = {}

    for tweet in tweets:
        clean = clean_text(tweet)
        vec = vectorizer.transform([clean])
        # proba de la classe positive (label 1)
        proba_positive = model.predict_proba(vec)[0][1]
        results[tweet] = sentiment_score(proba_positive)

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)