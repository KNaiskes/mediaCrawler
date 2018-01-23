import sqlite3
import os.path
import hashlib

database = "db/users.db"

def createDB():
	conn = sqlite3.connect(database)
	db = conn.cursor()
	db.execute("""CREATE TABLE IF NOT EXISTS users
	(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
	username TEXT NOT NULL, password TEXT NOT NULL)""")
	conn.commit()
	db.close()

def encryptPass(encrypt):
	password = hashlib.sha256()
	password = hashlib.sha256(encrypt.encode("utf8")).hexdigest()
	return password

def userExists(username, password):
	conn = sqlite3.connect(database)
	db = conn.cursor()
	if password == None:
		db.execute("SELECT * FROM users WHERE username = ?",(username,))
	else:
		password = encryptPass(password)
		db.execute("SELECT * FROM users WHERE username = ? AND password = ?",(username, password,))

	exists = db.fetchone()
	db.close()
	if exists is None:
		return False
	return True

"""
def addUser(username, password):
	if userExists(username) == True:
		print("user: {} already exists".format(username))
	else:
		password = encryptPass(password)
		conn = sqlite3.connect(database)
		db = conn.cursor()
		db.execute("INSERT INTO users VALUES(?,?,?)",(None,username, password))
		conn.commit()
		db.close()
"""
