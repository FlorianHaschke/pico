from machine import Pin, RTC 
import machine 
import urequests as requests
import network
import time
import ntptime
from time import sleep, sleep_us, ticks_us
import credentials
from machine import Pin


sensor_pin = machine.ADC(26)  
sensor_pin2 = machine.ADC(27)  


# Initialisierung GPIO-Ausgang für Trigger-Signal
trigger = Pin(2, Pin.OUT)

# Initialisierung GPIO-Eingang für Echo-Signal
echo = Pin(3, Pin.IN)

UREF = 3.3 
NULLPUNKT = 2.5253
# Volt per Ampere - Der Sensor hat eine hinterlegte Umrechnung der Voltmessung in einen Amperewert der hier gestzt wird
VpA = 0.1331
VpA2 = 0.1
U_Consumption = 24
U_Production = 12


URL = "https://eu-central-1.aws.data.mongodb-api.com/app/data-lwaix/endpoint/data/v1/action/"
API_KEY = "4tFRaI603cCb5aVF6l4wPYSDC6PsIHWw6VOLr4dFzSu86jDDQLRklSmqS2PSoLnx"

def connect_to_wifi(ssid, psk):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, psk)

    while not wlan.isconnected() and wlan.status() >= 0:
        print("Waiting to Connect")
        time.sleep(10)
    if not wlan.isconnected():
        raise Exception("Wifi not available")
    print("Connected to WiFi")

connect_to_wifi(credentials.INTERNET_NAME, credentials.INTERNET_PASSWORD)
ntptime.settime()    
        
def find(filter_dictionary):
    try:
        headers = { "api-key": API_KEY }
        searchPayload = {
            "dataSource": "Cluster0",
            "database": "MSYPicoSensorData",
            "collection": "ACS7125A",
            "filter": filter_dictionary,
        }
        response = requests.post(URL + "find", headers=headers, json=searchPayload)
        print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        if response.status_code >= 200 and response.status_code < 300:
            print("Success Response")
        else:
            print(response.status_code)
            print("Error")
        response.close()
    except Exception as e:
        print(e)
        
def insertData(sensor1, sensor2, sensor3, year, month, day, hour, minute, second, chargingPower, chargingPower2, inUse):
    try:
        headers = { "api-key": API_KEY }
        documentToAdd = {"Sensor": sensor1,
                         "year": year,
                         "month": month,
                         "day": day,
                         "hour": hour,
                         "minute": minute,
                         "second": second,
                         "Chargingpower": chargingPower}
        insertPayload = {
            "dataSource": "Cluster0",
            "database": "MSYPicoSensorData",
            "collection": "ACS7125A",
            "document": documentToAdd,
        }
        response = requests.post(URL + "insertOne", headers=headers, json=insertPayload)
        print(response)
        print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        if response.status_code >= 200 and response.status_code < 300:
            print("Success Response")
        else:
            print(response.status_code)
            print("Error")
        response.close()

    except Exception as e:
        print(e)

    try:
        headers = { "api-key": API_KEY }
        documentToAdd = {"Sensor": sensor2,
                         "year": year,
                         "month": month,
                         "day": day,
                         "hour": hour,
                         "minute": minute,
                         "second": second,
                         "Chargingpower": chargingPower2}
        insertPayload = {
            "dataSource": "Cluster0",
            "database": "MSYPicoSensorData",
            "collection": "ACS7125A",
            "document": documentToAdd,
        }
        response = requests.post(URL + "insertOne", headers=headers, json=insertPayload)
        print(response)
        print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        if response.status_code >= 200 and response.status_code < 300:
            print("Success Response")
        else:
            print(response.status_code)
            print("Error")
        response.close()
    except Exception as e:
        print(e)

    try:
        headers = { "api-key": API_KEY }
        documentToAdd = {"Sensor": sensor3,
                         "year": year,
                         "month": month,
                         "day": day,
                         "hour": hour,
                         "minute": minute,
                         "second": second,
                         "inUse": inUse}
        insertPayload = {
            "dataSource": "Cluster0",
            "database": "MSYPicoSensorData",
            "collection": "ACS7125A",
            "document": documentToAdd,
        }
        response = requests.post(URL + "insertOne", headers=headers, json=insertPayload)
        print(response)
        print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        if response.status_code >= 200 and response.status_code < 300:
            print("Success Response")
        else:
            print(response.status_code)
            print("Error")
        response.close()
    except Exception as e:
        print(e) 
    
    sleep(10)  

def insertOneUsage(sensor, year, month, day, hour, minute, second, pinvalue):
    try:
        headers = { "api-key": API_KEY }
        documentToAdd = {"Sensor": sensor,
                         "year": year,
                         "month": month,
                         "day": day,
                         "hour": hour,
                         "minute": minute,
                         "second": second,
                         "inUse": pinvalue}
        insertPayload = {
            "dataSource": "Cluster0",
            "database": "MSYPicoSensorData",
            "collection": "ACS7125A",
            "document": documentToAdd,
        }
        response = requests.post(URL + "insertOne", headers=headers, json=insertPayload)
        print(response)
        print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        if response.status_code >= 200 and response.status_code < 300:
            print("Success Response")
        else:
            print(response.status_code)
            print("Error")
        response.close()
    except Exception as e:
        print(e)
               
def deleteMany(filter_dictionary):
    try:
        headers = { "api-key": API_KEY }
        searchPayload = {
            "dataSource": "Cluster0",
            "database": "MSYPicoSensorData",
            "collection": "ACS7125A",
            "filter": filter_dictionary,
        }
        response = requests.post(URL + "deleteMany", headers=headers, json=searchPayload)
        print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        if response.status_code >= 200 and response.status_code < 300:
            print("Success Response")
        else:
            print(response.status_code)
            print("Error")
        response.close()
    except Exception as e:
        print(e)

window_size = 10  # Größe des gleitenden Mittelwerts-Fensters
sensor_values = [0] * window_size  # Eine Liste, um die letzten Werte zu speichern
sensor_values2 = [0] * window_size  # Eine Liste, um die letzten Werte zu speichern

def main():
    connect_to_wifi(credentials.INTERNET_NAME, credentials.INTERNET_PASSWORD)
    i = 1
    index = 0  # Index, um die Position des aktuellen Werts im Array zu verfolgen

    while True:
        sensor_value = sensor_pin.read_u16()
        sensor_value2 = sensor_pin2.read_u16()
        sensor_values[index] = sensor_value  # Aktualisiere den Wert in der Liste
        sensor_values2[index] = sensor_value2  # Aktualisiere den Wert in der Liste
        index = (index + 1) % window_size  # Aktualisiere den Index zyklisch
        moving_average = sum(sensor_values) / window_size
        moving_average2 = sum(sensor_values2) / window_size


        # Abstand messen
        trigger.low()
        sleep_us(2)
        trigger.high()
        sleep_us(5)
        trigger.low()
        # Zeiten messen
        while echo.value() == 0:
            signaloff = ticks_us()
        while echo.value() == 1:         
            signalon = ticks_us()
        # Vergangene Zeit ermitteln
        timepassed = signalon - signaloff # type: ignore
        # Abstand/Entfernung ermitteln
        # Entfernung über die Schallgeschwindigkeit (34320 cm/s bei 20 °C) berechnen
        # Durch 2 teilen, wegen Hin- und Rückweg
        abstand = timepassed * 0.03432 / 2

        # Setze die Variable seatSensor auf 1, falls der Abstand größer als 30 ist, sonst auf 0
        usage = 1 if abstand < 30 else 0

        chargingPower = ((((moving_average/65535)* UREF) - NULLPUNKT)/VpA)*(-U_Consumption)
        chargingPower2 = ((((moving_average2/65535)* UREF) - NULLPUNKT)/VpA2)*(U_Production)
        print("GMA1: ",((((moving_average/65535)* UREF) - NULLPUNKT)/VpA))
        print("GMA2 :", (((moving_average2/65535)*UREF) - NULLPUNKT)/VpA2)
        print("GMV1: ",((((moving_average/65535)* UREF) )))
        print("GMV2 :", (((moving_average2/65535)*UREF) ))
        print(abstand)
        print(usage)

        rtc_time_tuple = RTC().datetime()
        year = rtc_time_tuple[0]
        month = rtc_time_tuple[1]
        day = rtc_time_tuple[2]
        hour = rtc_time_tuple[4]
        minute = rtc_time_tuple[5]
        second = rtc_time_tuple[6]
        formatted_time = "{:04}-{:02}-{:02}T{:02}:{:02}:{:02}.0000Z".format(
            rtc_time_tuple[0], rtc_time_tuple[1], rtc_time_tuple[2], 
            rtc_time_tuple[4]+1, rtc_time_tuple[5], rtc_time_tuple[6]
        )
        currentSensor5a = "ACS712-5A"
        currentSensor20a = "ACS712-20A"
        seatSensor = "HC-SR04"
        # insertOneCurrent("ACS712-20A", 2023, 12, 13, 10, 57, 50, 0)

        insertData(currentSensor5a, currentSensor20a, seatSensor, year, month, day, hour, minute, second, chargingPower,chargingPower2,usage)
        # insertOneCurrent(currentSensor20a, year, month, day, hour, minute, second, chargingPower2)
        # insertOneUsage(seatSensor, year, month, day, hour, minute, second, usage)
        # deleteMany({"day": 13})
        # find({"day": 6})



main()
