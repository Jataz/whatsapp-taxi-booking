import sqlite3
import folium
from datetime import datetime

from flask import Flask, render_template, request, url_for, redirect,flash
import joblib
from textblob import TextBlob
import data as dt


from werkzeug.utils import secure_filename

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
    m = folium.Map(location=[-17.821817324977584, 31.050666330068275],zoom_start=12)

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

    BelvedereRoute = [(-17.833864324904955, 31.038711445690076),
            (-17.836611681332055, 31.037402527663726),
            (-17.836560615636404, 31.03687681472079),
            (-17.836264434183278, 31.03241361882764),
            (-17.836274647348493, 31.030793564630603),
            (-17.83552908498641, 31.02929152758492),
            (-17.837632992627796, 31.028229372793042),
            (-17.837490009415035, 31.027832405816874),
            (-17.836254221020774, 31.02282203933199),
            (-17.835539298213977, 31.019882338397764), #GANGES ROAD
            (-17.836540189360473, 31.019657032829194),
            (-17.837326599883895, 31.019152777523953),
            (-17.838746215288378, 31.013670342222685),
            (-17.839236439599656, 31.01150311736953),
            (-17.83996156052486, 31.008284466485048)]
    BelvedereRoute2=[(-17.835539298213977, 31.019882338397764),
                    (-17.83476011732957, 31.018972025296527),
                    (-17.834045188456006, 31.018564329473865),
                    (-17.833534523257452, 31.018542871801873),
                    (-17.83271745589416, 31.018650160161823),
                    (-17.83234466766984, 31.01747535262206),
                    (-17.831762503650495, 31.015345678665767),
                    (-17.832559148655513, 31.014911160795485),
                    (-17.833223016766237, 31.01428888830692),
                    (-17.833830709253633, 31.013312564227576),
                    (-17.834009441951046, 31.0114779332655),
                    (-17.83394816219555, 31.009814963684946),
                    (-17.835066514508846, 31.00975059065261),
                    (-17.835168646772193, 31.008870826107668),
                    (-17.835949956785015, 31.007755027152417),
                    (-17.836364866766576, 31.00710056813469)
                    ]

    folium.PolyLine(BelvedereRoute,
                    color='red',
                    weight=10,
                    opacity=0.8).add_to(m)
    folium.PolyLine(BelvedereRoute2,
                    color='red',
                    weight=10,
                    opacity=0.8).add_to(m)

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
        driverPhoto = request.files['driverPhoto'].read()
        cur.execute(""" INSERT INTO drivers (driver_ID, driver_name, phone_number, vehicle_number,driver_status,driver_photo) VALUES(?,?,?,
                           ?,?,?)""", (driverid, driverName, phoneNumber, vehicleNumber, status,driverPhoto))
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
        driverPhoto = request.files['driverPhoto'].read()
        
        cur.execute("""UPDATE  drivers SET 
                    driver_name = ?,
                    phone_number =? , 
                    vehicle_number =?,
                    driver_status = ?,
                    driver_photo = ? 
                    WHERE driver_ID=?""", (driverName, phoneNumber, vehicleNumber, status,driverPhoto,driverid))
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
        taxiPhoto = request.files['taxiPhoto'].read()
        cur.execute(""" INSERT INTO taxis (vehicle_number, number_plate,color,model,taxi_photo) VALUES(?,?,?,
                           ?,?)""", (vehicleNumber, numberPlate, color, model,taxiPhoto))
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

#--------------------------------------------------------------------------------------------- 
#--------------------------------------------------------------------------------------------- 

if __name__ == '__main__':
    app.run(debug=True)
