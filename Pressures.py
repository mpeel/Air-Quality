"""
This file obtains outdoor pressure for a chosen location.
"""
import datetime
from geopy.geocoders import Nominatim
import meteostat
#%%
#Obtain the exact location of e.g. a building
geolocator = Nominatim(user_agent='air_quality_monitoring')
location = geolocator.geocode(query='Blackett Laboratory')
latitude, longitude = location.latitude, location.longitude

# Make sure location is correct.
print(location)
print(f'lat: {latitude}')
print(f'lon: {longitude}')
#%%
#Obtain the pressure over a chosen period
start = datetime.datetime(year=2023, month=12, day=1, hour=8, minute=0)
end = datetime.datetime(year=2023, month=12, day=1, hour=20, minute=0)

#Get the pressure for said period, at chosen location
data = meteostat.Hourly(meteostat.Point(latitude, longitude), start, end).fetch()
#%%