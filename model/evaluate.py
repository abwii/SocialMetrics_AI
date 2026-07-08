import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
import matplotlib
matplotlib.use("Agg")  # backend sans interface graphique, pour sauvegarder les images
import matplotlib.pyplot as plt

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, classification_report

from db.database import get_connection
from utils.preprocess import clean_text

# dossier ou sauvegarder les figures
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")
os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_data():
    """Charge les tweets annotes depuis la base."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT text, positive, negative FROM tweets")
    rows = cursor.fetchall()
    conn.close()
    return pd.DataFrame(rows)


def save_confusion_matrix(y_true, y_pred, labels, title, filename):
    """Genere et sauvegarde une matrice de confusion."""
    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(cmap="Blues", values_format="d")
    plt.title(title)
    path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(f"Matrice sauvegardee : {path}")
    return cm


def evaluate_label(df, label_column, label_name, positive_name, negative_name, filename):
    """Entraine et evalue le modele pour une colonne de label donnee."""
    print(f"\n===== Evaluation : {label_name} =====")

    X = df["text"].apply(clean_text)
    y = df[label_column]

    # decoupage train / validation (80 / 20), stratifie pour garder l'equilibre des classes
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_val_vec = vectorizer.transform(X_val)

    model = LogisticRegression(max_iter=1000, class_weight="balanced")
    model.fit(X_train_vec, y_train)

    y_pred = model.predict(X_val_vec)

    # matrice de confusion
    save_confusion_matrix(
        y_val, y_pred,
        labels=[negative_name, positive_name],
        title=f"Matrice de confusion - {label_name}",
        filename=filename,
    )

    # metriques : precision, rappel, f1-score
    print("\nRapport de classification :")
    print(classification_report(
        y_val, y_pred,
        target_names=[negative_name, positive_name],
        zero_division=0,
    ))


def main():
    df = load_data()
    print(f"{len(df)} tweets charges depuis la base.")

    # ticket : matrice + metriques pour les predictions positives
    evaluate_label(
        df,
        label_column="positive",
        label_name="Predictions positives",
        positive_name="positif",
        negative_name="non positif",
        filename="confusion_positive.png",
    )

    # ticket : matrice + metriques pour les predictions negatives
    evaluate_label(
        df,
        label_column="negative",
        label_name="Predictions negatives",
        positive_name="negatif",
        negative_name="non negatif",
        filename="confusion_negative.png",
    )


if __name__ == "__main__":
    main()
