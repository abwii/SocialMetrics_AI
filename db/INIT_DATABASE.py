from database import get_connection

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("CREATE DATABASE IF NOT EXISTS socialmetrics")
    cursor.execute("USE socialmetrics")

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tweets (
        id INT AUTO_INCREMENT PRIMARY KEY,
        text TEXT NOT NULL,
        positive TINYINT DEFAULT 0,
        negative TINYINT DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()

    print("DB initialized!")

if __name__ == "__main__":
    init_db()