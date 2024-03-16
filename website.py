import machine
import time
import network
import socket
import time
import math
import gc
import credentials



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
NULLPUNKT = 2.515
VpA = 0.1331
VpA2 = 0.1
Ucharge = 5
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


def start_server():
    free_memory_before = gc.mem_free()

    addr = wlan.ifconfig()[0]
    port = 91

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

        print("MoAv",moving_average2)
        print("GleitWertU 1:", (moving_average2/65535)*UREF)

        loadPower = int(((((moving_average/65535)* UREF) - NULLPUNKT)/VpA)*(-Ucharge))
        modulePower = int(((((moving_average2/65535)* UREF) - NULLPUNKT)/VpA2)*(-Ucharge))
        batteryPower = int(modulePower - loadPower)
        if loadPower<3: loadPower=0
        if modulePower<3: modulePower=0
        if abs(batteryPower)<3: batteryPower=0



        conn, addr = s.accept()
        print('Connection from {}'.format(addr))
        request = conn.recv(1024)
        print('Request: {}'.format(request))

        opacityValue1 = 0
        opacityValue2 = 0
        opacityValue3 = 0

        if modulePower < 3 or batteryPower < 3:
            opacityValue1 = 0
        else: opacityValue1 = 1
        if loadPower < 3 or modulePower < 3:
            opacityValue2 = 0
        else: opacityValue2 = 1
        if batteryPower > -3 or loadPower < 3:
            opacityValue3 = 0
        else: opacityValue3 = 1
        html_content = """<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="initial-scale=1, width=device-width" />

    <link
      rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Inter:wght@400&display=swap"
    />
    <link
      rel="stylesheet"
      href="https://fonts.googleapis.com/css2?family=Julius Sans One:wght@400&display=swap"
    />

    <style>
      body {
        margin: 0;
        line-height: normal;
      }
    </style>
  </head>
  <body>
    <div
      style="
        position: relative;
        background-color: #000;
        width: 100%;
        height: 812px;
        overflow: hidden;
        text-align: left;
        font-size: 12px;
        color: #fff;
        font-family: 'Julius Sans One';0
      "
    >
        <div
          style="
          position: absolute;
          top: 200px;
          left: -45;
        ">
              <div
        style="
          position: absolute;
          top: -394px;
          left: 178.3px;
          border-radius: 50%;
          background-color: #ffd600;
          filter: blur(120px);
          width: 490.1px;
          height: 233.9px;
          transform: rotate(20.09deg);
          transform-origin: 0 0;
        "
      ></div>
<svg width="439" height="287" viewBox="0 0 439 287" xmlns="http://www.w3.org/2000/svg">
<g id="Frame 5">
<path id="Ellipse 2" d="M135.5 193C135.5 217.073 116.648 236.5 93.5 236.5C70.3516 236.5 51.5 217.073 51.5 193C51.5 168.927 70.3516 149.5 93.5 149.5C116.648 149.5 135.5 168.927 135.5 193Z" stroke="#2906FA" stroke-width="3" fill="none"/>
<path id="Ellipse 6" d="M257.5 68C257.5 92.0563 238.441 111.5 215 111.5C191.559 111.5 172.5 92.0563 172.5 68C172.5 43.9437 191.559 24.5 215 24.5C238.441 24.5 257.5 43.9437 257.5 68Z" stroke="#FFD600" stroke-width="3" fill="none"/>
<path id="Ellipse 5" d="M382.5 189.5C382.5 213.832 363.217 233.5 339.5 233.5C315.783 233.5 296.5 213.832 296.5 189.5C296.5 165.168 315.783 145.5 339.5 145.5C363.217 145.5 382.5 165.168 382.5 189.5Z" stroke="#33A716" stroke-width="3" fill="none"/>
<path id="Rectangle 1" d="M222 119V158C222 172.142 222 179.213 226.393 183.607C230.787 188 237.858 188 252 188H289" stroke="url(#paint0_linear_118_173)" stroke-width="3" fill="none" opacity="OPACITY1"/>
<path id="Rectangle 2" d="M144 188H178C192.142 188 199.213 188 203.607 183.607C208 179.213 208 172.142 208 158V119" stroke="url(#paint1_linear_118_173)" stroke-width="3" fill="none" opacity="OPACITY2"/>
<text fill="#2906FA" x="64" y="198" font-size="19px" font-family="Julius Sans One">LOAD_POWER W</text> 
<text fill="#33A716" x="310" y="198" font-size="19px" font-family="Julius Sans One">BATTERY_POWER W</text> 
<text fill="#FFD600" x="189" y="76" font-size="19px" font-family="Julius Sans One">MODULE_POWER W</text> 
<line id="Line 6" x1="144" y1="195.5" x2="289" y2="195.5" stroke="url(#paint2_linear_118_173)" stroke-width="3" opacity="OPACITY3"/>
</g>
<defs>
<linearGradient id="paint0_linear_118_173" x1="222" y1="119" x2="290.97" y2="185.971" gradientUnits="userSpaceOnUse">
<stop offset="0.364198" stop-color="#FFD600"/>
<stop offset="1" stop-color="#007D05"/>
</linearGradient>
<linearGradient id="paint1_linear_118_173" x1="144" y1="188" x2="210.492" y2="121.491" gradientUnits="userSpaceOnUse">
<stop stop-color="#2400FF"/>
<stop offset="0.678292" stop-color="#FFD600"/>
</linearGradient>
<linearGradient id="paint2_linear_118_173" x1="145" y1="195.5" x2="287" y2="195" gradientUnits="userSpaceOnUse">
<stop stop-color="#2906FA"/>
<stop offset="1" stop-color="#33A716"/>
</linearGradient>
</defs>
</svg>   

 </div>
      <div
        style="
          position: absolute;
          top: 104px;
          left: 76px;
          font-size: 36px;
          display: inline-block;
          width: 227px;
          height: 102px;
        "
      >
        Solar Bank
      </div>
      <div
        style="
          position: absolute;
          top: 506px;
          left: 25px;
          border-radius: 20px;
          background-color: #2400ff;
          filter: blur(8px);
          width: 225px;
          height: 60px;
        "
      ></div>
      <div
        style="
          position: absolute;
          top: 595px;
          left: 132px;
          border-radius: 20px;
          background-color: #316b22;
          filter: blur(8px);
          width: 225px;
          height: 60px;
        "
      ></div>
      <div
        style="
          position: absolute;
          top: 525px;
          left: 43px;
          font-size: 16px;
          display: inline-block;
          width: 242px;
          height: 21px;
        "
      >
        XXX Geladene Handys
      </div>
      <div
        style="
          position: absolute;
          top: 614px;
          left: 156px;
          font-size: 16px;
          display: inline-block;
          width: 242px;
          height: 21px;
        "
      >
        XXX Benutzungen
      </div>
      <div
        style="
          position: absolute;
          top: 723px;
          left: 44px;
          font-size: 10px;
          display: inline-block;
          width: 318px;
          height: 90px;
        "
      >
        <p style="margin: 0">
         <a href="https://haschkeflorian.grafana.net/public-dashboards/c70943a3ec7342e78102fb02dc19b040">
        Historic data and further Analysation </a>
        </p>
      </div>
    </div>
  </body>
</html>"""

        free_memory_after = gc.mem_free()


        # response = 'HTTP/1.0 200 OK\r\n\r\n{}'.format(html_content)
        response = 'HTTP/1.0 200 OK\r\n\r\n{}'.format(html_content.replace('LOAD_POWER', str(round(loadPower, 1))).replace('MODULE_POWER', str(round(modulePower, 1))).replace('BATTERY_POWER', str(round(batteryPower, 1))).replace('OPACITY1', str(opacityValue1)).replace('OPACITY2', str(opacityValue2)).replace('OPACITY3', str(opacityValue3)))

        # print("Aktueller Analogwert:", sensor_value)
        # print("Gleitender Mittelwert der letzten 10 Werte:", (moving_average/65535)*UREF)
        # print("Gleitender Amperewert der letzten 10 Werte:", (((moving_average/65535)*UREF) - NULLPUNKT)/VpA)
        # print("Gesamtmittelwert aller bisherigen Werte:", (overall_average/65535)*UREF)
        # print("Gleitender Amperewert der letzten 10 Werte:", (((overall_average/65535)*UREF) - NULLPUNKT)/VpA)

        conn.send(response)
        conn.close()
    
        print("Verfügbarer Speicher vorher:", free_memory_before, "Bytes")
        print("Verfügbarer Speicher nachher:", free_memory_after, "Bytes")

start_server()
