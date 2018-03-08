import requests
import csv
import sys
from time import sleep
from settings import api_key

default_url = 'https://eu1.locationiq.org/v1/search.php'

class Nominatim(object):
	def __init__(self):
		self._url = default_url+'?key={}&format=json'.format(api_key)

	def query(self, text):
		return requests.get(self._url+'&q='+text).json()

def geocode(city, connection):
	response = connection.query(u'{}, Hungary'.format(city))
	cities = [i for i in response if i['class']=='place' or i['type']=='administrative']
	if cities:
		return dict(
			lat=cities[0]['lat'],
			lon=cities[0]['lon']
			)
	else:
		return dict(lat='', lon='')

if __name__ == '__main__':
	nom = Nominatim()

	reader = csv.DictReader(sys.stdin)
	writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames+['lat', 'lon'])
	writer.writeheader()
	for row in reader:
		try:
			data = geocode(row['city_name'], nom)
			sleep(1.1)
		except:
			data={}
		row.update(data)
		writer.writerow(row)