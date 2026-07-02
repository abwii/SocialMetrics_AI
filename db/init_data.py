from database import get_connection

def seed_data():
    conn = get_connection()
    cursor = conn.cursor()

    data = [
        ("I love this product", 1, 0),
        ("This is amazing", 1, 0),
        ("I am very happy", 1, 0),
        ("Worst experience ever", 0, 1),
        ("I hate this so much", 0, 1),
        ("This is terrible", 0, 1),
        ("Not bad at all", 1, 0),
        ("I feel great today", 1, 0),
        ("This is disappointing", 0, 1),
        ("Absolutely fantastic", 1, 0),
    ]

    cursor.executemany(
        "INSERT INTO tweets (text, positive, negative) VALUES (%s, %s, %s)",
        data
    )

    conn.commit()
    conn.close()

    print("Data inserted!")

if __name__ == "__main__":
    seed_data()