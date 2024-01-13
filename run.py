"""
This file is used to run the sensors, to obtain data.
"""
#Import all neccessary libraries, all available on the manufacturers websites
#of every sensor.
import time
from datetime import datetime
import serial #PMS5003
from adafruit_pm25.uart import PM25_UART #PMS5003
import board #SCD30
import busio #SCD30
import adafruit_scd30 #SCD30
try:
    from smbus2 import SMBus #BME280
except ImportError:
    from smbus import SMBus
from bme280 import BME280 #BME280
#%%
#To ensure the sensors do not get stuck on the same values, the function below
#resets the PMS5003 sensor.
def reset_pm25():
    global reset_pin
    global uart
    global pm25
    
    reset_pin = None
    uart = serial.Serial('/dev/serial0', baudrate=9600, timeout=0.25)
    pm25 = PM25_UART(uart, reset_pin)

#Similarly, if the BME280 sesnors gets stuck on the same value of the value drops
#below a certain value, it resets.
def reset_bme280():
    global bus
    global bme280
    
    bus = SMBus(1)
    bme280 = BME280(i2c_dev=bus)

#In case of any problems with the SCD30, it can be reset too.
def reset_scd30():
    global i2c
    global scd
    # SCD-30 has tempremental I2C with clock stretching, datasheet recommends
    # starting at 50KHz
    i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
    scd = adafruit_scd30.SCD30(i2c)
#%%
#Reset the sensors to ensure the first recorded values are accurate
reset_pm25()
reset_bme280()
reset_scd30()

# For detecting if dust sensor is working
previous_03_dust_measurement = None
same_dust_measurement_count = 0

start = time.perf_counter()

while True:
    file = open('11_12.txt', 'a') #choose a file, where data should be saved
    # since the measurement interval is long (2+ seconds) we check for new data before reading
    # the values, to ensure current readings.
    if scd.data_available:
        print("Data Available!")
        print("CO2: %d PPM" % scd.CO2)
        print("Temperature: %0.2f degrees C" % scd.temperature)
        print("Humidity: %0.2f %% rH" % scd.relative_humidity)
        print("")
        print("Waiting for new data...")
        print("")
        
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()

    # Reset bme280 sensor when suddent drop in pressure
    if pressure < 700:
        print('resetting bme280')
        reset_bme280()
        while bme280.get_pressure() < 700:
            time.sleep(0.5)
        continue
    
    #Obtain the current date and time
    date = datetime.now()
    print(f'{temperature}C, {pressure}hPa, {humidity}% {date}')

    try:
        aqdata = pm25.read()
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        continue

    print()
    print("Concentration Units (standard)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )
    print("Concentration Units (environmental)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
    )
    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    print("---------------------------------------")

    if aqdata["particles 03um"] == previous_03_dust_measurement:
        same_dust_measurement_count += 1
    else:
        same_dust_measurement_count = 0
        
    previous_03_dust_measurement = aqdata["particles 03um"]
    
    # Reset dust sensor if we get the same dust measurement more than 10 times.
    if same_dust_measurement_count > 10:
        print('resetting dust sensor')
        reset_pm25()
        same_dust_measurement_count = 0
        
    # Save data here, remember the order of variables
    print(scd.CO2, scd.temperature, temperature, scd.relative_humidity, humidity, pressure, date, aqdata["particles 03um"], aqdata["particles 05um"], aqdata["particles 10um"], aqdata["particles 25um"], aqdata["particles 50um"], aqdata["particles 100um"], sep=', ', file=file)
    file.close()
    time.sleep(5)
#%%
