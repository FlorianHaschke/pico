import machine
import time
import network
import socket
import time
import math
import gc


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
    free_memory_before = gc.mem_free()

    addr = wlan.ifconfig()[0]
    port = 99

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
        font-family: 'Julius Sans One';
      "
    >
        <div
          style="
          position: absolute;
          top: 200px;
          left: -45;
        ">
<svg width="439" height="287" viewBox="0 0 439 287" fill="none" xmlns="http://www.w3.org/2000/svg">
<g id="Frame 5">
<path id="Ellipse 2" d="M135.5 193C135.5 217.073 116.648 236.5 93.5 236.5C70.3516 236.5 51.5 217.073 51.5 193C51.5 168.927 70.3516 149.5 93.5 149.5C116.648 149.5 135.5 168.927 135.5 193Z" stroke="#2906FA" stroke-width="3"/>
<path id="Ellipse 6" d="M257.5 68C257.5 92.0563 238.441 111.5 215 111.5C191.559 111.5 172.5 92.0563 172.5 68C172.5 43.9437 191.559 24.5 215 24.5C238.441 24.5 257.5 43.9437 257.5 68Z" stroke="#FFD600" stroke-width="3"/>
<path id="Ellipse 5" d="M382.5 189.5C382.5 213.832 363.217 233.5 339.5 233.5C315.783 233.5 296.5 213.832 296.5 189.5C296.5 165.168 315.783 145.5 339.5 145.5C363.217 145.5 382.5 165.168 382.5 189.5Z" stroke="#33A716" stroke-width="3"/>
<path id="Rectangle 1" d="M222 119V158C222 172.142 222 179.213 226.393 183.607C230.787 188 237.858 188 252 188H289" stroke="url(#paint0_linear_118_173)" stroke-width="3"/>
<path id="Rectangle 2" d="M144 188H178C192.142 188 199.213 188 203.607 183.607C208 179.213 208 172.142 208 158V119" stroke="url(#paint1_linear_118_173)" stroke-width="3"/>
<path id="XX W" d="M69.6136 185.455L73.3636 191.506H73.4773L77.2273 185.455H79.3011L74.7273 192.727L79.3011 200H77.2273L73.4773 194.062H73.3636L69.6136 200H67.5398L72.2273 192.727L67.5398 185.455H69.6136ZM82.4457 185.455L86.1957 191.506H86.3093L90.0593 185.455H92.1332L87.5593 192.727L92.1332 200H90.0593L86.3093 194.062H86.1957L82.4457 200H80.3718L85.0593 192.727L80.3718 185.455H82.4457ZM102.692 200L98.7152 185.455H100.505L103.545 197.301H103.687L106.783 185.455H108.772L111.869 197.301H112.011L115.05 185.455H116.84L112.863 200H111.045L107.835 188.409H107.721L104.511 200H102.692Z" fill="#2906FA"/>
<path id="XX W_2" d="M190.614 60.4545L194.364 66.5057H194.477L198.227 60.4545H200.301L195.727 67.7273L200.301 75H198.227L194.477 69.0625H194.364L190.614 75H188.54L193.227 67.7273L188.54 60.4545H190.614ZM203.446 60.4545L207.196 66.5057H207.309L211.059 60.4545H213.133L208.559 67.7273L213.133 75H211.059L207.309 69.0625H207.196L203.446 75H201.372L206.059 67.7273L201.372 60.4545H203.446ZM223.692 75L219.715 60.4545H221.505L224.545 72.3011H224.687L227.783 60.4545H229.772L232.869 72.3011H233.011L236.05 60.4545H237.84L233.863 75H232.045L228.835 63.4091H228.721L225.511 75H223.692Z" fill="#FFD600"/>
<path id="XX W_3" d="M315.614 180.455L319.364 186.506H319.477L323.227 180.455H325.301L320.727 187.727L325.301 195H323.227L319.477 189.062H319.364L315.614 195H313.54L318.227 187.727L313.54 180.455H315.614ZM328.446 180.455L332.196 186.506H332.309L336.059 180.455H338.133L333.559 187.727L338.133 195H336.059L332.309 189.062H332.196L328.446 195H326.372L331.059 187.727L326.372 180.455H328.446ZM348.692 195L344.715 180.455H346.505L349.545 192.301H349.687L352.783 180.455H354.772L357.869 192.301H358.011L361.05 180.455H362.84L358.863 195H357.045L353.835 183.409H353.721L350.511 195H348.692Z" fill="#138405"/>
<line id="Line 6" x1="144" y1="195.5" x2="289" y2="195.5" stroke="url(#paint2_linear_118_173)" stroke-width="3"/>
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
        <p style="margin: 0">More Details:</p>
        <p style="margin: 0">
          https://haschkeflorian.grafana.net/public-dashboards/c70943a3ec7342e78102fb02dc19b040
        </p>
      </div>
    </div>
  </body>
</html>"""

        free_memory_after = gc.mem_free()


        response = 'HTTP/1.0 200 OK\r\n\r\n{}'.format(html_content)
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
