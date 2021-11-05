# this file is called separately from app.py. This file reads and processes the data files.

import pandas as pd

land_ocean_data = pd.read_csv("./data/observed_land-ocean_temperature.csv") #in C
climate_forcings_data = pd.read_csv("./data/responses_to_climate_forcings.csv") #in K

#these will be the output csvs. There is one copy in C and one in F.
land_ocean_data_c = land_ocean_data.copy()
land_ocean_data_f = land_ocean_data.copy()
climate_forcings_data_c = climate_forcings_data.copy()
climate_forcings_data_f = climate_forcings_data.copy()

#functions to convert between different temperatures
kelvin_to_celsius = lambda x: (x-273.15)
kelvin_to_fahrenheit = lambda x: x*1.8 - 459.67
celsius_to_fahrenheit = lambda x: x*1.8 + 32

#convert the units for our output data
climate_forcings_data_c.iloc[:,1:] = climate_forcings_data_c.iloc[:,1:].apply(kelvin_to_celsius)
climate_forcings_data_f.iloc[:,1:] = climate_forcings_data_f.iloc[:,1:].apply(kelvin_to_fahrenheit)
land_ocean_data_f.iloc[:,[1,2]] = land_ocean_data_f.iloc[:,[1,2]].apply(celsius_to_fahrenheit)

#remove data before 1880 for climate forcings data
climate_forcings_data_c = climate_forcings_data_c[climate_forcings_data_c['Year'] >= 1880]
climate_forcings_data_f = climate_forcings_data_f[climate_forcings_data_f['Year'] >= 1880]
#remove data after 2005 for observed temperature data
land_ocean_data_c = land_ocean_data_c[land_ocean_data_c['Year'] <= 2005]
land_ocean_data_f = land_ocean_data_f[land_ocean_data_f['Year'] <= 2005]

#climate forcings celsius data
#get averages for forcings from 1880-1910
averages = []
headings = []
for f in climate_forcings_data_c.iloc[:,1:]:
    headings.append(f)
    mean = climate_forcings_data_c[f][(climate_forcings_data_c['Year'] >= 1880) & (climate_forcings_data_c['Year'] <= 1910)].mean()
    averages.append([f, mean])

forcing_averages_data = pd.DataFrame(averages, columns=['Forcing', 'Average'])

#get difference from mean for forcings
for i in forcing_averages_data.index:
    climate_forcings_data_c[forcing_averages_data.loc[i, 'Forcing']] = climate_forcings_data_c[forcing_averages_data.loc[i, 'Forcing']].apply(lambda x: x - forcing_averages_data.loc[i, 'Average'])

#climate forcings fahrenheit data
#get averages for forcings from 1880-1910
averages = []
headings = []
for f in climate_forcings_data_f.iloc[:,1:]:
    headings.append(f)
    mean = climate_forcings_data_f[f][(climate_forcings_data_f['Year'] >= 1880) & (climate_forcings_data_f['Year'] <= 1910)].mean()
    averages.append([f, mean])

forcing_averages_data = pd.DataFrame(averages, columns=['Forcing', 'Average'])
#averages_data.to_csv('averages.csv', index=False)

#get difference from mean for forcings
for i in forcing_averages_data.index:
    climate_forcings_data_f[forcing_averages_data.loc[i, 'Forcing']] = climate_forcings_data_f[forcing_averages_data.loc[i, 'Forcing']].apply(lambda x: x - forcing_averages_data.loc[i, 'Average'])

#observed temperature celsius data
#get averages for temps from 1880-1910
averages = []
headings = []
for t in land_ocean_data_c.iloc[:,1:]:
    headings.append(t)
    mean = land_ocean_data_c[t][(land_ocean_data_c['Year'] >= 1880) & (land_ocean_data_c['Year'] <= 1910)].mean()
    averages.append([t, mean])

temp_averages_data = pd.DataFrame(averages, columns=['Temp', 'Average'])

#get difference from mean for temps
for i in temp_averages_data.index:
    land_ocean_data_c[temp_averages_data.loc[i, 'Temp']] = land_ocean_data_c[temp_averages_data.loc[i, 'Temp']].apply(lambda x: x - temp_averages_data.loc[i, 'Average'])

#observed temperature fahrenheit data
#get averages for temps from 1880-1910
averages = []
headings = []
for t in land_ocean_data_f.iloc[:,1:]:
    headings.append(t)
    mean = land_ocean_data_f[t][(land_ocean_data_f['Year'] >= 1880) & (land_ocean_data_f['Year'] <= 1910)].mean()
    averages.append([t, mean])

temp_averages_data = pd.DataFrame(averages, columns=['Temp', 'Average'])

#get difference from mean for temps
for i in temp_averages_data.index:
    land_ocean_data_f[temp_averages_data.loc[i, 'Temp']] = land_ocean_data_f[temp_averages_data.loc[i, 'Temp']].apply(lambda x: x - temp_averages_data.loc[i, 'Average'])


#make csv files with the new units
land_ocean_data_c.to_csv('land_ocean_c_filtered.csv', index=False)
land_ocean_data_f.to_csv('land_ocean_f_filtered.csv', index=False)
climate_forcings_data_c.to_csv('climate_forcings_c_filtered.csv', index=False)
climate_forcings_data_f.to_csv('climate_forcings_f_filtered.csv', index=False)