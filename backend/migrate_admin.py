"""
Add is_admin column to users table
"""

import sqlite3

def migrate():
    conn = sqlite3.connect('futureyou.db')
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'is_admin' in columns:
            print("✅ Column 'is_admin' already exists")
            return
        
        # Add is_admin column
        cursor.execute("ALTER TABLE users ADD COLUMN is_admin BOOLEAN DEFAULT 0")
        conn.commit()
        
        print("✅ Successfully added 'is_admin' column to users table")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
