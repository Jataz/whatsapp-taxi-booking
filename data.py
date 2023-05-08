import sqlite3

def total_Drivers():
    con = sqlite3.connect('WhatsappTaxiOrg.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM drivers").rowcount
    rows = cur.fetchall()
    total = (len(rows))
    return total

def total_Taxis():
    con = sqlite3.connect('WhatsappTaxiOrg.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM taxis")
    rows = cur.fetchall()
    total = (len(rows))
    return total

def total_Customers():
    con = sqlite3.connect('WhatsappTaxiOrg.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM customers")
    rows = cur.fetchall()
    total = (len(rows))
    return total

def total_Users():
    con = sqlite3.connect('WhatsappTaxiOrg.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    total = (len(rows))
    return total

        

