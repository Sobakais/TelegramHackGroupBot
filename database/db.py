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
        cursor.executemany(
            "INSERT OR REPLACE INTO users (id, nickname) VALUES (?, ?)", members
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
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS hacks (
        day integer,
        month integer,
        year integer,
        name text,
        description text
        )
        """)
        cursor.execute(
            "INSERT OR REPLACE INTO hacks VALUES (?, ?, ?, ?, ?)",
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
        cursor.execute("SELECT rowid, * FROM hacks WHERE rowid = ?", (rowid))
        hacks = cursor.fetchall()
        return hacks


def delete_hack(rowid):
    with sq.connect(path_to_db) as con:
        cursor = con.cursor()
        cursor.execute("DELETE FROM hacks WHERE rowid = ?", (rowid))
