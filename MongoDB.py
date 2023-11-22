from machine import Pin, RTC 
import machine 
import urequests as requests
import network
import time
import ntptime
import utime
import credentials

sensor_pin = machine.ADC(26)  

# //////////////////////////////////////////////////////////////

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


def findOne(filter_dictionary):
    try:
        headers = { "api-key": API_KEY }
        searchPayload = {
            "dataSource": "Cluster0",
            "database": "BME280",
            "collection": "Readings",
            "filter": filter_dictionary,
        }
        response = requests.post(URL + "findOne", headers=headers, json=searchPayload)
        print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        if response.status_code >= 200 and response.status_code < 300:
            print("Success Response")
        else:
            print(response.status_code)
            print("Error")
        response.close()
    except Exception as e:
        print(e)
        
        
def find(filter_dictionary):
    try:
        headers = { "api-key": API_KEY }
        searchPayload = {
            "dataSource": "Cluster0",
            "database": "BME280",
            "collection": "Readings",
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
        

def insertOne(pinvalue, time):
    try:
        headers = { "api-key": API_KEY }
        documentToAdd = {"Device": "ACS712-5A",
                         "AnalogPinValue": pinvalue,
                         "Time": time}
        insertPayload = {
            "dataSource": "Cluster0",
            "database": "MSYPicoSensorData",
            "collection": "ACS712-5A",
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
        
        
def insertMany(document_list):
    try:
        headers = { "api-key": API_KEY }
        insertPayload = {
            "dataSource": "Cluster0",
            "database": "BME280",
            "collection": "Readings",
            "documents": document_list,
        }
        response = requests.post(URL + "insertMany", headers=headers, json=insertPayload)
        print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        if response.status_code >= 200 and response.status_code < 300:
            print("Success Response")
        else:
            print(response.status_code)
            print("Error")
        response.close()
    except Exception as e:
        print(e)
        
        
def updateOne(filter_dictionary, update_dict):
    try:
        headers = { "api-key": API_KEY }
        update = {"set": update_dict}
        searchPayload = {
            "dataSource": "Cluster0",
            "database": "BME280",
            "collection": "Readings",
            "filter": filter_dictionary,
            "update": update_dict,
        }
        response = requests.post(URL + "updateOne", headers=headers, json=searchPayload)
        print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        if response.status_code >= 200 and response.status_code < 300:
            print("Success Response")
        else:
            print(response.status_code)
            print("Error")
        response.close()
    except Exception as e:
        print(e)
        
        
def deleteOne(filter_dictionary):
    try:
        headers = { "api-key": API_KEY }
        searchPayload = {
            "dataSource": "Cluster0",
            "database": "BME280",
            "collection": "Readings",
            "filter": filter_dictionary,
        }
        response = requests.post(URL + "delete", headers=headers, json=searchPayload)
        print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))
        if response.status_code >= 200 and response.status_code < 300:
            print("Success Response")
        else:
            print(response.status_code)
            print("Error")
        response.close()
    except Exception as e:
        print(e)

 

def main():
    connect_to_wifi(credentials.INTERNET_NAME, credentials.INTERNET_PASSWORD)
    #document_list = []
    while True:
        sensor_value = sensor_pin.read_u16()
        # temp, pressure, humidity = bme.values
        print(sensor_value)
        rtc_time_tuple = RTC().datetime()
        formatted_time = "{:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(
            rtc_time_tuple[0], rtc_time_tuple[1], rtc_time_tuple[2], 
            rtc_time_tuple[4], rtc_time_tuple[5], rtc_time_tuple[6]
        )
        print(formatted_time)
        
        insertOne(sensor_value, formatted_time)
        
        #document_list.append({"Device": "BME280",
            #"Temperature (C)": temp,
            #"Pressure": pressure,
            #"Humidity": humidity,
            #"Time": formatted_time}
        #)
        #if len(document_list) == 10:
           #print(json.dumps(document_list))
           #insertMany(document_list)
           #document_list = []
        #findOne({"Temperature (C)": "23.26C", "Humidity": "53.69%"})
        #find({"Temperature (C)": "24.65C"})
        #updateOne({"Temperature (C)": "23.26C"}, {"Temperature (C)": "24.26C"})
        # deleteOne({"Temperature (C)": "24.26C"})

main()