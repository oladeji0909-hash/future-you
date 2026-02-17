import sqlite3

# Connect to database
conn = sqlite3.connect('futureyou.db')
cursor = conn.cursor()

# Delete all users except admin (email: oladejo0909@gmail.com)
cursor.execute("DELETE FROM users WHERE email != 'oladejo0909@gmail.com'")

# Show remaining users
cursor.execute("SELECT id, email, full_name, is_admin FROM users")
users = cursor.fetchall()

print("Remaining users:")
for user in users:
    print(f"ID: {user[0]}, Email: {user[1]}, Name: {user[2]}, Admin: {user[3]}")

# Commit and close
conn.commit()
conn.close()

print("\n✅ All non-admin users deleted!")
