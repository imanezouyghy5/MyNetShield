import sqlite3
import os

DB_PATH = "netshield_security.db"

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found. No migration needed.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Check if password_hash exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [row[1] for row in cursor.fetchall()]
        
        if not columns:
            print("Users table does not exist. Persistence.py will create it.")
        elif "password_hash" not in columns:
            print("Adding password_hash column to users table...")
            cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT NOT NULL DEFAULT ''")
            conn.commit()
            print("Migration successful.")
        else:
            print("Users table already has password_hash column.")
            
    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
