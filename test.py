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
sensor_pin2 = machine.ADC(27)  

index = 0  # Index, um die Position des aktuellen Werts im Array zu verfolgen
total_sum = 0  # Summe aller bisherigen Werte
total_count = 0  # Anzahl der bisherigen Werte
window_size = 10  # Größe des gleitenden Mittelwerts-Fensters
sensor_values = [0] * window_size  # Eine Liste, um die letzten Werte zu speichern
sensor_values2 = [0] * window_size  # Eine Liste, um die letzten Werte zu speichern


UREF = 3.3
# NULLPUNKT = 2.5371
NULLPUNKT = 2.515
VpA = 0.1331
VpA2 = 0.1

def start_server():
    addr = wlan.ifconfig()[0]
    port = 90

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((addr, port))
    s.listen(5)

    print('Web server started on {}:{}'.format(addr, port))

    index = 0 

    while True:
        led.on()
        sensor_value = sensor_pin.read_u16()  # Lese den analogen Wert
        sensor_value2 = sensor_pin2.read_u16()  # Lese den analogen Wert

        sensor_values[index] = sensor_value  # Aktualisiere den Wert in der Liste
        sensor_values2[index] = sensor_value2  # Aktualisiere den Wert in der Liste
        index = (index + 1) % window_size  # Aktualisiere den Index zyklisch

        # Berechne den gleitenden Mittelwert der letzten zehn Werte
        moving_average = sum(sensor_values) / window_size
        moving_average2 = sum(sensor_values2) / window_size

        # print("GleitWertU 1:", (moving_average/65535)*UREF)
        print("MoAv",moving_average2)
        print("GleitWertU 1:", (moving_average2/65535)*UREF)
        # print("GleitWertA :", (((moving_average/65535)*UREF) - NULLPUNKT)/VpA)
        # print("GleitWertA :", (((moving_average2/65535)*UREF) - NULLPUNKT)/VpA2)
        # print("Gesamtmittelwert aller bisherigen Werte:", (overall_average/65535)*UREF)
        # print("Gesamtmittelwert Amperewert:", (((overall_average/65535)*UREF) - NULLPUNKT)/VpA)

        chargingPower = ((((moving_average/65535)*UREF) - NULLPUNKT)/VpA) * 5

        conn, addr = s.accept()
        print('Connection from {}'.format(addr))
        request = conn.recv(1024)
        print('Request: {}'.format(request))
       
        html_content = """<!DOCTYPE html>
<html>
<head>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Comic+Sans+MS&display=swap');
    </style>
</head>
<body style="background: linear-gradient(to right, #87CEEB, #FFFF00); text-align:center; vertical-align:middle; font-family:'Comic Sans MS',cursive;">
    <h1 style="color: white; margin-top: 1%;">SOLARBANK</h1>
    <div style="display: flex; justify-content: space-around; align-items: center; height: 60vh;">
        <div style="flex: 1; background-color: rgba(144, 238, 144, 0); padding: 20px; box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.3); border-radius: 15px;">
            <h2>PV-Modulenergie</h2>
<svg width="575" height="341" viewBox="0 0 575 341" fill="none" xmlns="http://www.w3.org/2000/svg">
<g id="Frame 4">
<path id="Ellipse 2" d="M152.5 226C152.5 255.049 129.838 278.5 102 278.5C74.1625 278.5 51.5 255.049 51.5 226C51.5 196.951 74.1625 173.5 102 173.5C129.838 173.5 152.5 196.951 152.5 226Z" stroke="#07048F" stroke-width="3"/>
<path id="Ellipse 6" d="M297.5 77C297.5 106.049 274.838 129.5 247 129.5C219.162 129.5 196.5 106.049 196.5 77C196.5 47.9512 219.162 24.5 247 24.5C274.838 24.5 297.5 47.9512 297.5 77Z" stroke="#FFD600" stroke-width="3"/>
<path id="Ellipse 5" d="M446.5 221.5C446.5 250.811 423.403 274.5 395 274.5C366.597 274.5 343.5 250.811 343.5 221.5C343.5 192.189 366.597 168.5 395 168.5C423.403 168.5 446.5 192.189 446.5 221.5Z" stroke="#33A716" stroke-width="3"/>
<path id="Rectangle 1" d="M254 138V189C254 203.142 254 210.213 258.393 214.607C262.787 219 269.858 219 284 219H335" stroke="url(#paint0_linear_103_2)" stroke-width="3"/>
<path id="Rectangle 2" d="M161 219H209C223.142 219 230.213 219 234.607 214.607C239 210.213 239 203.142 239 189V138" stroke="url(#paint1_linear_103_2)" stroke-width="3"/>
<g id="172581_battery_charge_icon 1" clip-path="url(#clip0_103_2)">
<path id="Vector" d="M389.08 189.86V194.72H383.16C379.891 194.72 377.24 197.621 377.24 201.2V253.04C377.24 256.619 379.891 259.52 383.16 259.52H406.84C410.109 259.52 412.76 256.619 412.76 253.04V201.2C412.76 197.621 410.109 194.72 406.84 194.72H400.92V189.86H389.08Z" stroke="black" stroke-width="2" stroke-miterlimit="10" stroke-linecap="round" stroke-linejoin="round"/>
<path id="Vector_2" d="M396.48 243.32L389.08 225.5H395L393.52 210.92L400.92 228.74H395L396.48 243.32Z" fill="black"/>
</g>
<g id="1101625351623422786 1">
<path id="Vector_3" d="M87.3 231.6V203.2H82.5664V210.3H73.1V215.034H82.5664V219.766H73.1V224.5H82.5664V231.6H87.3Z" fill="black"/>
<path id="Vector_4" d="M120.436 215.034H107.786L98.726 205.974C97.0121 204.259 94.6449 203.2 92.0336 203.2V231.6C94.6449 231.6 97.0121 230.541 98.7267 228.827L107.787 219.766H120.436C123.05 219.766 125.166 221.888 125.166 224.5V245.8H129.9V224.5C129.9 219.272 125.663 215.034 120.436 215.034Z" fill="black"/>
</g>
<g id="8012437951535694872 1">
<g id="Group">
<g id="Group_2">
<path id="Vector_5" d="M247 94.862C256.853 94.862 264.798 86.8527 264.798 77.0636C264.798 67.2744 256.789 59.2651 247 59.2651C237.211 59.2651 229.202 67.2744 229.202 77.0636C229.202 86.8527 237.147 94.862 247 94.862ZM247 64.4139C253.992 64.4139 259.65 70.0713 259.65 77.0636C259.65 84.0558 253.992 89.7132 247 89.7132C240.008 89.7132 234.35 84.0558 234.35 77.0636C234.35 70.0713 240.008 64.4139 247 64.4139Z" fill="black"/>
<path id="Vector_6" d="M249.606 51.0015V42.8015C249.606 41.3395 248.462 40.1953 247 40.1953C245.538 40.1953 244.394 41.3395 244.394 42.8015V51.0015C244.394 52.4636 245.538 53.6077 247 53.6077C248.462 53.6077 249.606 52.4636 249.606 51.0015Z" fill="black"/>
<path id="Vector_7" d="M244.394 103.126V111.326C244.394 112.788 245.538 113.932 247 113.932C248.462 113.932 249.606 112.788 249.606 111.326V103.126C249.606 101.664 248.462 100.519 247 100.519C245.538 100.519 244.394 101.664 244.394 103.126Z" fill="black"/>
<path id="Vector_8" d="M267.277 60.4728L273.062 54.6884C274.079 53.6713 274.079 52.0186 273.062 51.0015C272.045 49.9845 270.392 49.9845 269.375 51.0015L263.591 56.786C262.574 57.8031 262.574 59.4558 263.591 60.4728C264.099 60.9814 264.735 61.2356 265.434 61.2356C266.133 61.2356 266.769 60.9814 267.277 60.4728Z" fill="black"/>
<path id="Vector_9" d="M220.938 103.126C221.446 103.634 222.082 103.888 222.781 103.888C223.417 103.888 224.116 103.634 224.625 103.126L230.409 97.3411C231.426 96.324 231.426 94.6713 230.409 93.6543C229.392 92.6372 227.74 92.6372 226.722 93.6543L220.938 99.4388C219.921 100.456 219.921 102.109 220.938 103.126Z" fill="black"/>
<path id="Vector_10" d="M283.868 77.0636C283.868 75.6016 282.724 74.4574 281.262 74.4574H273.062C271.6 74.4574 270.456 75.6016 270.456 77.0636C270.456 78.5256 271.6 79.6698 273.062 79.6698H281.262C282.66 79.6698 283.868 78.5256 283.868 77.0636Z" fill="black"/>
<path id="Vector_11" d="M212.738 79.6698H220.938C222.4 79.6698 223.544 78.5256 223.544 77.0636C223.544 75.6016 222.4 74.4574 220.938 74.4574H212.738C211.276 74.4574 210.132 75.6016 210.132 77.0636C210.132 78.5256 211.34 79.6698 212.738 79.6698Z" fill="black"/>
<path id="Vector_12" d="M271.219 103.888C271.854 103.888 272.553 103.634 273.062 103.126C274.079 102.109 274.079 100.456 273.062 99.4388L267.277 93.6543C266.26 92.6372 264.608 92.6372 263.591 93.6543C262.574 94.6713 262.574 96.324 263.591 97.3411L269.375 103.126C269.884 103.634 270.583 103.888 271.219 103.888Z" fill="black"/>
<path id="Vector_13" d="M230.409 60.4728C231.426 59.4558 231.426 57.8031 230.409 56.786L224.625 51.0015C223.608 49.9845 221.955 49.9845 220.938 51.0015C219.921 52.0186 219.921 53.6713 220.938 54.6884L226.722 60.4728C227.231 60.9814 227.867 61.2356 228.566 61.2356C229.265 61.2356 229.901 60.9814 230.409 60.4728Z" fill="black"/>
</g>
</g>
</g>
</g>
<defs>
<linearGradient id="paint0_linear_103_2" x1="254" y1="138" x2="335" y2="219" gradientUnits="userSpaceOnUse">
<stop offset="0.364198" stop-color="#FFD600"/>
<stop offset="1" stop-color="#007D05"/>
</linearGradient>
<linearGradient id="paint1_linear_103_2" x1="161" y1="219" x2="239" y2="138" gradientUnits="userSpaceOnUse">
<stop stop-color="#2400FF"/>
<stop offset="0.678292" stop-color="#FFD600"/>
</linearGradient>
<clipPath id="clip0_103_2">
<rect width="81" height="74" fill="white" transform="matrix(0 -1 1 0 358 266)"/>
</clipPath>
</defs>
</svg>


        </div>
    </div>
</body>
</html>""".format((moving_average/65535)*UREF)

        response = 'HTTP/1.0 200 OK\r\n\r\n{}'.format(html_content)
        # print("Aktueller Analogwert:", sensor_value)
        # print("Gleitender Mittelwert der letzten 10 Werte:", (moving_average/65535)*UREF)
        # print("Gleitender Amperewert der letzten 10 Werte:", (((moving_average/65535)*UREF) - NULLPUNKT)/VpA)
        # print("Gesamtmittelwert aller bisherigen Werte:", (overall_average/65535)*UREF)
        # print("Gleitender Amperewert der letzten 10 Werte:", (((overall_average/65535)*UREF) - NULLPUNKT)/VpA)

        conn.send(response)
        conn.close()

start_server()
