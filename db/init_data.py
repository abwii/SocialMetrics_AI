import sys
import os
import json
 
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
 
from db.database import get_connection

def load_tweets():
    """Charge les tweets annotes depuis le fichier JSON."""
    path = os.path.join(os.path.dirname(__file__), "tweets.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
 
 
def seed_data():
    tweets = load_tweets()
 
    conn = get_connection()
    cursor = conn.cursor()
 
    # on vide la table pour eviter les doublons a chaque execution
    cursor.execute("DELETE FROM tweets")
 
    data = [(t["text"], t["positive"], t["negative"]) for t in tweets]
 
    cursor.executemany(
        "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)",
        data
    )
 
    conn.commit()
    conn.close()
 
    print(f"{len(data)} tweets inserted!")


if __name__ == "__main__":
    seed_data()