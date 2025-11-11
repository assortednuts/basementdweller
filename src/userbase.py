import sqlite3
import requests

userDB = sqlite3.connect('basement_userbase.db', isolation_level=None)
cur = userDB.cursor()

cur.execute("CREATE TABLE userbase(id INTEGER PRIMARY KEY, username TEXT, mc_username TEXT, mc_id TEXT, mc_version TEXT)") # Remove after developement is complete
cur.execute("PRAGMA journal_mode=WAL")

def checkpoint_db():
    cur.execute("PRAGMA wal_checkpoint(FULL)")
    userDB.commit()

def user_exists(userid):
    cur.execute("SELECT id FROM userbase WHERE id=?", (userid,))
    data = cur.fetchall()
    if not data:
        print("User does not exist")
        return False
    else:
        print("User exists")
        return True

def read_info(userid, column):
    cur.execute("SELECT ? FROM userbase WHERE id=?", (column, userid,))
    data = cur.fetchall()
    return data[0][0]

def user_create(userid, username):
    cur.execute("INSERT INTO userbase(id, username) VALUES(?, ?)", (userid, username,))
    checkpoint_db()
    print(f"Added user {username} with id {userid} to database")

def add_minecraft_user(userid, mcusername, version):
    cur.execute("SELECT mc_username FROM userbase WHERE id=?", (userid,))
    data = cur.fetchall()
    print(data)

    if data and data[0][0] is not None:
        return 405

    # Get Minecraft ID from API
    mc_id_api_call = requests.get("https://api.mojang.com/users/profiles/minecraft/" + mcusername)
    uuid_index = "id"

    if mc_id_api_call.status_code != 200 or version == 'bedrock':
        mc_id_api_call = requests.get("https://mcprofile.io/api/v1/bedrock/gamertag/" + mcusername)
        if mc_id_api_call.status_code != 200:
            return 404
        else:
            mcusername = "." + mcusername
            uuid_index = "floodgateuid"
            version = 'bedrock'
    else:
        version = 'java'
    info = mc_id_api_call.json()
    mc_id = info[uuid_index]
    cur.execute("UPDATE userbase SET mc_username=?, mc_id=?, mc_version=? WHERE id=?", (mcusername, mc_id, version, userid,))
    print(data)
    checkpoint_db()
    return mcusername

def remove_minecraft_user(userid):
    cur.execute("SELECT mc_username FROM userbase WHERE id=?", (userid,))
    data = cur.fetchall()
    if not data:
        return None
    else:
        tmp = data[0][0]
        if read_info(userid, 'version') == 'bedrock':
            tmp = "." + tmp
        cur.execute("UPDATE userbase SET mc_username=?, mc_id=?, mc_version=? WHERE id=?", (None, None, None, userid,))
        checkpoint_db()
        return tmp
