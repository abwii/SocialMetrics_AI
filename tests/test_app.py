import pytest

import app as app_module


class FakeVectorizer:
    """Vectorizer factice : renvoie le texte nettoye tel quel (pas de vraie vectorisation)."""

    def transform(self, texts):
        return texts


class FakeModel:
    """Modele factice : renvoie une probabilite positive controlee par test via proba_map."""

    def __init__(self, proba_map, default_proba=0.5):
        self.proba_map = proba_map
        self.default_proba = default_proba

    def predict_proba(self, texts):
        proba = self.proba_map.get(texts[0], self.default_proba)
        return [[1 - proba, proba]]


@pytest.fixture
def make_client(monkeypatch):
    """Fixture permettant de creer un client de test avec un modele/vectorizer factices."""

    def _make(proba_map=None, default_proba=0.5):
        monkeypatch.setattr(app_module, "vectorizer", FakeVectorizer())
        monkeypatch.setattr(app_module, "model", FakeModel(proba_map or {}, default_proba))
        app_module.app.testing = True
        return app_module.app.test_client()

    return _make


# ---------- cas nominaux ----------

def test_predict_single_tweet_positive(make_client):
    client = make_client(proba_map={"i love this product": 0.95})

    response = client.post("/predict", json={"tweets": ["I love this product"]})

    assert response.status_code == 200
    data = response.get_json()
    assert data == {"I love this product": 0.9}


def test_predict_single_tweet_negative(make_client):
    client = make_client(proba_map={"this is terrible": 0.1})

    response = client.post("/predict", json={"tweets": ["This is terrible"]})

    assert response.status_code == 200
    data = response.get_json()
    assert data == {"This is terrible": -0.8}


def test_predict_multiple_tweets(make_client):
    client = make_client(proba_map={
        "great news today": 0.8,
        "worst day ever": 0.2,
    })

    response = client.post("/predict", json={"tweets": ["Great news today", "Worst day ever"]})

    assert response.status_code == 200
    data = response.get_json()
    assert set(data.keys()) == {"Great news today", "Worst day ever"}
    assert data["Great news today"] == 0.6
    assert data["Worst day ever"] == -0.6


# ---------- cas d'erreur ----------

def test_predict_invalid_json_body(make_client):
    client = make_client()

    response = client.post("/predict", data="not a json body", content_type="application/json")

    assert response.status_code == 400
    assert response.get_json()["error"] == "Request body must be valid JSON"


def test_predict_missing_tweets_field(make_client):
    client = make_client()

    response = client.post("/predict", json={})

    assert response.status_code == 400
    assert response.get_json()["error"] == "Missing 'tweets' field"


def test_predict_tweets_not_a_list(make_client):
    client = make_client()

    response = client.post("/predict", json={"tweets": "not a list"})

    assert response.status_code == 400
    assert response.get_json()["error"] == "'tweets' must be a non-empty list"


def test_predict_tweets_empty_list(make_client):
    client = make_client()

    response = client.post("/predict", json={"tweets": []})

    assert response.status_code == 400
    assert response.get_json()["error"] == "'tweets' must be a non-empty list"


def test_predict_tweet_not_a_string(make_client):
    client = make_client()

    response = client.post("/predict", json={"tweets": ["valid tweet", 123]})

    assert response.status_code == 400
    assert response.get_json()["error"] == "Each tweet must be a non-empty string"


def test_predict_tweet_blank_string(make_client):
    client = make_client()

    response = client.post("/predict", json={"tweets": ["   "]})

    assert response.status_code == 400
    assert response.get_json()["error"] == "Each tweet must be a non-empty string"


def test_predict_wrong_http_method(make_client):
    client = make_client()

    response = client.get("/predict")

    assert response.status_code == 405
