import machine
import urequests as requests
import network
import time
import credentials



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


try:
    connect_to_wifi(credentials.INTERNET_NAME , credentials.INTERNET_PASSWORD)
    # Need to substitute from DATA API
    url = "https://eu-central-1.aws.data.mongodb-api.com/app/data-lwaix/endpoint/data/v1/action/insertOne"
    headers = { "api-key": "4tFRaI603cCb5aVF6l4wPYSDC6PsIHWw6VOLr4dFzSu86jDDQLRklSmqS2PSoLnx" }

    documentToAdd = {"device": "MyPico", "readings": [77, 80, 40, 60, 70, 80, 10]}

    insertPayload = {
        "dataSource": "Cluster0",
        "database": "MSYPicoSensorData",
        "collection": "ACS712-5A",
        "document": documentToAdd,
    }

    print("sending...")

    response = requests.post(url, headers=headers, json=insertPayload)

    print("Response: (" + str(response.status_code) + "), msg = " + str(response.text))

    if response.status_code == 201:
        print("Added Successfully")
    else:
        print("Error")

    # Always close response objects so we don't leak memory
    response.close()

except Exception as e:
    print(e)
 