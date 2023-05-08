import sqlite3
   
#DEFINING CONNECTI0N TO DB AND ITS CURSOR
connection = sqlite3.connect('WhatsappTaxiOrg.db')
cursor = connection.cursor()

#CRETAING TABLES IN DB
#CUSTOMER TABLE
command1 = """CREATE TABLE IF NOT EXISTS
customers(phone_number INTEGER , driver_ID INTEGER ,date_and_time TEXT PRIMARY KEY, city TEXT, 
FOREIGN KEY(driver_ID) REFERENCES drivers(driver_ID))"""

cursor.execute(command1)

#DRIVERS TABLE
command2 = """CREATE TABLE IF NOT EXISTS
drivers(driver_ID INTEGER PRIMARY KEY, name TEXT, phone_number INTEGEER, vehicle_number INTEGER, status TEXT,
FOREIGN KEY(vehicle_number) REFERENCES taxis(vehicle_number))"""

cursor.execute(command2)

#TAXI TABLE
command3 = """CREATE TABLE IF NOT EXISTS
taxis(vehicle_number INT PRIMARY KEY, number_plate TEXT, color TEXT, model TEXT)"""

cursor.execute(command3)



#CRUD OPERATIONS
#ADD TO DRIVERS
#cursor.execute("INSERT INTO drivers VALUES (101, 'Vambe E', +263777437080, 201, 'free')")
#cursor.execute("INSERT INTO drivers VALUES (102,'Muchada M', +263714175327, 202, 'free')")


#connection.commit()

#ADD TO CUSTOMERS
#cursor.execute("INSERT INTO customers (phone_number, premium) VALUES (+263774969384, 'yes')")
#cursor.execute("INSERT INTO customers (phone_number) VALUES (+263774969384)")
#cursor.execute("DELETE FROM customers WHERE phone_number = 263774969384 ")
#connection.commit()

#ADD TO TAXIS
#cursor.execute("INSERT INTO taxis VALUES (201, 'H19019E', 'green', '2009 Volve mario')")
#cursor.execute("INSERT INTO taxis VALUES (202, 'H190455T', 'green', '2009 Volve brandy')")
#cursor.execute("INSERT INTO taxis VALUES (203, 'H190456B', 'green', '2009 Volve vodka')")
#cursor.execute("INSERT INTO taxis VALUES (204, 'H190525Z', 'green', '2009 Volve vodka')")
#cursor.execute("INSERT INTO taxis VALUES (205, 'H190850X', 'green', '2009 Volve brandy')")
#cursor.execute("INSERT INTO taxis VALUES (206, 'H190392Q', 'green', '2009 Volve mario')")
#connection.commit()








#FETCHING INFO FROM THE DB
#FECTING FROM DRIVERS
# cursor.execute("SELECT * FROM drivers")
# print("DRIVERS")
# for raw in cursor:
#     print(raw)

# #FECTING FROM CUSTOMERS
# cursor.execute("SELECT * FROM customers")
# print("CUSTOMERS")
# for raw in cursor:
#     print(raw)

# #FECTING FROM TAXIS
# cursor.execute("SELECT * FROM taxis")
# print("TAXIS")
# for raw in cursor:
#     print(raw)







