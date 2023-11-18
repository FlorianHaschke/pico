import machine
import time
import network
import socket
import urequests  # Make sure this module is available on your Pico
import ujson

# Your existing code...

def send_to_influxdb_cloud(org, bucket, token, measurement, fields):
    influxdb_url = "https://{}.influxdata.com/api/v2/write?org={}&bucket={}&precision=s".format(org, org, bucket)
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Token {}".format(token)
    }

    data = "{},{} {}".format(measurement, ",".join(["{}={}".format(key, value) for key, value in fields.items()]), int(time.time()))

    try:
        response = urequests.post(influxdb_url, data=data, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response.close()
    except Exception as e:
        print("Error sending data to InfluxDB Cloud:", e)

def start_server():
    # Your existing code...

    # Set your InfluxDB Cloud credentials
    org = "TH-Nuernberg"
    bucket = "test"
    token = "L4rmaGMXkzxL9kM9vjdpvDcFoqGOcAiWmwmwTvQb2464m1iFVZwZL4TIBf2j2bnU8UMAsZzGn0NITELl_Me-bQ=="

    while True:
        # Your existing code...

        charging_power = 1000
        data_to_send = {"charging_power": charging_power}
        send_to_influxdb_cloud(org, bucket, token, "power_measurement", data_to_send)
        print(data_to_send)

        # Your existing code...

# Rest of your code...
start_server()