import pandas as pd

#preindustrial_data = pd.read_csv("./data/850_year_preindustrial_control_experiment.csv") #K
land_ocean_data = pd.read_csv("./data/observed_land-ocean_temperature.csv") #C
climate_forcings_data = pd.read_csv("./data/responses_to_climate_forcings.csv") #K

kelvin_to_celsius = lambda x: (x-273.15)
kelvin_to_fahrenheit = lambda x: x*1.8 - 459.67
celsius_to_fahrenheit = lambda x: x*1.8 + 32
climate_forcings_data.iloc[:,1:] = climate_forcings_data.iloc[:,1:].apply(kelvin_to_celsius)
#land_ocean_data.iloc[:,[1,2]] = land_ocean_data.iloc[:,[1,2]].apply(celsius_to_fahrenheit)

#remove data before 1880
climate_forcings_data = climate_forcings_data[climate_forcings_data['Year'] >= 1880]
#remove data after 2005
land_ocean_data = land_ocean_data[land_ocean_data['Year'] <= 2005]

#get averages for forcings from 1880-1910
averages = []
headings = []
for f in climate_forcings_data.iloc[:,1:]:
    headings.append(f)
    mean = climate_forcings_data[f][(climate_forcings_data['Year'] >= 1880) & (climate_forcings_data['Year'] <= 1910)].mean()
    averages.append([f, mean])

forcing_averages_data = pd.DataFrame(averages, columns=['Forcing', 'Average'])
#averages_data.to_csv('averages.csv', index=False)

#get difference from mean for forcings
for i in forcing_averages_data.index:
    climate_forcings_data[forcing_averages_data.loc[i, 'Forcing']] = climate_forcings_data[forcing_averages_data.loc[i, 'Forcing']].apply(lambda x: x - forcing_averages_data.loc[i, 'Average'])



#get averages for temps from 1880-1910
averages = []
headings = []
for t in land_ocean_data.iloc[:,1:]:
    headings.append(t)
    mean = land_ocean_data[t][(land_ocean_data['Year'] >= 1880) & (land_ocean_data['Year'] <= 1910)].mean()
    averages.append([t, mean])

temp_averages_data = pd.DataFrame(averages, columns=['Temp', 'Average'])

#get difference from mean for temps
for i in temp_averages_data.index:
    land_ocean_data[temp_averages_data.loc[i, 'Temp']] = land_ocean_data[temp_averages_data.loc[i, 'Temp']].apply(lambda x: x - temp_averages_data.loc[i, 'Average'])


#make csv files with the new units
land_ocean_data.to_csv('land_ocean_filtered.csv', index=False)
climate_forcings_data.to_csv('climate_forcings_filtered.csv', index=False)