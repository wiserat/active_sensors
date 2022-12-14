import requests
import json
import os
from email.message import EmailMessage
import smtplib
import ssl
import requests
import jsonpath_rw_ext as jp
from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
import json
import os
from sqlalchemy.orm import load_only
from email.message import EmailMessage
import smtplib
import ssl
import sqlite3
from datetime import datetime, timedelta, date
import datetime

my_message = EmailMessage()
context = ssl.create_default_context()


def check_existing_values(value_type, item_id, value):
    list_of_values = []
    try:
        with open(f"data_dir/{item_id}_dir/{item_id}_values_of_{value_type}.txt", "r") as f:
            for line in f.readlines():
                value = (line.rstrip())
                list_of_values.append(value)
        
        if str(value) == list_of_values[-1] and str(value) == list_of_values[-2]: #and str(value) == list_of_values[-3] and str(value) == list_of_values[-4] and str(value) == list_of_values[-5]:
            return False
    except:
        pass
    
def write_current_value(value, value_type, item_id):
    with open(f"data_dir/{item_id}_dir/{item_id}_values_of_{value_type}.txt", "a") as f:
        f.write(f"{value}\n")
        
def remove_old_values(value_type, item_id):
    list_of_values = []
    with open(f"data_dir/{item_id}_dir/{item_id}_values_of_{value_type}.txt", "r") as f:
        for line in f.readlines():
            value = (line.rstrip())
            list_of_values.append(value)
            
    while len(list_of_values) > 25: 
            list_of_values.pop(0)
            with open(f"data_dir/{item_id}_dir/{item_id}_values_of_{value_type}.txt", "w") as f:
                for line in list_of_values:
                    f.write(line + "\n")
                    
def wrong_notification(item_id, my_message, context, list_of_problems):
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
            if item_id == place_id:
                verification = True
                year = int(year)
                month = int(month)
                date_in_logs = int(date_in_logs)
                break
    
    if verification == True:
        today = datetime.date.today()
        #day_in_month_delta = month_delta.day
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
                
    if start_email_sending == True:
        my_password = 'uzokwsyoiwsygion'
        my_email = 'sensorvzduchu@gmail.com'
        my_message['From'] = my_email
        my_subject = "Upozornění na nefunkční senzor vzduchu"
        my_message['Subject'] = my_subject
        my_body = f"""
    Dobrý den, 
s lítostí Vám musíme oznámit, že Váš senzor s id: \"{item_id}\" přestal fungovat.
Konkrétně se jedná o senzor {list_of_problems}.
        """
        my_message.set_content(my_body)
        
        con = sqlite3.connect('instance/database.db')
        cur = con.cursor()
        
        for row in cur.execute('''SELECT * FROM user'''):
            if item_id == row[1]:
                current_user_id = row[0]
                break
            else:
                current_user_id = None
        
        emails = []
        if current_user_id != None:
            with open(f'all_emails_dir/{current_user_id}_emails', 'r') as f:
                for line in f:
                    emails.append(line.strip())
            
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
            if counter > 0:
                with open('logs', 'a') as f:
                    print("log file opened")
                    f.write(f'{item_id}:{datetime.date.today()}\n')
                    print(datetime.date.today())
                
        del my_message['From']
        del my_message['Subject']
        del my_message['To']


try:
    with open('website/sensor_ids.txt', 'x') as f:
        f.close()
except:
    pass
try:
    with open('website/location_ids.txt', 'x') as f:
        f.close()
except:
    pass
try:
    os.mkdir('data_dir')
except:
    pass

r = requests.get('https://data.sensor.community/static/v1/data.json').json()
list_of_ids = []
list_of_location_ids = []
temporarily_list = []

with open('website/sensor_ids.txt', 'r') as f:
    for line in f.readlines():
        list_of_ids.append(line.rstrip())
with open('website/location_ids.txt', 'r') as f:
    for line in f.readlines():
        list_of_location_ids.append(line.rstrip())
for item in r:
    p1_exists = False
    p2_exists = False
    p1_value = None
    p2_value = None
    list_of_problems = []
    if item['location']['country'] == 'CZ':
        for itom in item['sensordatavalues']:
            if itom['value_type'] == "P1":
                p1_exists = True
                p1_value = itom['value']
            elif itom['value_type'] == "P2":
                p2_exists = True
                p2_value = itom['value']
            else:
                continue
        if p1_exists == True and p2_exists == True:
            item_id = str(item['sensor']['id'])
            item_location_id = str(item['location']['id'])
            if item_id not in temporarily_list:
                for itom in item['sensordatavalues']:
                    if itom['value_type'] == "P1" or itom['value_type'] == "P2":
                        try:
                            os.mkdir(f"data_dir/{item_id}_dir")
                        except:
                            pass
                        try:
                            with open(f"data_dir/{item_id}_dir/{item_id}_values_of_{itom['value_type']}.txt", 'x') as f:
                                f.close()
                        except:
                            pass
                        if item_id not in list_of_ids:
                            list_of_ids.append(item_id)
                            with open('website/sensor_ids.txt', 'a') as f:
                                f.write(f"{item_id}\n")
                            list_of_location_ids.append(item_location_id)
                            with open('website/location_ids.txt', 'a') as f:
                                f.write(f"{item_location_id}\n")
                                
                        if list_of_ids.index(item_id) == list_of_location_ids.index(item_location_id):
                            if itom['value'] == None:
                                list_of_problems.append(itom['value_type'])
                            else:
                                checker = True
                                checker = check_existing_values(itom['value_type'], item_id, itom['value'])
                                write_current_value(itom['value'], itom['value_type'], item_id)
                                remove_old_values(itom['value_type'], item_id)
                                temporarily_list.append(item_id)
                                if checker == False:
                                    list_of_problems.append(itom['value_type'])
            if len(list_of_problems) > 0:
                wrong_notification(item_id, my_message, context, list_of_problems)