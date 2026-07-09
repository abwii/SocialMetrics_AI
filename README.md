# SocialMetrics AI — Sentiment Analysis API

## 📌 Contexte

SocialMetrics AI est une entreprise fictive spécialisée dans l’analyse de données issues des réseaux sociaux.

Le client, **Daunale Treupe**, souhaite surveiller les opinions exprimées sur X (anciennement Twitter).

L’objectif du projet est de concevoir un service capable d’analyser automatiquement le sentiment des tweets à partir de leur contenu.

---

## 🎯 Objectifs du projet

- Développer une API REST avec Flask permettant l’analyse de sentiments
- Implémenter un modèle de machine learning basé sur la régression logistique
- Utiliser une base de données MySQL pour stocker des tweets annotés
- Mettre en place un pipeline de traitement des données textuelles
- Générer et analyser des métriques de performance du modèle (matrice de confusion, précision, rappel, F1-score)
- Prévoir un mécanisme de réentraînement du modèle avec de nouvelles données

---

## ⚙️ Technologies utilisées

- Python 3
- Flask
- Scikit-learn
- Pandas
- NumPy
- MySQL / MariaDB
- TF-IDF Vectorizer

---

## 🧠 Architecture du projet

```text
SocialMetrics_AI/
│
├── app.py
├── .gitignore
├── README.md
│
├── db/
│   ├── database.py
│   ├── INIT_DATABASE.py
│   └── init_data.py
│
├── model/
│   └── train.py
│
├── utils/
│   └── preprocess.py
│
└── tests/
    ├── test_app.py
    └── test_preprocess.py
```

> **Note :** Les fichiers `model.pkl` et `vectorizer.pkl` sont générés automatiquement lors de l'entraînement du modèle et ne sont pas versionnés.

---

## 🚀 Installation

### 1. Cloner le projet

```bash
git clone <repo-url>
cd SocialMetrics_AI
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

## 🗄️ Initialisation de la base de données

### 1. Créer la base de données et la table

```bash
python db/INIT_DATABASE.py
```

### 2. Insérer les données d'entraînement

```bash
python db/init_data.py
```

---

## 🤖 Entraînement du modèle

```bash
python model/train.py
```

Cette commande génère automatiquement les fichiers :

- `model/model.pkl`
- `model/vectorizer.pkl`

---

## 🌐 Lancer l'API

```bash
python app.py
```

L'API sera disponible à l'adresse :

```text
http://127.0.0.1:5000
```

---

## 📡 Endpoint API

### `POST /predict`

Analyse une liste de tweets et retourne un score de sentiment.

#### Exemple de requête

```json
{
  "tweets": [
    "I love this product",
    "This is terrible"
  ]
}
```

#### Exemple de réponse

```json
{
  "I love this product": 1,
  "This is terrible": -1
}
```

---

## 📊 Modèle de Machine Learning

- **Algorithme :** Logistic Regression
- **Vectorisation :** TF-IDF
- **Sortie :**
  - `1` → sentiment positif
  - `-1` → sentiment négatif

---

## ✅ Tests

Le projet contient des tests unitaires (`pytest`) couvrant :

- L'endpoint `POST /predict` : cas nominal (tweets valides, un ou plusieurs) et cas d'erreur (JSON invalide, champ `tweets` manquant, `tweets` vide/mal typé, tweet vide).
- Le pipeline de preprocessing (`utils/preprocess.py`) : mise en minuscule, suppression des URLs, de la ponctuation/chiffres, normalisation des espaces.

### Lancer les tests

Depuis la racine du projet :

```bash
pytest
```

Pour un rapport plus détaillé :

```bash
pytest -v
```

Pour lancer uniquement un fichier de test précis :

```bash
pytest tests/test_app.py
pytest tests/test_preprocess.py
```

---

## 🔄 Améliorations possibles

- Ajout d'une classe **neutre**
- Réentraînement automatique via une tâche planifiée (cron)
- Utilisation de modèles plus avancés (Word2Vec, BERT, etc.)
- Enrichissement du dataset d'entraînement
- Évaluation détaillée avec matrices de confusion et métriques (précision, rappel, F1-score)

---

## 👥 Auteurs

- Wassim BACHA
- Jimmy LETTE-VOUETO
- Christian MICELA
- Timothé PEYREGNE

Projet réalisé en groupe dans le cadre d’un TP de Machine Learning & API
