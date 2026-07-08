from flask import Flask, request, jsonify

from utils.preprocess import clean_text
import pickle

app = Flask(__name__)

# chargement du modele et du vectorizer
model = pickle.load(open("model/model.pkl", "rb"))
vectorizer = pickle.load(open("model/vectorizer.pkl", "rb"))


def sentiment_score(proba_positive):
    """Convertit une probabilite [0, 1] en score de sentiment [-1, 1]."""
    return round(2 * proba_positive - 1, 4)


@app.route("/predict", methods=["POST"])
def predict():
    # le corps doit etre du JSON valide
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Request body must be valid JSON"}), 400

    # la cle tweets doit etre presente
    if "tweets" not in data:
        return jsonify({"error": "Missing 'tweets' field"}), 400

    tweets = data["tweets"]

    # tweets doit etre une liste non vide
    if not isinstance(tweets, list) or len(tweets) == 0:
        return jsonify({"error": "'tweets' must be a non-empty list"}), 400

    # chaque element doit etre une chaine non vide
    for tweet in tweets:
        if not isinstance(tweet, str) or tweet.strip() == "":
            return jsonify({"error": "Each tweet must be a non-empty string"}), 400

    results = {}
    for tweet in tweets:
        clean = clean_text(tweet)
        vec = vectorizer.transform([clean])
        proba_positive = model.predict_proba(vec)[0][1]
        results[tweet] = sentiment_score(proba_positive)

    return jsonify(results)


if __name__ == "__main__":
    app.run(debug=True)