import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from db.database import get_server_connection, DB_NAME


def init_db():
    conn = get_server_connection()
    cursor = conn.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    cursor.execute(f"USE {DB_NAME}")

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