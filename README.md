# Night lights of Hungarian municipalities

Save PNG pictures and calculate average nightlight brightess for 8-by-8km surroundings of Hungarian municipalities using the [VIIRS instrument](https://jointmission.gsfc.nasa.gov/viirs.html) of the Suomi NPP satellite. Images courtesy of [NASA EarthData](https://earthdata.nasa.gov/about/science-system-description/eosdis-components/global-imagery-browse-services-gibs). Geocoding courtesy of [LocationIQ](https://locationiq.org/).

Get an API key from [LocationIQ](https://locationiq.org/#register).

`git pull https://github.com/korenmiklos/night_lights.git`
`pip install -r requirements.txt`
`echo api_key=<API_KEY_HERE> > settings.py`
`make`