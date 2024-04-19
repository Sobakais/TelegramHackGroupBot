import sqlite3 as sq
from resources.config import path_to_db


def init_db(members):
    with sq.connect(path_to_db) as con:
        cursor = con.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            nickname TEXT,
            chanceFuck INTEGER DEFAULT 0)""")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS hacks(
        day integer,
        month integer,
        year integer,
        name text,
        description text,
        state text DEFAULT '🚫')""")

        cursor.execute(""" CREATE TABLE IF NOT EXISTS responses(
        id INTEGER PRIMARY KEY,
        respondlist TEXT NOT NULL)""")

        cursor.executemany(
            "INSERT OR REPLACE INTO users (id, nickname) VALUES (?, ?)", members
        )


def add_respond(userid, lines):
    with sq.connect(path_to_db) as con:
        cursor = con.cursor()
        cursor.execute(
            f"""INSERT OR REPLACE INTO responses (respondlist) VALUES (?) WHERE id = {userid}""",
            lines,
        )


def get_responds(userid):
    with sq.connect(path_to_db) as con:
        cursor = con.cursor()
        cursor.execute(
            f"SELECT respondlist FROM responses WHERE id = {userid}")
        cursor.execute(
            f"SELECT respondlist FROM responses WHERE id = {userid}")

        responds = cursor.fetchone()
        if responds is None:
            return []
        return responds[0].split("_")


def get_user(tgid):
    with sq.connect(path_to_db) as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (tgid,))
        return cursor.fetchone()


def set_chance(tgid, chance):
    with sq.connect(path_to_db) as con:
        cursor = con.cursor()
        if tgid.isdigit():
            cursor.execute(
                "UPDATE users SET chanceFuck = ? WHERE id = ?", (chance, tgid)
            )
        else:
            cursor.execute(
                "UPDATE users SET chanceFuck = ? WHERE nickname = ?", (
                    chance, tgid)
            )


def chng_nick(tgid, newNick):
    with sq.connect(path_to_db) as con:
        cursor = con.cursor()
        cursor.execute(
            "UPDATE users SET nickname = ? WHERE id = ?", (newNick, tgid))


def get_nick(tgid):
    with sq.connect(path_to_db) as con:
        cursor = con.cursor()
        cursor.execute(f"SELECT nickname FROM users WHERE id = '{tgid}'")
        nick = cursor.fetchone()
        if nick is None:
            return "No subject"
        return f"Nick: {nick[0]}"


def show_all():
    with sq.connect(path_to_db) as con:
        cursor = con.cursor()
        cursor.execute("SELECT * FROM users WHERE nickname IS NOT NULL")
        users = cursor.fetchall()
        respond = ""
        for user in users:
            respond += f"ID: {user[0]} | Nick: {user[1]}\n"
        return respond


def add_hack(date, name, description):
    with sq.connect(path_to_db) as con:
        cursor = con.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO hacks (day, month, year, name, description) VALUES (?, ?, ?, ?, ?)",
            (date[0], date[1], date[2], name, description),
        )


def get_hacks():
    with sq.connect(path_to_db) as con:
        cursor = con.cursor()
        cursor.execute("SELECT rowid, * FROM hacks")
        hacks = cursor.fetchall()
        return hacks


def get_hack(rowid):
    with sq.connect(path_to_db) as con:
        cursor = con.cursor()
        cursor.execute(
            "SELECT rowid, * FROM hacks WHERE rowid = ?", (str(rowid)))
        hack = cursor.fetchone()
        return hack


def set_hack_name(rowid, name):
    with sq.connect(path_to_db) as con:
        cursor = con.cursor()
        cursor.execute(
            "UPDATE hacks SET name = ? WHERE rowid = ?", (name, rowid))


def set_hack_date(rowid, date):
    with sq.connect(path_to_db) as con:
        cursor = con.cursor()
        cursor.execute(
            "UPDATE hacks SET day = ?, month = ?, year = ? WHERE rowid = ?",
            (date[0], date[1], date[2], rowid),
        )


def set_hack_description(rowid, description):
    with sq.connect(path_to_db) as con:
        cursor = con.cursor()
        cursor.execute(
            "UPDATE hacks SET description = ? WHERE rowid = ?", (
                description, rowid)
        )


def set_hack_status(rowid, status):
    with sq.connect(path_to_db) as con:
        cursor = con.cursor()
        cursor.execute(
            "UPDATE hacks SET state = ? WHERE rowid = ?", (status, rowid))
        cursor = con.cursor()
        cursor.execute("DELETE FROM hacks WHERE rowid = ?", (rowid))
    with sq.connect(path_to_db) as con:
        cursor = con.cursor()
        cursor.execute("DELETE FROM hacks WHERE rowid = ?", (rowid))
