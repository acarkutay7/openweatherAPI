import time
import pandas as pd
import fetch_weather as fw
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, Float

engine = create_engine('sqlite:///weather_data.db')

# container object that keeps together many different features of a database
# SUCH AS Table, Engine, Connection & database like create_all or drop_all
metadata = MetaData() 

# Define table 
weather_data = Table('weather_data', metadata,
                     Column('id', Integer, primary_key = True),
                     Column('city', String),
                     Column('temperature', Float))

# Create tabl e
metadata.create_all(engine)

data_list = [] # list to store data

cities  = ['İstanbul', 'Bursa', 'Ankara', 'İzmir', 'Antalya']
api_key = "your_api"
for city in cities: # Temperature in Turkey
    data = fw.fetch_weather_data(city, api_key)
    temp_k = data['main']['temp'] # get temperature
    temp_c = temp_k - 273.15 # convert to Celcius
    data_list.append(temp_c) 
    
# Load the data into a pandas dataframe
df = pd.DataFrame(data_list, columns = ['Temperature'])

# Perform some basic stastical analysis
mean_temp = df['Temperature'].mean()
max_temp = df['Temperature'].max()
min_temp = df['Temperature'].min()

print(f"Mean temperature: {mean_temp} C")
print(f"Max temperature: {max_temp} C")
print(f"Min temperature: {min_temp} C")

# Insert data into the table
with engine.connect() as connection:
    for city, temp in zip(cities, data_list):
        query = weather_data.insert().values(city = city, temperature = temp)
        connection.execute(query)

