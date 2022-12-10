import os
from conf_all_in_one import *
from email.message import EmailMessage
import smtplib
import ssl

my_message = EmailMessage()
context = ssl.create_default_context()


def check_existing_values(sensor_type, place_name, sensor_value):
    # checks if there is not exacly the same value already
    list_of_values = []
    try:
        with open(f"data_dir/{place_name.name}_dir/{place_name.name}_values_of_{sensor_type}.txt", "r") as f:
            for line in f.readlines():
                value = (line.rstrip())
                list_of_values.append(value)
        
        if str(sensor_value) == list_of_values[-1] and str(sensor_value) == list_of_values[-2] and str(sensor_value) == list_of_values[-3] and str(sensor_value) == list_of_values[-4] and str(sensor_value) == list_of_values[-5]:
            return False
    except:
        pass
    
def write_current_value(sensor_value, sensor_type, place_name):
    # appends the current value for later comparison via check_existing_values function
    with open(f"data_dir/{place_name.name}_dir/{place_name.name}_values_of_{sensor_type}.txt", "a") as f:
        f.write(f"{sensor_value}\n")
        
def remove_old_values(sensor_type, place_name):
    # does not have to be runned if you do not want to delete old values
    list_of_values = []
    with open(f"data_dir/{place_name.name}_dir/{place_name.name}_values_of_{sensor_type}.txt", "r") as f:
        for line in f.readlines():
            value = (line.rstrip())
            list_of_values.append(value)
            
    while len(list_of_values) > 25: # this number is adjustable due to how many values you want to safe
            list_of_values.pop(0)
            with open(f"data_dir/{place_name.name}_dir/{place_name.name}_values_of_{sensor_type}.txt", "w") as f:
                for line in list_of_values:
                    f.write(line + "\n")
                    

# code starts here...
        
for place_name in place_names: 
    sensor_types = ["pm100", "pm025", "temperature", "humidity"]
    x = -1
    number_of_problems = 0
    list_of_problems = []
    
    # create directory for each place
    try:
        os.mkdir("data_dir")
    except: 
        pass
    try:
        os.mkdir(f"data_dir/{place_name.name}_dir")
    except:
        pass
    
    for sensor_type in sensor_types:
        # create files for each sensor type in each place directory
        try:
            with open(f"data_dir/{place_name.name}_dir/{place_name.name}_values_of_{sensor_type}.txt", "x") as f:
                f.close()
        except:
            pass
        
        x = x + 1
        value = values(place_name, x)
        
        
        # check if value is not None/error
        if value == None:
            number_of_problems = number_of_problems + 1
            list_of_problems.append(f"{sensor_type}")
        else: 
            # check, write and remove old values
            checker = check_existing_values(sensor_type, place_name, value)
            write_current_value(value, sensor_type, place_name)
            remove_old_values(sensor_type, place_name)
            if checker == False:
                number_of_problems = number_of_problems + 1
                list_of_problems.append(f"{sensor_type}")
            
    # output of concrete problems
    if number_of_problems == 4:
        print(f"{place_name.name} is not working as a whole")
        wrong_notification(place_name, my_message, context, list_of_problems)
    elif number_of_problems > 1:
        print(f"{place_name.name}'s sensors of {list_of_problems} are not working")    
        wrong_notification(place_name, my_message, context, list_of_problems)
    elif number_of_problems == 1:
        print(f"{place_name.name}'s sensor of {list_of_problems} is not working")
        wrong_notification(place_name, my_message, context, list_of_problems)
    else:
        continue