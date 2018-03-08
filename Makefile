city_lights.csv: cities_tiles.csv download_tiles.py
	python3 download_tiles.py
cities_tiles.csv: cities_georeferenced.csv convert_coordinates.py
	python3 convert_coordinates.py < $< > $@
cities_georeferenced.csv: cities.csv georeference_cities.py settings.py
	python3 georeference_cities.py < $< > $@