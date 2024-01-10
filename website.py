import network
import time

ssid = "WLAN-197399"
password = "32734056271867621744"

wlan = network.WLAN(network.STA_IF)

def connect_to_wifi():
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        time.sleep(1)
    print("Verbunden mit WiFi:", ssid)

connect_to_wifi()