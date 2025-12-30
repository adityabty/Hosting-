import sqlite3

con = sqlite3.connect("hosting.db", check_same_thread=False)
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY,
tg_id INTEGER UNIQUE,
credits INTEGER DEFAULT 0
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS bots(
id INTEGER PRIMARY KEY,
user_id INTEGER,
bot_type TEXT,
folder TEXT,
process_name TEXT,
status TEXT,
FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

con.commit()


def get_or_create_user(tg_id):
    cur.execute("SELECT * FROM users WHERE tg_id=?", (tg_id,))
    user = cur.fetchone()
    if not user:
        cur.execute("INSERT INTO users(tg_id, credits) VALUES(?, 0)", (tg_id,))
        con.commit()
        return get_or_create_user(tg_id)
    return user


def update_credits(tg_id, new_value):
    cur.execute("UPDATE users SET credits=? WHERE tg_id=?", (new_value, tg_id))
    con.commit()


def add_bot(user_id, bot_type, folder, process):
    cur.execute(
        "INSERT INTO bots(user_id, bot_type, folder, process_name, status) VALUES(?,?,?,?,?)",
        (user_id, bot_type, folder, process, "running"),
    )
    con.commit()
