import machine
import time
import network
import socket
import time
import math
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
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
def start_server():
    addr = wlan.ifconfig()[0]
    port = 83
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((addr, port))
    s.listen(5)
    print('Web server started on {}:{}'.format(addr, port))
    while True:
        led.on()
        sensor_value = sensor_pin.read_u16()  # Lese den analogen Wert
        window_size = 20  # Größe des gleitenden Mittelwerts-Fensters
        sensor_values = [0] * window_size  # Eine Liste, um die letzten Werte zu speichern
        index = 0  # Index, um die Position des aktuellen Werts im Array zu verfolgen
        total_sum = 0  # Summe aller bisherigen Werte
        total_count = 0  # Anzahl der bisherigen Werte
        total_sum += sensor_value  # Addiere den aktuellen Wert zur Gesamtsumme
        total_count += 1  # Inkrementiere die Anzahl der bisherigen Werte
        sensor_values[index] = sensor_value  # Aktualisiere den Wert in der Liste
        index = (index + 1) % window_size  # Aktualisiere den Index zyklisch
        # Berechne den gleitenden Mittelwert der letzten zehn Werte
        moving_average = sum(sensor_values) / window_size
        overall_average = total_sum / total_count
        print("Gesamtmittelwert aller bisherigen Werte:", (overall_average/65535)*UREF)
        chargingPower = ((((moving_average/65535)*UREF) - NULLPUNKT)/VpA) * 5
        conn, addr = s.accept()
        print('Connection from {}'.format(addr))
        request = conn.recv(1024)
        print('Request: {}'.format(request))
        html_content = '<!DOCTYPE html>\n<html><body style="background: linear-gradient(to bottom, white, yellow);text-align:center;vertical-align:middle;line-height:100vh;"><div style="display:inline-block;font-size:24px;color:black;">Die aktuelle Ladeleistung betraegt {} Watt</div></body></html>'.format(chargingPower)
        response = 'HTTP/1.0 200 OK\r\n\r\n{}'.format(html_content)
        # response = 'HTTP/1.0 200 OK\r\n\r\n<!DOCTYPE html>\n<html><body style="background-color:white">{}</body></html>'.format((overall_average/65535)*UREF)
        # print("Aktueller Analogwert:", sensor_value)
        # print("Gleitender Mittelwert der letzten 10 Werte:", (moving_average/65535)*UREF)
        # print("Gleitender Amperewert der letzten 10 Werte:", (((moving_average/65535)*UREF) - NULLPUNKT)/VpA)
        # print("Gesamtmittelwert aller bisherigen Werte:", (overall_average/65535)*UREF)
        # print("Gleitender Amperewert der letzten 10 Werte:", (((overall_average/65535)*UREF) - NULLPUNKT)/VpA)
        conn.send(response)
        conn.close()
start_server()