import requests
import jsonpath_rw_ext as jp
import os

from one_by_one.config import *


def sensor_json(url):
    # request to get entire json, after that we can speciffy text and items
    return requests.get(url).json()

def sensor_item(sensor_json_list, sensor_id):
    # first part to get specific items from entire json from previous function
    return [item for item in sensor_json_list if item['sensor']['id'] == sensor_id][-1]

def extract_value_from_json_item(json, key):
    # get value of particulate matter from one of urls, that I defined in config file
    query = '$.sensordatavalues[?(value_type="{}")].value'.format(key)
    matches = jp.match(query, json)
    return float(matches[-1])

def check_existing_values(sensor_value, sensor_type):
    # checks if there is not exacly the same value already
    list_of_values = []
    with open(f"{smichov_name}_file/{smichov_name}_values_of_{sensor_type}.txt", "r") as f:
        for line in f.readlines():
            value = (line.rstrip())
            list_of_values.append(value)
    
    if list_of_values[-1] == str(sensor_value): # checks if the last written value is the same as the current one
        print("Nekde je problem lol(tohle potom bude oznameni ze se neco pokazilo)")
    else:
        print("Pohoda jahoda")
    
def write_current_value(sensor_value, sensor_type):
    # appends the current value for later comparison via check_existing_values function
    with open(f"{smichov_name}_file/{smichov_name}_values_of_{sensor_type}.txt", "a") as f:
        f.write(f"{sensor_value}\n")
        
def remove_old_values(sensor_type):
    # does not have to be runned if you do not want to delete old values
    list_of_values = []
    with open(f"{smichov_name}_file/{smichov_name}_values_of_{sensor_type}.txt", "r") as f:
        for line in f.readlines():
            value = (line.rstrip())
            list_of_values.append(value)
            
    while len(list_of_values) > 25: # this number is adjustable due to how many values you want to safe
            list_of_values.pop(0)
            with open(f"{smichov_name}_file/{smichov_name}_values_of_{sensor_type}.txt", "w") as f:
                for line in list_of_values:
                    f.write(line + "\n")
                    

# code starts here...

                    
pm_sensor_item = sensor_item(
        sensor_json(conf_url_pm_sensor),
        smichov_conf_particle_sensor_id)
th_sensor_item = sensor_item(
        sensor_json(conf_url_th_sensor),
        smichov_conf_temperature_sensor_id)

value_pm100 = extract_value_from_json_item(pm_sensor_item, "P1")
value_pm025 = extract_value_from_json_item(pm_sensor_item, "P2")
value_temperature = extract_value_from_json_item(th_sensor_item, "temperature")
value_humidity = extract_value_from_json_item(th_sensor_item, "humidity")

sensor_type = ["pm100", "pm025", "temperature", "humidity"]
sensor_value = [value_pm100, value_pm025, value_temperature, value_humidity]

for value in sensor_value:
    try:
        os.mkdir(f"{smichov_name}_file")
    except:
        pass
    
    try:
        with open(f"{smichov_name}_file/{smichov_name}_values_of_{sensor_type[sensor_value.index(value)]}.txt", "x") as f:
            f.close()
    except:
        pass
    
    if value == None:
        print("Nekde je problem lol(tohle potom bude oznameni ze se neco pokazilo)")
    else:
        check_existing_values(value, sensor_type[sensor_value.index(value)])
        
        write_current_value(value, sensor_type[sensor_value.index(value)])
        
        remove_old_values(sensor_type[sensor_value.index(value)])