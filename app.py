from sqlite3.dbapi2 import connect
from flask import Flask,render_template, request, session, url_for, redirect,flash
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import requests
import random, os
import folium

import joblib
from textblob import TextBlob
from werkzeug.utils import secure_filename

import sqlite3
from datetime import datetime
import DBscripts as db
import functionData as fd

from geopy.geocoders import Nominatim
from geopy import distance
import time
from datetime import datetime
import data as dt


app = Flask(__name__)
app.secret_key = "this-is-a-secret-key"


td = dt.total_Drivers()
tt = dt.total_Taxis()
tc = dt.total_Customers()
tu = dt.total_Users()

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        con = sqlite3.connect("WhatsappTaxiOrg.db")
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        result = cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        if len(result.fetchall()) > 0:
            con.close()
            return render_template('dashboard.html',td=td,tt=tt,tc=tc,tu=tu)

        else:
            msg = 'Invalid Username or Password try again'
            con.close()
            return render_template('login.html', msg=msg)

@app.route('/dashboard')
def dashboard():
    m = folium.Map(location=[-17.833626443125766, 31.018526778543766],zoom_start=15)

    # Global tooltip
    tooltip = 'Click For More Info'

    # Create markers
    #BELVEEDERE ROUTE 
    folium.Marker([-17.836826157213498, 31.036866085965986],
                popup='<strong>TRANSERV</strong>',
                tooltip=tooltip).add_to(m),
    folium.Marker([-17.836274647348493, 31.030793564630603],
                popup='<strong>ZUPCO GARAGE</strong>',
                tooltip=tooltip).add_to(m),
    folium.Marker([-17.837490009415035, 31.027832405816874],
                popup='<strong>BISHOP GAU AVE</strong>',
                tooltip=tooltip).add_to(m),
    folium.Marker([-17.836254221020774, 31.02282203933199],
                popup='<strong>CHOPPIES BIG MALL</strong>',
                tooltip=tooltip).add_to(m),
    folium.Marker([-17.835539298213977, 31.019882338397764],
                popup='<strong>GANGES ROAD</strong>',
                tooltip=tooltip).add_to(m),
    folium.Marker([-17.838746215288378, 31.013670342222685],
                popup='<strong>GANGES ROAD</strong>',
                tooltip=tooltip).add_to(m),
    folium.Marker([-17.83996156052486, 31.008284466485048],
                popup='<strong>HIT</strong>',
                tooltip=tooltip).add_to(m),
    folium.Marker([-17.833626443125766, 31.018526778543766],
                popup='<strong>CHRIST MINISTRIES CHURCH</strong>',
                tooltip=tooltip).add_to(m),
    folium.Marker([-17.831762503650495, 31.015345678665767],
                popup='<strong>BLAKEWAY DRIVE</strong>',
                tooltip=tooltip).add_to(m),
    folium.Marker([-17.83394816219555, 31.009814963684946],
                popup='<strong>LAWLEY AVE</strong>',
                tooltip=tooltip).add_to(m),
    folium.Marker([-17.836364866766576, 31.00710056813469],
                popup='<strong>HIT</strong>',
                tooltip=tooltip).add_to(m)

    # BelvedereRoute = [(-17.833864324904955, 31.038711445690076),
    #         (-17.836611681332055, 31.037402527663726),
    #         (-17.836560615636404, 31.03687681472079),
    #         (-17.836264434183278, 31.03241361882764),
    #         (-17.836274647348493, 31.030793564630603),
    #         (-17.83552908498641, 31.02929152758492),
    #         (-17.837632992627796, 31.028229372793042),
    #         (-17.837490009415035, 31.027832405816874),
    #         (-17.836254221020774, 31.02282203933199),
    #         (-17.835539298213977, 31.019882338397764), #GANGES ROAD
    #         (-17.836540189360473, 31.019657032829194),
    #         (-17.837326599883895, 31.019152777523953),
    #         (-17.838746215288378, 31.013670342222685),
    #         (-17.839236439599656, 31.01150311736953),
    #         (-17.83996156052486, 31.008284466485048)]
    # BelvedereRoute2=[(-17.835539298213977, 31.019882338397764),
    #                 (-17.83476011732957, 31.018972025296527),
    #                 (-17.834045188456006, 31.018564329473865),
    #                 (-17.833534523257452, 31.018542871801873),
    #                 (-17.83271745589416, 31.018650160161823),
    #                 (-17.83234466766984, 31.01747535262206),
    #                 (-17.831762503650495, 31.015345678665767),
    #                 (-17.832559148655513, 31.014911160795485),
    #                 (-17.833223016766237, 31.01428888830692),
    #                 (-17.833830709253633, 31.013312564227576),
    #                 (-17.834009441951046, 31.0114779332655),
    #                 (-17.83394816219555, 31.009814963684946),
    #                 (-17.835066514508846, 31.00975059065261),
    #                 (-17.835168646772193, 31.008870826107668),
    #                 (-17.835949956785015, 31.007755027152417),
    #                 (-17.836364866766576, 31.00710056813469)
    #                 ]

    # folium.PolyLine(BelvedereRoute,
    #                 color='red',
    #                 weight=10,
    #                 opacity=0.8).add_to(m)
    # folium.PolyLine(BelvedereRoute2,
    #                 color='red',
    #                 weight=10,
    #                 opacity=0.8).add_to(m)

    # Generate map
    m.save('templates/map.html')
    return render_template("dashboard.html",td=td,tt=tt,tc=tc,tu=tu)

@app.route('/map')
def map():
    return render_template('map.html')

#--------------------------------------------------------------------------------------------- 
#--------------------------------------------------------------------------------------------- 
#view drivers in a table view drivers
@app.route('/viewDrivers')
def viewDrivers():
    con = sqlite3.connect('WhatsappTaxiOrg.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM drivers")
    rows = cur.fetchall()
    return render_template("viewDrivers.html", rows=rows )

#Adding new driver
@app.route('/add_Driver', methods=["POST"])
def add_Driver():
    con = sqlite3.connect("WhatsappTaxiOrg.db", timeout = 1)
    cur = con.cursor()
    if request.method == "POST":
        
        driverid= request.form['driverid']
        driverName = request.form['driverName']
        phoneNumber = request.form['phoneNumber']
        vehicleNumber = request.form['vehicleNumber']
        status = request.form['status']
        #driverPhoto = request.files['driverPhoto'].read()
        cur.execute(""" INSERT INTO drivers (driver_ID, driver_name, phone_number, vehicle_number,driver_status) VALUES(?,?,?,
                           ?,?)""", (driverid, driverName, phoneNumber, vehicleNumber, status))
        con.commit()
        flash("Driver Inserted Successfully")
        con.close()
        return redirect(url_for('viewDrivers'))

#update drivers
@app.route('/update', methods = ['POST','GET'])
def updateDriver():
    con = sqlite3.connect('WhatsappTaxiOrg.db',timeout=1)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    if request.method == 'POST':
        
        driverid= request.form['driverid']
        driverName = request.form['driverName']
        phoneNumber = request.form['phoneNumber']
        vehicleNumber = request.form['vehicleNumber']
        status = request.form['status']
        #driverPhoto = request.files['driverPhoto'].read()
        
        cur.execute("""UPDATE  drivers SET 
                    driver_name = ?,
                    phone_number =? , 
                    vehicle_number =?,
                    driver_status = ?
                    WHERE driver_ID=?""", (driverName, phoneNumber, vehicleNumber, status,driverid))
        con.commit()
        flash("Driver Updated Successfully")
        con.close()
        return redirect(url_for('viewDrivers'))   
        
    
#deleting driver
@app.route('/delete/<driver_ID>')
def delete(driver_ID):
    con = sqlite3.connect('WhatsappTaxiOrg.db',timeout=1)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("DELETE  FROM drivers WHERE driver_ID=? ",(driver_ID,))
    con.commit()
    flash("Driver Deleted Successfully")
    con.close()
    return redirect(url_for('viewDrivers'))

#---------------------------------------------------------------------------------------------    
#---------------------------------------------------------------------------------------------  
       

#view taxis in a table view taxis
@app.route('/viewTaxis')
def viewTaxis():
    con = sqlite3.connect('WhatsappTaxiOrg.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM taxis")
    rows = cur.fetchall()
    return render_template("viewTaxis.html", rows=rows )
   
#adding a new taxi
@app.route('/add_Taxi', methods=["POST"])
def add_Taxi():
    con = sqlite3.connect("WhatsappTaxiOrg.db",timeout=1)
    cur = con.cursor()
    if request.method == "POST":

        vehicleNumber= request.form['vehicleNumber']
        numberPlate = request.form['numberPlate']
        color = request.form['color']
        model = request.form['model']
       # taxiPhoto = request.files['taxiPhoto'].read()
        cur.execute(""" INSERT INTO taxis (vehicle_number, number_plate,color,model) VALUES(?,?,?,
                           ?)""", (vehicleNumber, numberPlate, color, model))
        con.commit()
        flash("Taxi Inserted Successfully")
        con.close()
        return redirect(url_for('viewTaxis'))
    
#update Taxi
@app.route('/update_Taxi' , methods = ['POST','GET'])
def updateTaxi():
    con = sqlite3.connect("WhatsappTaxiOrg.db",timeout=1)
    cur = con.cursor()
    if request.method == "POST":

        vehicleNumber= request.form['vehicleNumber']
        numberPlate = request.form['numberPlate']
        color = request.form['color']
        model = request.form['model']
        #taxiPhoto = request.files['taxiPhoto'].read()s
        cur.execute(""" UPDATE  taxis Set 
                    number_plate = ?,
                    color =?,
                    model =?
                    WHERE vehicle_number=?""", ( numberPlate, color, model,vehicleNumber))
        con.commit()
        flash("Taxi Updated Successfully")
        con.close()
        return redirect(url_for('viewTaxis'))
    
#deleting Taxi
@app.route('/delete_Taxi/<int:vehicle_number>')
def delete_Taxi(vehicle_number):
    con = sqlite3.connect('WhatsappTaxiOrg.db',timeout=1)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("DELETE  FROM taxis WHERE vehicle_number=? ",(vehicle_number,))
    con.commit()
    flash("Driver Deleted Successfully")
    con.close()
    return redirect(url_for('viewTaxis'))

#--------------------------------------------------------------------------------------------- 
#--------------------------------------------------------------------------------------------- 

#list of customers in a table
@app.route('/customersTable')
def customersTable():
    con = sqlite3.connect('WhatsappTaxiOrg.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM customers")
    rows = cur.fetchall()
    return render_template("customersTable.html", rows=rows )

#--------------------------------------------------------------------------------------------- 
#--------------------------------------------------------------------------------------------- 

#list of users of the system
@app.route('/viewUsers')
def viewUsers():
    con = sqlite3.connect('WhatsappTaxiOrg.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    return render_template("viewUsers.html", rows=rows )

#deleting User
@app.route('/delete_User/<int:id>')
def delete_User(id):
    con = sqlite3.connect('WhatsappTaxiOrg.db',timeout=1)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("DELETE  FROM users WHERE id=? ",(id,))
    con.commit()
    flash("Driver Deleted Successfully")
    con.close()
    return redirect(url_for('viewUsers'))

#--------------------------------------------------------------------------------------------- 
#--------------------------------------------------------------------------------------------- 

@app.route('/')
def logout():
    return render_template('login.html')



    #------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------
    #------------------------------------------------------------------------------



@app.route("/WhatsappTaxiBooking", methods=['POST'])
def booking():
    msg = request.form.get('Body').lower()
    global phone_number
    phone_number = request.form.get('From').replace("whatsapp:+", " ")
    global user_name
    user_name = request.form.get ('ProfileName')
    date = datetime.today()
    resp = MessagingResponse()

   # def countDown():
      



    if "taxi" in msg :
        number = request.form.get('From').replace("whatsapp:", " ")
        connection = sqlite3.connect('WhatsappTaxiOrg.db')
        cursor = connection.cursor()
        name_check = cursor.execute('SELECT * FROM customers WHERE phone_number=? AND premium = ?', (number,"yes"))

        #------------------EXISTING USER WITH PREMIUM ACCOUNT ----------------------------
        if len(name_check.fetchall()) > 0 :
            session["stage"] = "stage2.0"
            resp.message(f"*PREMIUM ACCOUNT*\nHello {user_name}.\n*Type in your option:*\n\n1.Book a taxi\n2.About Us\n🚕🚖🇿🇼🚕🚖\n") 

        #------------------NEW USER ----------------------------
        elif len(name_check.fetchall()) == 0 :
            session["stage"] = "stage2.1"
            resp.message(f"Hello {user_name}.\n*Welcome to Whatsapp Taxi Booking.*\n*Type in your option:*\n\n1.Book a taxi\n2.Register premium account\n3.About Us\n🚕🚖🇿🇼🚕🚖\n") 
        # connection.close()

    
    elif "stage" in session :
        stage = session["stage"]
        #----------------------- SESSION FOR NON PREMIUM ACCOUNTS-------------------------------------
        if stage == "stage2.1" and msg == "1":
            session["stage"] = "location"
            resp.message("*Share your location (use the whatsapp location feature)*📍")

        #------------------------- (option 2) premuim account-----------
        elif stage == "stage2.1" and msg == "2":
            session["stage"]= "premuim"
            resp.message("Premium reg is not available at the moment")

        #-------------------------(option 3 )About Us -----------
        elif stage == "stage2.1" and msg == "3":
            resp.message("ABOUT US\nWhatsApp Taxi Booking is a system that will offer a taxi booking service to citizens. The system will be used by taxi companies in such a way that they will register an account with us which will enable them to use our WhatsApp taxi booking system. The system will enable citizens in Zimbabwe to booking a taxi ride from registered taxi companies through their WhatsApp applications. Firstly, the system will check if the user is an existing or new user and greets the user with his or her WhatsApp username. The system will then display different options for the user such as, book a taxi, register for premium account, and about we option. When the user chooses the book a taxi option, he or she will be prompt to send his current location using the WhatsApp location feature. The system will check if the location sent is valid or not. In the case that the location is valid, the system will be smart enough to search for any taxi driver who is free and close to the location send by the user and book that taxi. The driver will be given the location sent by the user and the driver`s location along with the driver`s name, taxi colour, model and number plate will also be sent to the user. This will enable both the user and taxi driver to know the whereabouts of each other.")

        #-------------------------(option 2) validating location sent by user-----------
        elif stage == "location":
            session["stage"] = "final-booking"
            if "Latitude" in request.values.keys() and "Longitude" in request.values.keys():
                global message_latitude
                global message_longitude
                global message_address
            
                message_latitude = request.values.get("Latitude", None)

                message_longitude = request.values.get("Longitude", None)

                message_address = request.values.get('Address', None)
 
                  
                connection = sqlite3.connect('WhatsappTaxiOrg.db')
                cursor = connection.cursor()
                distanceList = []
                driverList = []
                for row in cursor.execute("SELECT driver_ID, latitude, longitude FROM drivers WHERE driver_status = 'free' "):
                    global message_latitude1
                    global message_longitude1
                    driver_ID,message_latitude1, message_longitude1 = row[0],row[1], row[2]
                
                    location1 = (message_latitude, message_longitude)
                    location2 = (message_latitude1, message_longitude1)

                    dist_between = (distance.distance(location1,location2).km)
                    #---------FORMARTING DISTANCE INTO 4 DECIMAL PLACES
                    value = (dist_between)
                    formatted_string = "{:.2f}".format(value)
                    float_value = float(formatted_string)
                    #----------GIVING DISTANCE TO CUSTOMER
                    
                    distanceList.append(float_value)
                    driverList.append(driver_ID)

                    index =(distanceList.index(min(distanceList)))
                    global minDistance
                    minDistance = min(distanceList)
                    global ddriver
                    ddriver = driverList[index]

                for row in cursor.execute("SELECT * FROM drivers WHERE driver_ID = "+str(driverList[index])):
                    driver_ID = row[0]
                    global driver_name
                    driver_name = row[1]
                    global driver_photo  
                    global phoneNumber
                    phoneNumber = row[2]
                    driver_photo = row[-1]
                    global vehicle_number 
                    vehicle_number = row[3]
                    resp.message(f"*The closest Taxi is {minDistance} km away from your location*\n\n1.Book the taxi ☑️\n2.Cancel ❌")

                # for row in cursor.execute("SELECT driver_ID, latitude, longitude FROM drivers WHERE driver_status != 'free' "):
                #     cursor.fetchall()
                #     resp.message(f"Sorry they are no taxis currently avaible near you")
                #     #connection.close()
                
            elif "Latitude" not in request.values.keys() and "Longitude" not in request.values.keys():
                session["stage"] = "user_location" 
                resp.message("❌Invalid location❌\nType the word *Taxi* to go back to menu")
                

               
#-----------------------AFTER USER SENDS LOCATIONS---------------------
        elif stage == "final-booking" and msg == "1":
            session["stage"] = "rating"
            today = datetime.today()
            connection = sqlite3.connect('WhatsappTaxiOrg.db')
            cursor = connection.cursor()
            cursor.execute("UPDATE drivers SET driver_status = ? Where phone_number = ?", ("busy", phoneNumber))
            connection.commit()
            connection.close()

            connection = sqlite3.connect('WhatsappTaxiOrg.db')
            cursor = connection.cursor()
            cursor.execute("INSERT INTO customers (phone_number,userName,date_and_time) VALUES (?,?,?)",(phone_number,user_name,today))
            connection.commit()

            connection = sqlite3.connect('WhatsappTaxiOrg.db')
            cursor = connection.cursor()
            for row in cursor.execute("SELECT * FROM taxis WHERE vehicle_number = "+str(vehicle_number)):
                number_plate = row[1]
                car_color = row[2]
                car_model = row[3]
            connection.commit()    
            connection.close()

            connection = sqlite3.connect('WhatsappTaxiOrg.db')
            cursor = connection.cursor()
            cursor.execute("SELECT phone_number FROM customers WHERE phone_number ="+str(phone_number))
            Numberr = cursor.fetchone()
            for phoneNumberr in Numberr:
                #Account SID 
                account_sid = "AC528f2786dbc01f42f34ddeb1a705da36"
                # Account Auth Token 
                auth_token  = "6548cb418657da18297afc1285c6d305"
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                    to=f"whatsapp:{phoneNumberr}",
                    from_="whatsapp:+14155238886",
                    persistent_action=[f"geo: {message_latitude1},{message_longitude1}|{message_address}"],
                    body=f"Name:{driver_name},\nPlate:{number_plate}"
                    )
                print(message.sid)

                message = client.messages.create(
                    to=f"whatsapp:{phoneNumberr}",
                    from_="whatsapp:+14155238886",
                    body=f"*Booking Successful*☑️\nYou will be kept up to date on the driver whereabouts after every nimute\n\n👤DRIVER DETAILS👤\n\n<>Driver name-> {driver_name}\n\n🚖CAR DETAILS🚖\n\n<>Number Plate-> {number_plate}\n<>Car Color-> {car_color}, {car_model}"
                    )
                print(message.sid)
                

            client = Client(account_sid, auth_token)
            message = client.messages.create( 
                to="whatsapp:"+str(phoneNumber),
                from_="whatsapp:+14155238886",
                body=f"*🚨🚨ALERT🚨🚨*\n\n{driver_name} Your taxi has been booked by {user_name}.\nNB.Keep your GPS ON\n\nUser location👇🏼👇🏼"
                )
            print(message.sid)
            client = Client(account_sid, auth_token)
            message = client.messages.create( 
                to="whatsapp:"+str(phoneNumber),
                from_="whatsapp:+14155238886",
                body=f"{message_address}",
                persistent_action=[f"geo: {message_latitude},{message_longitude}"]
                )
            print(message.sid)
            connection.commit()
            connection.close()
            time.sleep(15)
#------------------------------------------------------------------------------------------------------
            while minDistance > 0:
                #for row in cursor.execute("SELECT latitude, longitude FROM drivers WHERE driver_ID = "+str(ddriver)):
                connection = sqlite3.connect('WhatsappTaxiOrg.db')
                cursor = connection.cursor()
                for row in cursor.execute("SELECT lat, lon, addresses FROM coordinates "):
                    message_latitude1, message_longitude1, addresses = row[0], row[1], row[2]
                        
                    location1 = (message_latitude, message_longitude)
                    location2 = (message_latitude1, message_longitude1)

                    dist_between = (distance.distance(location1,location2).km)
                    #---------FORMARTING DISTANCE INTO 4 DECIMAL PLACES
                    value = (dist_between)
                    formatted_string = "{:.2f}".format(value)
                    float_value = float(formatted_string)

                    if float_value >0.5:
                        message = client.messages.create(
                            to=f"whatsapp:{phoneNumberr}",
                            from_="whatsapp:+14155238886",
                            body=f"{addresses}\nThe taxi is now {float_value} kms away from picking you up",
                            persistent_action=[f"geo: {message_latitude1},{message_longitude1}"]
                        )
                        print(message.sid)
                        
                    else:
                        session["stage"] = "rating"
                        message = client.messages.create(
                            to=f"whatsapp:{phoneNumberr}",
                            from_="whatsapp:+14155238886",
                            body=f"Taxi has arrived",
                            persistent_action=[f"geo: {message_latitude1},{message_longitude1}"]
                        )
                        # message = client.messages.create(
                        #     to=f"whatsapp:{phoneNumberr}",
                        #     from_="whatsapp:+14155238886",
                        #     body=f"Rate your experience when you have reached the destiation.\n\n⭐⭐⭐⭐⭐\n  1   2    3    4    5"
                        # )
                        # print(message.sid)
                        cursor.execute("UPDATE drivers SET driver_status = ? Where phone_number = ?", ("free", phoneNumber))
                        connection.commit()
                        connection.close()
                        quit()
                    time.sleep(10)
  

        # elif stage == "rating" and msg == "1":
        #     resp.message("RATING")
            
            # #Account SID 
            # account_sid = "AC528f2786dbc01f42f34ddeb1a705da36"
            # # Account Auth Token 
            # auth_token  = "6548cb418657da18297afc1285c6d305"
            # client = Client(account_sid, auth_token)
            # message = client.messages.create( 
            #     to="whatsapp:"+str(phoneNumber),
            #     from_="whatsapp:+14155238886",
            #     body=f"{username}\nRating:⭐"
                
            #     )
            # print(message.sid)        

  #--------------------------------------------------------------------------------------------              

        elif stage == "final-booking" and msg == "2":
            resp.message("❌Booking canceled❌.\nType the word *Taxi* to go back to menu.")
            

        elif stage == "final-booking" and msg != "1" or "2" :
            resp.message("❌Invalid input❌.\nType the word *Taxi* to go back to menu.")

        




        #----------------------- SESSION FOR PREMIUM ACCOUNTS-------------------------------------
        elif stage == "stage2.0" and msg == "1":
            session["stage"] = "location"
            resp.message("Share your live location (use the whatsapp location feature)📍")

        elif stage == "stage2.0" and msg == "2":
            resp.message("ABOUT US\nXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

        elif msg != "taxi":
            resp.message("Type the word *taxi* to get started")

    else: 
        resp.message("Type the word *taxi* to get started")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)