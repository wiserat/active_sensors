import requests
import jsonpath_rw_ext as jp


# json files with all of the data
conf_url_pm_sensor = "http://api.luftdaten.info/static/v2/data.1h.json"
conf_url_th_sensor = "http://api.luftdaten.info/static/v2/data.1h.json"

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# to add a new class, copy some existing one and change the name of the variables and the name of the class
# do not forget to add the variable of your class to the place_names list
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# classes start here
class smichov_class:
    def __init__(self):
        self.name = "smichov"
        self.conf_particle_sensor_id = 73737
        self.conf_temperature_sensor_id = 73738

smichov = smichov_class()
        
class hrdlorezy_class:
    def __init__(self):
        self.name = "hrdlorezy"
        self.conf_particle_sensor_id = 57275
        self.conf_temperature_sensor_id = 57276
        
hrdlorezy = hrdlorezy_class()
        
class belehradska_class:
    def __init__(self):
        self.name = "belehradska"
        self.conf_particle_sensor_id = 62343
        self.conf_temperature_sensor_id = 62344
        
belehradska = belehradska_class()

class brno_class:
    def __init__(self):
        self.name = "brno"
        self.conf_particle_sensor_id = 65591
        self.conf_temperature_sensor_id = 65592

brno = brno_class()

class vinohrady_class:
    def __init__(self):
        self.name = "vinohrady"
        self.conf_particle_sensor_id = 55766
        self.conf_temperature_sensor_id = 66529
        
vinohrady = vinohrady_class()

class ostrava_class:
    def __init__(self):
        self.name = "ostrava"
        self.conf_particle_sensor_id = 65156
        self.conf_temperature_sensor_id = 65157

ostrava = ostrava_class()
        
class dusni_class:
    def __init__(self):
        self.name = "dusni"
        self.conf_particle_sensor_id = 67739
        self.conf_temperature_sensor_id = 67740
        
dusni = dusni_class()
        
class podoli_class:
    def __init__(self):
        self.name = "podoli"
        self.conf_particle_sensor_id = 70357
        self.conf_temperature_sensor_id = 70358
        
podoli = podoli_class()

class stresovice_class:
    def __init__(self):
        self.name = "stresovice"
        self.conf_particle_sensor_id = 40202
        self.conf_temperature_sensor_id = 40203

stresovice = stresovice_class()

class ustinadlabem_class:
    def __init__(self):
        self.name = "ustinadlabem"
        self.conf_particle_sensor_id = 65628
        self.conf_temperature_sensor_id = 65629
        
ustinadlabem = ustinadlabem_class()

class mladaboleslav_class:
    def __init__(self):
        self.name = "mladaboleslav"
        self.conf_particle_sensor_id = 66626
        self.conf_temperature_sensor_id = 66627

mladaboleslav = mladaboleslav_class()
        
class plzen_class:
    def __init__(self):
        self.name = "plzen"
        self.conf_particle_sensor_id = 49039
        self.conf_temperature_sensor_id = 49040
        
plzen = plzen_class()
        
class jihlava_class:
    def __init__(self):
        self.name = "jihlava"
        self.conf_particle_sensor_id = 75437
        self.conf_temperature_sensor_id = 75438
        
jihlava = jihlava_class()

class olomouc_class:
    def __init__(self):
        self.name = "olomouc"
        self.conf_particle_sensor_id = 70222
        self.conf_temperature_sensor_id = 70223

olomouc = olomouc_class()

class ostravac_class:
    def __init__(self):
        self.name = "ostravac"
        self.conf_particle_sensor_id = 43196
        self.conf_temperature_sensor_id = 65157
        
ostravac = ostravac_class()

class novemesto_class:
    def __init__(self):
        self.name = "novemesto"
        self.conf_particle_sensor_id = 73632
        self.conf_temperature_sensor_id = 73633

novemesto = novemesto_class()
        
class pocernice_class:
    def __init__(self):
        self.name = "pocernice"
        self.conf_particle_sensor_id = 75946
        self.conf_temperature_sensor_id = 75945
        
pocernice = pocernice_class()
        
class holesovice_class:
    def __init__(self):
        self.name = "holesovice"
        self.conf_particle_sensor_id = 76127
        self.conf_temperature_sensor_id = 76128
        
holesovice = holesovice_class()



# functions to get the data from json into variables 
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
    
sensor_json_list_pm = sensor_json(conf_url_pm_sensor)
sensor_json_list_th = sensor_json(conf_url_th_sensor)
    
def values(place_name, x):
    # this function gets the values from json and returns them as variables !to put all of them in a list 'x' must be "list"
    list_of_values = []
    checkpoint = True

    try:
        pm_sensor_item = sensor_item(sensor_json_list_pm, place_name.conf_particle_sensor_id)
        th_sensor_item = sensor_item(sensor_json_list_th, place_name.conf_temperature_sensor_id)
    except: 
        checkpoint = False
        return None
        
    if checkpoint == False:
        return None
    
    elif x == "list":
        value_pm100 = extract_value_from_json_item(pm_sensor_item, "P1")
        value_pm025 = extract_value_from_json_item(pm_sensor_item, "P2")
        value_temperature = extract_value_from_json_item(th_sensor_item, "temperature")
        value_humidity = extract_value_from_json_item(th_sensor_item, "humidity")
        
        list_of_values = [value_pm100, value_pm025, value_temperature, value_humidity]
        return list_of_values
        
    elif x == 0:
        value_pm100 = extract_value_from_json_item(pm_sensor_item, "P1")
        return value_pm100
        
    elif x == 1:
        value_pm025 = extract_value_from_json_item(pm_sensor_item, "P2")
        return value_pm025
        
    elif x == 2:
        value_temperature = extract_value_from_json_item(th_sensor_item, "temperature")
        return value_temperature
        
    elif x == 3:
        value_humidity = extract_value_from_json_item(th_sensor_item, "humidity")
        return value_humidity
        
    else:
        print("Problem with 'x' given to the values function!")
            


# list of all of the classes defined above
place_names = [belehradska, 
               brno, 
               hrdlorezy,
               mladaboleslav,
               smichov,
               vinohrady,
               stresovice,
               podoli,
               ostrava, 
               dusni,
               ustinadlabem, 
               plzen,
               jihlava,
               olomouc, 
               ostravac,
               novemesto,
               pocernice,
               holesovice]


#x = -1
#for place_name in place_names:
#    x = 1
#    print(values(place_name, x))
