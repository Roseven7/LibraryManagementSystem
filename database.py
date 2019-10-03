import sqlite3


def createDatabase():
    """
    creates new database

    """
    con = sqlite3.connect("library.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS book(id INTEGER PRIMARY KEY, title text, author text, releaseDate char, releasePlace text, pages int, ISBN char)")
    con.commit()
    con.close()


def addBookRec(title, author, releaseDate, releasePlace, pages, ISBN):
    """
    creates a new record in the database

    """
    con = sqlite3.connect("library.db")
    cur = con.cursor()
    cur.execute("INSERT INTO book VALUES (NULL, ?, ?, ?, ?, ?, ?)", (title, author, releaseDate, releasePlace, pages, ISBN))
    con.commit()
    con.close()


def viewData():
    """
    displays data from the database

    """
    con = sqlite3.connect("library.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM book")
    row = cur.fetchall()
    con.close()
    return row


def deleteRec(id):
    """
    deletes record with given id

    """
    con = sqlite3.connect("library.db")
    cur = con.cursor()
    cur.execute("DELETE FROM book WHERE id = ?", (id,))
    con.commit()
    con.close()


def searchRec(title="", author="", releaseDate="", releasePlace="", pages="", ISBN=""):
    """
    searches the database if any of the parameters is given

    """
    con = sqlite3.connect("library.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM book WHERE title=? OR author=? OR releaseDate=? OR releasePlace=? OR pages=? OR ISBN=?", (title, author, releaseDate, releasePlace, pages, ISBN))
    row = cur.fetchall()
    con.close()
    return row


def updateRec(title="", author="", releaseDate="", releasePlace="", pages="", ISBN="", id=""):
    """
    updates record in the database

    """
    con = sqlite3.connect("library.db")
    cur = con.cursor()
    cur.execute(
        "UPDATE book SET title=?, author=?, releaseDate=?, releasePlace=?, pages=?, ISBN=? WHERE id=?",
        (title, author, releaseDate, releasePlace, pages, ISBN, id))
    con.commit()
    con.close()


createDatabase()
