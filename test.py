import machine
import time
import network
import socket
import time
import math
import ujson
import urequests 

sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
# sta_if.connect("WLAN-197399", "32734056271867621744")
sta_if.connect("stefan Fritzbox", "32103449752892365973")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 8081))
s.listen(5)

sta_if = network.WLAN(network.STA_IF)
print(sta_if.ifconfig()[0])
print("WLAN-Status:", sta_if.isconnected())

wlan = network.WLAN(network.STA_IF)
wlan.active(True)


led = machine.Pin(25, machine.Pin.OUT)  
sensor_pin = machine.ADC(26)  

index = 0  # Index, um die Position des aktuellen Werts im Array zu verfolgen
total_sum = 0  # Summe aller bisherigen Werte
total_count = 0  # Anzahl der bisherigen Werte
window_size = 10  # Größe des gleitenden Mittelwerts-Fensters
sensor_values = [0] * window_size  # Eine Liste, um die letzten Werte zu speichern


UREF = 3.3
NULLPUNKT = 2.5371
VpA = 0.1331

# def send_to_node_red(data):
#     node_red_url = "http://your-node-red-ip:your-node-red-port/your-endpoint"
#     headers = {"Content-Type": "application/json"}

#     try:
#         response = urequests.post(node_red_url, data=ujson.dumps(data), headers=headers)
#         response.close()
#     except Exception as e:
#         print("Error sending data to Node-RED:", e)



# def start_server():
    # addr = wlan.ifconfig()[0]
    # port = 89

    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # s.bind((addr, port))
    # s.listen(5)

    # print('Web server started on {}:{}'.format(addr, port))


while True:
        led.on()
        sensor_value = sensor_pin.read_u16()  # Lese den analogen Wert
        total_sum += sensor_value  # Addiere den aktuellen Wert zur Gesamtsumme
        total_count += 1  # Inkrementiere die Anzahl der bisherigen Werte

        sensor_values[index] = sensor_value  # Aktualisiere den Wert in der Liste
        index = (index + 1) % window_size  # Aktualisiere den Index zyklisch

        # Berechne den gleitenden Mittelwert der letzten zehn Werte
        moving_average = sum(sensor_values) / window_size
        overall_average = total_sum / total_count


        print("Gleitender Mittelwert der letzten 10 Werte:", (moving_average/65535)*UREF)
        print("Gleitender Amperewert der letzten 10 Werte:", (((moving_average/65535)*UREF) - NULLPUNKT)/VpA)
        print("Gesamtmittelwert aller bisherigen Werte:", (overall_average/65535)*UREF)
        print("Gesamtmittelwert Amperewert:", (((overall_average/65535)*UREF) - NULLPUNKT)/VpA)


        chargingPower = ((((moving_average/65535)*UREF) - NULLPUNKT)/VpA) * 5

        # conn, addr = s.accept()
        # print('Connection from {}'.format(addr))
        # request = conn.recv(1024)
        # print('Request: {}'.format(request))
       
        # html_content = """<!DOCTYPE html>
        # <html>
        # <head>
        #     <style>
        #         @import url('https://fonts.googleapis.com/css2?family=Comic+Sans+MS&display=swap');
        #     </style>
        # </head>
        # <body style="background-color:white; background-image:linear-gradient(to bottom, white, yellow); text-align:center; vertical-align:middle; line-height:100vh; margin:0; font-family:'Comic Sans MS',cursive;">
        #     <div style="display:flex; align-items:center; justify-content:center; font-size:5vw; color:black;">
                # Die aktuelle Ladeleistung betraegt {:.2f} Watt
        #     </div>
        # </body>
        # </html>""".format((overall_average/65535)*UREF)

        # response = 'HTTP/1.0 200 OK\r\n\r\n{}'.format(html_content)
        # print("Aktueller Analogwert:", sensor_value)
        # print("Gleitender Mittelwert der letzten 10 Werte:", (moving_average/65535)*UREF)
        # print("Gleitender Amperewert der letzten 10 Werte:", (((moving_average/65535)*UREF) - NULLPUNKT)/VpA)
        # print("Gesamtmittelwert aller bisherigen Werte:", (overall_average/65535)*UREF)
        # print("Gleitender Amperewert der letzten 10 Werte:", (((overall_average/65535)*UREF) - NULLPUNKT)/VpA)
        
        # data_to_send = {"charging_power": chargingPower}
        # send_to_node_red(data_to_send)

        # conn.send(response)
        # conn.close()
        time.sleep(1)




# start_server()

