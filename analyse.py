#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 10:34:53 2023

@author: sima
"""

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from datetime import datetime
from matplotlib.dates import DateFormatter, HourLocator
import pandas as pd


# Define lists to store the separated data
temperatures = [] #Temperature from BME280
pressures = []  #Pressure from BME280
humidity = []   #Humidity from BME280
times = []  #Date and time from the data
tempsscd = []   #Temperature from SCD30
CO2s = []   #CO2 concentration  from SCD30
humsscd = []    #Humidity from SCD30
p3s = []    #Particulates larger than 0.3um
p5s = []    #Particulates larger than 0.5um
p10s = []   #Particulates larger than 1.0um
p25s = []   #Particulates larger than 2.5um
p50s =[]    #Particulates larger than 5.0um
p100s = []  #Particulates larger than 10.0um
date = []   #Separate arry for the date

# Open the text file
with open('file_name.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Split the line using a comma as the delimiter
        data = line.strip().split(', ')
        if len(data) == 13: #Input the number of variables your dataq file contains
            # Extract the values and convert them to float where applicable
            CO2 = float(data[0])
            tempscd = float(data[1]) - 1.99 #SCD30 temperature shifted for calibration
            temperature = float(data[2]) + 0.22 #BME280 temperature shifted for calibration
            humscd = float(data[3])
            humidity_value = float(data[4])
            pressure = float(data[5])
            timestamp = data[6]
            p3 = data[7]
            p5 = data[8]
            p10 = data[9]
            p25 = data[10]
            p50 = data[11]
            p100 = data[12]
            
            #Split the data variable into date and time
            date_parts = timestamp.split(' ')[0].split('-')

            # Split the timestamp to extract the time
            time_parts = timestamp.split(' ')[1].split(':')
            hours = int(time_parts[0])
            minutes = int(time_parts[1])
            seconds = float(time_parts[2])
            time_decimal = hours + minutes / 60 + seconds / 3600
        
            #Either append data directly or use the if function to include specific data
            if pressure > 700:
                # Append the values to their respective lists
                temperatures.append(temperature)
                pressures.append(pressure)
                humidity.append(humidity_value)
                tempsscd.append(tempscd)
                CO2s.append(CO2)
                humsscd.append(humscd)
                p3s.append(p3)
                p5s.append(p5)
                p10s.append(p10)
                p25s.append(p25)
                p50s.append(p50)
                p100s.append(p100)
                times.append(time_decimal)
                date_times = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S.%f')
                date.append(date_times)
#%%
#Plotting the CO2 concentration and temperature of each room, two plots one above the other

# Create a figure and two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 10), sharex=True, gridspec_kw={'height_ratios': [2, 3]})

# Plot temperature data on the first subplot (upper)
ax1.plot(times, temperatures, label='BME280')
ax1.plot(times, tempsscd, label = 'SCD30')
ax1.set_ylabel('Temperature (°C)', fontsize=15)
ax1.legend(loc='lower right', fontsize=10)
ax1.tick_params(axis='y', labelsize = 13)
ax1.grid()

# Plot CO2 concentration data on the second subplot (lower)
ax2.plot(times, CO2s, label='CO2 Concentration')
ax2.set_ylabel('$CO_{2}$ Concentration (ppm)', fontsize=15)
ax2.set_xlabel('Local Time (h)', fontsize=15)
ax2.tick_params(axis='y', labelsize = 13)
ax2.tick_params(axis='x', labelsize = 13)
ax2.grid()

# Add labels to the subplots 
ax2.set_xlabel('Local Time (h)')
plt.xticks(np.arange(8, 21, step=1))

#Choose appropriate limits for the axes
ax1.set_ylim([18,25.5])
ax1.set_xlim([8, 20.5])
ax2.set_ylim([300, 1600]) 
ax2.set_xlim([8, 20.5])

# Add a big title for the entire figure
fig.suptitle('$CO_{2}$ concentration and Temperature', fontsize=17)

plt.tight_layout()
plt.show()
#%%
#This section plots the CO2 concentration and Temperature from imported data file, against time

fig, ax1 = plt.subplots(figsize=(7, 5))
plt.grid()

ax1.set_axisbelow(True) #The x-axis (time) is shared/the same for both variables

# Create a second y-axis for Temperature on the right side
ax2 = ax1.twinx()
ax2.plot(times, temperatures, color='red', label='Temperature BME', zorder=-1, alpha=0.7)
ax2.plot(times, tempsscd, color='orange', label='Temperature SCD', zorder=-2, alpha=0.7)
ax2.set_ylabel('Temperature (°C)', fontsize=15) #Select font and label size accordingly, for better visibility in e.g. a report
ax2.tick_params(axis='y', labelsize = 13)
ax1.tick_params(axis='x', labelsize = 13)

#Below, the scale of both axes is set for better comparison with other data files
#Do not change if you want two figures with the same scale, for comparison
ax2.set_ylim([18,25.5]) #Choose appropriate limits for the y-axis
ax2.set_xlim([8, 20.5]) #Choose appropriate limits for the x-axis

# Plot CO2 concentration on the left y-axis
ax1.scatter(times, CO2s, color='blue', label='CO2 Concentration', marker='.', zorder=3, alpha=1)
ax1.set_xlabel('Local Time (h)', fontsize=15) #Select font and label size accordingly, for better visibility in e.g. a report
ax1.set_ylabel("$CO_{2}$ Concentration (ppm)", fontsize=15)
ax1.tick_params(axis='y', labelsize=13)
ax1.set_ylim([300, 1600]) 

# Title for the plot
plt.title('CO2 and Temperature, fontsize=17)

# Legend for both y-axes
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper left', fontsize=10)

plt.show()
#%%
#Plotting the indoor and outdoor pressure over time for chosen file

#Outdoor pressure, obtained from the Pressures.py file
pres_out = [1007.6,1008.0,1008.2,1008.0,1008.1,1008.1,1008.3,1008.5,1008.8,1009.3,1009.9,1010.3,1010.7]
time_out = [8,9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

plt.figure(figsize=(15,4))
plt.grid()

plt.plot(times, pressures, color='red', label='Indoor', zorder=-1, alpha=0.7)
plt.plot(time_out, pres_out, color='blue', label='Outdoor', marker='.', zorder=3, alpha=1)
plt.xlabel('Local Time (h)', fontsize=12)
plt.ylabel('Pressure (hPa)', fontsize=15)
plt.title('Pressure comparison, Indoor vs Outdoors', fontsize=17)

plt.xticks(fontsize=10)
plt.yticks(fontsize=13)
plt.xticks(np.arange(8, 21, step=1)) #Display time stamps as mentioned for clarity

plt.legend(loc='upper left')
plt.show()
#%%
#This section plots the amount of particles of size 0.3-0.5 um from a file,
#creating a histogram of how many particles were detected every 10 minutes.

particle_sizes = ["particles 03um", "particles 05um", "particles 10um", "particles 25um", "particles 50um", "particles 100um"]

#Separate particles into size categories.
#The particles recorded are saved as bigger than 0.3um, bigger than 0.5um...
result3um = []
result5um = []
result10um = []
result25um = []
result50um = []
result100um = []
all_sizes = []
for i in range(8521,len(p3s)): #select a range of data you want to investigate
    result3um.append(int(p3s[i]) - int(p5s[i]) - int(p10s[i]) - int(p25s[i]) - int(p50s[i]) - int(p100s[i]))
    result5um.append(int(p5s[i]) - int(p10s[i]) - int(p25s[i]) - int(p50s[i]) - int(p100s[i]))
    result10um.append(int(p10s[i]) - int(p25s[i]) - int(p50s[i]) - int(p100s[i]))
    result25um.append(int(p25s[i]) - int(p50s[i]) - int(p100s[i]))
    result50um.append(int(p50s[i]) - int(p100s[i]))
    result100um.append(int(p100s[i]))

#To eliminate any errors, when no particles are left due to the way they are saved
#i.e. there are particles bigger than 0.3um but none are bigger than 2.5um
#they are assigned the value zero in their bin.
for term in [result3um, result5um, result10um, result25um, result50um, result100um]:
    for i, val in enumerate(term):
        if val < 0:
            term[i] = 0
            
particle_data = {}
particle_data["particles 03um"] = result3um
particle_data["particles 05um"] = result5um
particle_data["particles 10um"] = result10um
particle_data["particles 25um"] = result25um
particle_data["particles 50um"] = result50um
particle_data["particles 100um"] = result100um

window_size = 120 #adjust according to the time interval
total_points = len(particle_data["particles 03um"])

# Calculate the number of data points to consider
num_part = total_points // window_size

#Create an array to store average values
averaged_values = np.zeros(num_part)

# Calculate the average of every 120 points
for i in range(num_part):
    start_idx = i * window_size
    end_idx = (i + 1) * window_size
    averaged_values[i] = np.mean(particle_data["particles 03um"][start_idx:end_idx])

num_intervals = len(times) // 120

#Create an array to store time for each 10-minute interval
time_intervals = np.zeros(num_intervals)

#Assigning timestamps for each 10-minute interval
for i in range(num_intervals):
    time_intervals[i] = i * 10 

fig, ax1 = plt.subplots(figsize=(8, 6))
plt.grid()
ax2.set_axisbelow(True) #x-axis shared between the number of particles and humidity

# Create a second y-axis for Temperature on the right side
ax2 = ax1.twinx()
ax2.hist(time_intervals, bins=num_intervals, weights=averaged_values, edgecolor='black', zorder=3)

ax2.set_ylabel('Average number over 10 minute intervals')
ax2.tick_params(axis='y')
ax2.set_ylim([0,400])
ax1.set_ylim([0,40])

#Time is here set from zero to some number of minutes recorded
#Therefore, subtract the decimal time of the first data point
for k in range(len(times)):
    times[k]=(times[k]-9.221876116944445)*60 
 
# Plot CO2 concentration on the left y-axis
ax1.scatter(times, humidity,label='Humidity BME', marker='.', zorder=2)
ax1.scatter(times, humsscd, label='Humidity SCD', marker='.', zorder=1)
ax1.set_xlabel('Time (min)')
ax1.set_ylabel('Relative Humidity (%)')
ax1.tick_params(axis='y')

plt.title('Concentration of particles sized 0.3-0.5 um')

lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper left')

plt.show()
#%%
#Plotting 4 sub-plots for chosen file, displays temperature, pressure, humidity and CO2 separately

# Create a 2x2 grid of subplots
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
fig.suptitle('Particulates')

# Scatter plot in the top-left subplot with a legend
axes[0, 0].scatter((date), temperatures, label='BME280', marker='.')
axes[0, 0].scatter((date), tempsscd, label='SCD30', marker='.')
axes[0, 0].set_title('Temperature plot')
axes[0, 0].legend(loc='upper left')
axes[0, 0].set_ylabel('°C')
axes[0, 0].grid()

# Scatter plot in the top-right subplot with a legend
axes[0, 1].scatter(date, humidity, label='BME280', marker='.')
axes[0, 1].scatter(date, humsscd, label='SCD30', marker='.')
axes[0, 1].set_title('Humidity plot')
axes[0, 1].legend(loc='upper right')
axes[0, 1].set_ylabel('%')
axes[0, 1].grid()


# Scatter plot in the bottom-left subplot with a legend
axes[1, 0].scatter(date, CO2s, label='SCD30', marker='.')
axes[1, 0].set_title('CO2 plot')
axes[1, 0].legend(loc='upper right')
axes[1, 0].set_ylabel('PPM')
axes[1, 0].grid()


# Scatter plot in the bottom-right subplot with a legend
axes[1, 1].scatter(date, pressures, label='BME280', marker='.')
axes[1, 1].set_title('Pressure plot')
axes[1, 1].legend(loc='upper right')
axes[1, 1].set_ylabel('hPa')
axes[1, 1].grid()


# Add labels to the subplots
for i in range(2):
    for j in range(2):
        axes[i, j].set_xlabel('Time')
        axes[i, j].set_xticklabels(date, rotation=60)
        axes[i, j].xaxis.set_major_locator(HourLocator(interval=1))
        axes[i, j].xaxis.set_major_formatter(DateFormatter('%d. %m. %H:00'))
        axes[i, j].tick_params(which='major', axis='x', labelsize=8)

# Adjust spacing between subplots
plt.tight_layout()

# Show the plot
plt.show()
#%%
