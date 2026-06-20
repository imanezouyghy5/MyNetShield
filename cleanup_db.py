import sqlite3
import os

db_path = r"c:\Users\DELL\Documents\MyNetShield\netshield_security.db"


def cleanup_db():
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # 1. Correct hostnames
        print("Standardizing hostnames...")
        cursor.execute(
            "UPDATE device_inventory SET hostname = 'iPhone' WHERE LOWER(hostname) IN ('iphon', 'iphon.')"
        )
        rows_affected = cursor.rowcount
        print(f"Updated {rows_affected} hostnames.")

        # 2. Fix vendors for iPhones with randomized MACs
        print("Fixing vendors for randomized MAC iPhones...")
        # Check randomized MAC pattern (LAA bit set - second char is 2, 6, A, E)
        cursor.execute("""
            UPDATE device_inventory 
            SET vendor = 'Apple (Anonymisé)' 
            WHERE hostname = 'iPhone' 
            AND (vendor = 'Fabricant inconnu' OR vendor = 'Appareil avec MAC privée/aléatoire' OR vendor IS NULL OR vendor = '')
            AND (
                SUBSTR(mac, 2, 1) IN ('2', '6', 'a', 'A', 'e', 'E')
            )
        """)
        rows_affected = cursor.rowcount
        print(f"Updated {rows_affected} vendors.")

        # 3. Handle Achraf-s-pc identification in DB if it's currently bad
        cursor.execute("""
            UPDATE device_inventory 
            SET vendor = '🖥️ Console Maître (NetShield Host)', device_type = '🖥️ Console Maître (NetShield Host)'
            WHERE mac = 'LOCAL_HOST'
        """)

        conn.commit()
        conn.close()
        print("Cleanup complete!")

    except Exception as e:
        print(f"Error during cleanup: {e}")


if __name__ == "__main__":
    cleanup_db()
