import sqlite3
import requests

userDB = sqlite3.connect('basement_userbase.db', isolation_level=None)
cur = userDB.cursor()

cur.execute("CREATE TABLE userbase(id INTEGER PRIMARY KEY, username TEXT, mc_username TEXT, mc_id TEXT)") # Remove after developement is complete
cur.execute("PRAGMA journal_mode=WAL")

def checkpoint_db():
    cur.execute("PRAGMA wal_checkpoint(FULL)")

def user_exists(userid):
    cur.execute("SELECT id FROM userbase WHERE id=?", (userid,))
    data = cur.fetchall()
    if not data:
        print("User does not exist")
        return False
    else:
        print("User exists")
        return True

def user_create(userid, username):
    cur.execute("INSERT INTO userbase(id, username) VALUES(?, ?)", (userid, username,))
    print(f"Added user {username} with id {userid} to database")

def add_minecraft_user(userid, mcusername):
    cur.execute("SELECT mc_username FROM userbase WHERE id=?", (userid,))
    data = cur.fetchall()
    print(data)

    cur.execute("UPDATE userbase SET mc_username=? WHERE id=?", (mcusername, userid,)) 
    # Get Minecraft ID from API
    mc_id_api_call = requests.get("https://api.mojang.com/users/profiles/minecraft/" + mcusername)
    if mc_id_api_call.status_code == 200 and not data:
        data = mc_id_api_call.json()
        mc_id = data["id"]
        cur.execute("UPDATE userbase SET mc_id=? WHERE id=?", (mc_id, userid,))
        return mcusername
    elif mc_id_api_call.status_code != 200:
        return 404
    elif mc_id_api_call.status_code == 200 and data[0][0] != None:
        return 405

    checkpoint_db()

def remove_minecraft_user(userid):
    cur.execute("SELECT mc_username FROM userbase WHERE id=?", (userid,))
    data = cur.fetchall()
    if not data:
        return False
    else:
        tmp = data[0][0]
        cur.execute("UPDATE userbase SET mc_username=?, mc_id=? WHERE id=?", (None, None, userid,))
        return tmp
