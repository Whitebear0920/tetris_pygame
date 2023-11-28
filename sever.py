import socket
import threading
import json

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
start = False
players = []
server_iP = "0.0.0.0"
server_port = 57414
server_addr = (server_iP,server_port) 
s.bind(server_addr)
print('server start at: %s:%s' % server_addr)
print('wait for connection...')

while True:
    try:
        data, address = s.recvfrom(65565)
    except ConnectionResetError:
        print("someone leave")
        continue
    data = json.loads(data.decode())
    if data["type"] == "connecting":
        players.append(address)
        data = {"type":"connected"}
        data = json.dumps(data).encode()
        s.sendto(data,address)
    elif len(players) == 2:
        data = json.dumps(data).encode()
        for i in players:
            if i != address:
                s.sendto(data,i)