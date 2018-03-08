import csv
import sys
import math

## FIXME: zoom levels
default_dict = dict(
    	z='',
    	tile_x='',
    	tile_y='',
    	pixel_x='',
    	pixel_y='')

def lat_lon_to_tile(lat,lon,z):
    """convert a Point to tuple (x,y,z) representing a tile in Mercator projection
   
    information about converting coordinates to a tile in Mercator projection may be found at:
    http://wiki.openstreetmap.org/wiki/Slippy_map_tilenames
    http://mapki.com/wiki/Lat/Lon_To_Tile
    """

    lat_rad = math.radians(lat)
    n = 2.0 ** z
    x = ((lon + 180.0) / 360.0 * n)
    y = ((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)

    tile_x = int(x)
    tile_y = int(y)

    pixel_x = int((x-tile_x)*256)
    pixel_y = int((y-tile_y)*256)

    return dict(
    	z=z,
    	tile_x=tile_x,
    	tile_y=tile_y,
    	pixel_x=pixel_x,
    	pixel_y=pixel_y)

if __name__ == '__main__':
	z = 8
	reader = csv.DictReader(sys.stdin)
	writer = csv.DictWriter(sys.stdout, fieldnames=reader.fieldnames+list(default_dict.keys()))
	writer.writeheader()
	for data in reader:
		try:
			lati = float(data['lat'])
			longi = float(data['lon'])
			data.update(lat_lon_to_tile(lati,longi, z))
		except:
			data.update(default_dict)
		writer.writerow(data)