import network
import usocket as socket

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def start_server():
    addr = wlan.ifconfig()[0]
    port = 80

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((addr, port))
    s.listen(5)

    print('Web server started on {}:{}'.format(addr, port))

    while True:
        conn, addr = s.accept()
        print('Connection from {}'.format(addr))
        request = conn.recv(1024)
        print('Request: {}'.format(request))

        response = 'HTTP/1.0 200 OK\r\n\r\nHallo'

        conn.send(response)
        conn.close()

start_server()