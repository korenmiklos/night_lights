import requests
from PIL import Image
from io import BytesIO
import csv

TILE_CACHE = {}
WIDTH = 16

class Tile(object):
	def __init__(self, x, y, z, date):
		self.x = int(x)
		self.y = int(y)
		self.z = int(z)
		self.date = date
		self.image = None

	def url(self):
		return 'https://gibs.earthdata.nasa.gov/wmts/epsg3857/best/VIIRS_Night_Lights/default/{}/GoogleMapsCompatible_Level{}/{}/{}/{}.png'.format(self.date, self.z, self.z, self.y, self.x)

	def request(self):
		if self.url() in TILE_CACHE:
			self.image = TILE_CACHE[self.url()]
		else:
			print(self.url())
			response = requests.get(self.url())
			self.image = Image.open(BytesIO(response.content))
			TILE_CACHE[self.url()] = self.image

	def get_box(self, center_x, center_y, width):
		if self.image is None:
			self.request()
		box = (center_x-width//2, center_y-width//2, center_x+width//2, center_y+width//2)
		return self.image.crop(box)

class City(object):
	def __init__(self, row, year):
		self.tile = Tile(row['tile_x'], row['tile_y'], row['z'], '{}-01-01'.format(year))
		self.image = self.tile.get_box(int(row['pixel_x']), int(row['pixel_y']), WIDTH)
		self.name = row['city_name']
		self.ksh_kod = row['ksh_kod']
		self.year = year
		self.file_name = '{}/{}.png'.format(self.year, self.ksh_kod)

	def save(self):
		self.image.save(self.file_name)

	def average_light(self):
		pixels = self.image.load()
		return sum([pixels[x,y][3] for x in range(WIDTH) for y in range(WIDTH)])/(float(WIDTH)**2)

if __name__ == '__main__':
	reader = csv.DictReader(open('cities_tiles.csv', 'r'))
	writer = csv.DictWriter(open('city_lights.csv', 'w'), fieldnames=reader.fieldnames+['average_light_2012', 'average_light_2016'])
	writer.writeheader()
	for row in list(reader):
		if row['tile_x'] and row['tile_y']:
			data = dict(
				average_light_2012=None,
				average_light_2016=None,
				)
			for year in [2012, 2016]:
				city = City(row, year)
				data['average_light_{}'.format(year)] = city.average_light()
				city.save()
			row.update(data)
			writer.writerow(row)
