import machine
import time
import network
import socket
import time
import math

# sta_if = network.WLAN(network.STA_IF)
# sta_if.active(True)
# sta_if.connect("WLAN-197399", "32734056271867621744")

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.bind(('', 8081))
# s.listen(5)

# sta_if = network.WLAN(network.STA_IF)
# print(sta_if.ifconfig()[0])
# print("WLAN-Status:", sta_if.isconnected())


led = machine.Pin(25, machine.Pin.OUT)  
sensor_pin = machine.ADC(26)  

window_size = 1  # Größe des gleitenden Mittelwerts-Fensters
sensor_values = [0] * window_size  # Eine Liste, um die letzten Werte zu speichern
index = 0  # Index, um die Position des aktuellen Werts im Array zu verfolgen
total_sum = 0  # Summe aller bisherigen Werte
total_count = 0  # Anzahl der bisherigen Werte


UREF = 3.3
NULLPUNKT = 2.820 
VpA = 0.185

while True:
    # conn, addr = s.accept()
    # request = conn.recv(1024)
    # chargingPower = ((((moving_average/65535)*UREF) - NULLPUNKT)/VpA) * 5

    # response = "HTTP/1.1 200 OK\n\n" + "<html><head><style>h1 {text-align: center; font-family: Arial, sans-serif; padding: 200px;} body {height: 100vh; background: linear-gradient(to bottom, skyblue, cornflowerblue); overflow: hidden;} .cloud {top: 50%; width: 300px; height: 100px; animation-duration: 8s; position: absolute; left: 0; background: white; border-radius: 1000px; animation: zoomies ".format(chargingPower) + "s infinite linear;} .cloudb {top: 44%; width: 150px; height: 90px; animation-duration: 8s; position: absolute; left: 20px; background: white; border-radius: 1000px; animation: zoomies ".format(chargingPower) + "s infinite linear;} .cloud::before {content: ""; position: absolute; top: -80%; left: 10%; width: 50%; height: 150%; background: white; border-radius: 50%;} @keyframes zoomies {from {left: 0; transform: translateX(-100%);} to {left: 100%; transform: translateX(0%);}}</style></head><body><div class='cloud'></div><div class='cloudb'></div><h1>""Aktuelle Windgeschwindigkeit: " + "{:.2f}".format(chargingPower) + " m/s</h1></div></body></html>"
    # conn.send(response.encode())
    # conn.close()
    
    led.on()
    sensor_value = sensor_pin.read_u16()  # Lese den analogen Wert

    total_sum += sensor_value  # Addiere den aktuellen Wert zur Gesamtsumme
    total_count += 1  # Inkrementiere die Anzahl der bisherigen Werte

    sensor_values[index] = sensor_value  # Aktualisiere den Wert in der Liste
    index = (index + 1) % window_size  # Aktualisiere den Index zyklisch

    # Berechne den gleitenden Mittelwert der letzten zehn Werte
    moving_average = sum(sensor_values) / window_size
    overall_average = total_sum / total_count
    
    chargingPower = ((((moving_average/65535)*UREF) - NULLPUNKT)/VpA) * 5


    #print("Aktueller Analogwert:", sensor_value)
    print("Gleitender Mittelwert der letzten 10 Werte:", (moving_average/65535)*UREF)
    print("Gleitender Amperewert der letzten 10 Werte:", (((moving_average/65535)*UREF) - NULLPUNKT)/VpA)
    print("Gesamtmittelwert aller bisherigen Werte:", (overall_average/65535)*UREF)
    #print("Gleitender Amperewert der letzten 10 Werte:", (((overall_average/65535)*UREF) - NULLPUNKT)/VpA)
    
    time.sleep(1)