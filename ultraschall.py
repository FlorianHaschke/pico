# Bibliotheken laden
from time import sleep, sleep_us, ticks_us
from machine import Pin

# Initialisierung GPIO-Ausgang für Trigger-Signal
trigger = Pin(2, Pin.OUT)

# Initialisierung GPIO-Eingang für Echo-Signal
echo = Pin(3, Pin.IN)

# Wiederholung (Endlos-Schleife)
while True:
    # Abstand messen
    trigger.low()
    sleep_us(2)
    trigger.high()
    sleep_us(5)
    trigger.low()
    # Zeiten messen
    while echo.value() == 0:
       signaloff = ticks_us()
    while echo.value() == 1:         
       signalon = ticks_us()
    # Vergangene Zeit ermitteln
    timepassed = signalon - signaloff # type: ignore
    # Abstand/Entfernung ermitteln
    # Entfernung über die Schallgeschwindigkeit (34320 cm/s bei 20 °C) berechnen
    # Durch 2 teilen, wegen Hin- und Rückweg
    abstand = timepassed * 0.03432 / 2
    print(abstand)

    # 2 Sekunde warten
    sleep(2)