from machine import Pin, RTC 
import machine 
import urequests as requests
import network
import time
import ntptime
import utime
import credentials

sensor_pin = machine.ADC(26)  
sensor_pin2 = machine.ADC(27)  
ntptime.settime()

UREF = 3.3 
# NULLPUNKT = 2.5371
NULLPUNKT = 2.5253
VpA = 0.1331
VpA2 = 0.1
Ucharge = 5
Ucharge2 = 20


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


# def findOne(filter_dictionary):
    # try:
    #     headers = { "api-key": API_KEY }
    #     searchPayload = {
    #         "dataSource": "Cluster0",
    #         "database": "BME280",
    #         "collection": "Readings",
    #         "filter": filter_dictionary,
    #     }
    #     response = requests.post(URL + "findOne", headers=headers, json=searchPayload)
    #     print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
    #     if response.status_code >= 200 and response.status_code < 300:
    #         print("Success Response")
    #     else:
    #         print(response.status_code)
    #         print("Error")
    #     response.close()
    # except Exception as e:
    #     print(e)
        
        
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
        

def insertOne(sensor, year, month, day, hour, minute, second, pinvalue):
    try:
        headers = { "api-key": API_KEY }
        documentToAdd = {"Sensor": sensor,
                         "year": year,
                         "month": month,
                         "day": day,
                         "hour": hour,
                         "minute": minute,
                         "second": second,
                         "Chargingpower": pinvalue}
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
        
        
# def insertMany(document_list):
    # try:
    #     headers = { "api-key": API_KEY }
    #     insertPayload = {
    #         "dataSource": "Cluster0",
    #         "database": "BME280",
    #         "collection": "Readings",
    #         "documents": document_list,
    #     }
    #     response = requests.post(URL + "insertMany", headers=headers, json=insertPayload)
    #     print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
    #     if response.status_code >= 200 and response.status_code < 300:
    #         print("Success Response")
    #     else:
    #         print(response.status_code)
    #         print("Error")
    #     response.close()
    # except Exception as e:
    #     print(e)
        
        
# def updateOne(filter_dictionary, update_dict):
    # try:
    #     headers = { "api-key": API_KEY }
    #     update = {"set": update_dict}
    #     searchPayload = {
    #         "dataSource": "Cluster0",
    #         "database": "BME280",
    #         "collection": "Readings",
    #         "filter": filter_dictionary,
    #         "update": update_dict,
    #     }
    #     response = requests.post(URL + "updateOne", headers=headers, json=searchPayload)
    #     print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
    #     if response.status_code >= 200 and response.status_code < 300:
    #         print("Success Response")
    #     else:
    #         print(response.status_code)
    #         print("Error")
    #     response.close()
    # except Exception as e:
    #     print(e)
        
        
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


        # print(moving_average)
        # print(moving_average2)
        chargingPower = ((((moving_average/65535)* UREF) - NULLPUNKT)/VpA)*(-Ucharge)
        chargingPower2 = ((((moving_average2/65535)* UREF) - NULLPUNKT)/VpA2)*(Ucharge2)
        # print("GMA1: ",((((moving_average/65535)* UREF) - NULLPUNKT)/VpA))
        # print("GMA2 :", (((moving_average2/65535)*UREF) - NULLPUNKT)/VpA2)
        # print(chargingPower)
        # print(chargingPower2)
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
        sensor1 = "ACS712-5A"
        sensor2 = "ACS712-20A"
        # print(formatted_time)              
        # insertOne("ACS712-5A", 2023, 12, 4, 18, 57, 50, 0)

        # insertOne(sensor1, year, month, day, hour, minute, second, chargingPower)
        # insertOne(sensor2, year, month, day, hour, minute, second, chargingPower2)
        # deleteMany({"day": 4})
        find({"day": 6})


main()