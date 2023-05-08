from flask import Flask,render_template, request, session, redirect
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3



resp = MessagingResponse()

    
def validation(user_name, name_check):
    if len(name_check.fetchall()) > 0 : 
        return(f"*PREMIUM ACCOUNT*\nHello {user_name}.\nType in your option:\n\n1.Book a taxi\n2.About Us\n🚕🚖🇿🇼🚕🚖\n") 
    

       

        #------------------NEW USER ----------------------------
    elif len(name_check.fetchall()) == 0 :
        
        return (f"Hello {user_name}. Welcome to Whatsapp Taxi Booking.\nType in your option:\n\n1.Book a taxi\n2.Register premium account\n3.About Us\n🚕🚖🇿🇼🚕🚖\n")
        

        

    





def saving_to_DB():

        try:
            connection = sqlite3.connect('WhatsappTaxiOrg.db', timeout=1)
            connection.execute("INSERT INTO customers (phone_number, date_and_time, city) VALUES (?, ?, ?)", (number, date, city ))
            

        except:
            print(Exception)

        finally:
            connection.commit()
            connection.close()