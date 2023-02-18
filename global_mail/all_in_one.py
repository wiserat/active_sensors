import requests
import json
import os
from email.message import EmailMessage
import smtplib
import ssl
import requests
import json
import os
from email.message import EmailMessage
import smtplib
import ssl
import sqlite3
from datetime import datetime, timedelta, date
import datetime


my_message = EmailMessage()
context = ssl.create_default_context()


#creating necessary files and directories
try:
    with open('website/sensor_ids.txt', 'x') as f:
        f.close()
except:
    pass
try:
    os.mkdir('data_dir')
except:
    pass


#creating database
con = sqlite3.connect('instance/database.db')
cur = con.cursor()
list_of_registred = []
#listing all registred sensors
try:
    with open('website/email_ids.txt', 'r') as f:
        for line in f:
            list_of_registred.append(line.rstrip())
except:
    pass

#checking if there is new sensor
for row in cur.execute('''SELECT * FROM user'''):
    if row[1] not in list_of_registred:
        list_of_registred.append(row[1])

with open('website/email_ids.txt', 'w') as f:
    for item in list_of_registred:
        f.write(f'{item}\n')

#creating directory for each sensor
def create_dir(sensor_id):
    try:
        os.mkdir(f'data_dir/{sensor_id}_dir')     
    except:
        pass

#creating file for each sensor data type
def create_file(sensor_id, file_name):
    try:
        with open(f'data_dir/{sensor_id}_dir/{file_name}.txt', 'x') as f:
            f.close()
    except:
        pass

#check if values of registred sensors are correct
def check_existing_values(value_type, sensor_id, value):
    list_of_values = []
    try:
        with open(f"data_dir/{sensor_id}_dir/{value_type}.txt", "r") as f:
            for line in f.readlines():
                value = (line.rstrip())
                list_of_values.append(value)
        
        if str(value) == list_of_values[-1] and str(value) == list_of_values[-2] and str(value) == list_of_values[-3] and str(value) == list_of_values[-4] and str(value) == list_of_values[-5]:
            return False
    except:
        pass  
    
#write current values of registred sensor to file
def write_current_value(value, value_type, sensor_id):
    with open(f"data_dir/{sensor_id}_dir/{value_type}.txt", "a") as f:
        f.write(f"{value}\n")
        
#remove old values of registred sensors from file
def remove_old_values(value_type, sensor_id):
    list_of_values = []
    with open(f"data_dir/{sensor_id}_dir/{value_type}.txt", "r") as f:
        for line in f.readlines():
            value = (line.rstrip())
            list_of_values.append(value)
            
    while len(list_of_values) > 25: 
            list_of_values.pop(0)
            with open(f"data_dir/{sensor_id}_dir/{value_type}.txt", "w") as f:
                for line in list_of_values:
                    f.write(line + "\n")

#email noticiation sender if sensor is not working
def wrong_notification(sensor_id, my_message, context, list_of_problems):
    #check if the email was already sent (to avoid spamming every time this program runs)
    try:
        with open('logs', 'x') as f:
            f.close()
    except:
        pass
    
    start_email_sending = True
    verification = False
    with open('logs', 'r') as f:
        for line in f.readlines():
            info = (line.rstrip())
            really_trash, all_date = info.split(":")
            trash, month, date_in_logs = info.split("-")
            place_id, year = trash.split(":")
            if str(sensor_id) == str(place_id):
                verification = True
                year = int(year)
                month = int(month)
                date_in_logs = int(date_in_logs)
                break
    
    if verification == True:
        today = datetime.date.today()
        d0 = date(year, month, date_in_logs)
        d1 = date(today.year, today.month, today.day)
        delta = d1 - d0
        if delta.days < 30:
            start_email_sending = False
        elif delta.days >= 120:
            if delta.days in range(120, 10000, 90):
                start_email_sending = True
            else:
                start_email_sending = False
                
    #if email wasn't sent yet, send it
    if start_email_sending == True:
        my_password = 'uzokwsyoiwsygion'
        my_email = 'sensorvzduchu@gmail.com'
        my_message['From'] = my_email
        my_subject = "Upozornění na nefunkční senzor vzduchu"
        my_message['Subject'] = my_subject
        my_body = f"""
    Dobrý den, 
s lítostí Vám musíme oznámit, že Váš senzor s id: \"{sensor_id}\" přestal fungovat.
Konkrétně se jedná o senzor {list_of_problems}.
        """
        my_message.set_content(my_body)
        
        con = sqlite3.connect('instance/database.db')
        cur = con.cursor()
        
        #getting the user id
        for row in cur.execute('''SELECT * FROM user'''):
            if str(sensor_id) == str(row[1]):
                current_user_id = row[0]
                break
            else:
                current_user_id = None
        
        #getting the user emails
        emails = []
        if current_user_id != None:
            with open(f'all_emails_dir/{current_user_id}_emails', 'r') as f:
                for line in f:
                    emails.append(line.strip())
            
            #sending email to each submittet email
            counter = 0
            for email in emails:
                try:
                    print("before sending")
                    my_message['To'] = email
                    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                        smtp.login(my_email, my_password)
                        smtp.sendmail(my_email, email, my_message.as_string())
                        print("email sent")
                        counter = counter + 1
                        del my_message['To'] 
                except:
                    pass
            #writing to log file that email was sent
            if counter > 0:
                with open('logs', 'a') as f:
                    print("log file opened")
                    f.write(f'{sensor_id}:{datetime.date.today()}\n')
                    print(datetime.date.today())
                
        del my_message['From']
        del my_message['Subject']
        del my_message['To']      
        
#requesting data from sensor.community
r = requests.get('https://data.sensor.community/static/v1/data.json').json()
list_of_sensor_ids = []
list_of_location_ids = []
list_of_email_ids = []
list_of_checked_sensors = []
checker = True

#reading sensor ids from file
with open('website/sensor_ids.txt', 'r') as f:
    for line in f.readlines():
        list_of_sensor_ids.append(line.rstrip())
#reading email ids from the file (these are the emails to be checked)
with open('website/email_ids.txt', 'r') as f:
    for line in f.readlines():
        list_of_email_ids.append(line.rstrip())
        
for item in r:
    list_of_problems = []
    #sensor id must be unique, so we add location id to it (sensor id is not unique)
    sensor_id = str(item['sensor']['id']) + "_" + str(item['location']['id'])
    if sensor_id not in list_of_checked_sensors:
        list_of_checked_sensors.append(sensor_id)
        #all of the ids must be written even when not being checked, so login via the website can be done and the emails could be assigned to the sensor
        if str(sensor_id) not in list_of_sensor_ids:
            with open('website/sensor_ids.txt', 'a') as f:
                f.write(f'{sensor_id}\n')
        
        #ckecks if any emails are assigned to the sensor, only then the sensor is checked, emails sent and values written
        if str(sensor_id) in list_of_email_ids:
            create_dir(str(sensor_id))
            #looping thru sensors of different types
            for itom in item['sensordatavalues']:
                #print(sensor_id, item['location']['longitude'], itom['value_type'], itom['value'] + "\n")
                if itom['value'] == None:
                    list_of_problems.append(itom['value_type'])
                else:
                    #functions above
                    create_file(sensor_id, itom['value_type'])
                    write_current_value(itom['value'], itom['value_type'], sensor_id)    
                    checker = check_existing_values(itom['value_type'], sensor_id, itom['value'])
                    if checker == False:
                        list_of_problems.append(itom['value_type'])
                    remove_old_values(itom['value_type'], sensor_id)
                    
            if len(list_of_problems) > 0:
                wrong_notification(sensor_id, my_message, context, list_of_problems)