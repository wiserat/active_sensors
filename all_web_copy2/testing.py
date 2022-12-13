import requests

r = requests.get('https://data.sensor.community/static/v1/data.json').json()

for item in r:
   # if item['location']['country'] == 'CZ':
   #     if item['sensor']['id'] == 47080:   #temp hum press pressatsea 33067
                                            print(item['location']['country'])