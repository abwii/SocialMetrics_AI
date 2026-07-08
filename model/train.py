import sys
import os
import pandas as pd
import pickle

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db.database import get_connection

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def load_data():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT text, positive FROM tweets")
    rows = cursor.fetchall()

    conn.close()

    df = pd.DataFrame(rows)
    return df

def train():
    df = load_data()

    X = df["text"]
    y = df["positive"]

    vectorizer = TfidfVectorizer(max_features=5000)
    X_vec = vectorizer.fit_transform(X)

    model = LogisticRegression(max_iter=1000, class_weight="balanced")
    model.fit(X_vec, y)

    pickle.dump(model, open("model/model.pkl", "wb"))
    pickle.dump(vectorizer, open("model/vectorizer.pkl", "wb"))

    print("Model trained successfully!")

if __name__ == "__main__":
    train()