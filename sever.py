import socket
import threading

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_iP = "0.0.0.0"
server_port = 57414
server_addr = (server_iP,server_port) 
s.bind(server_addr)
print('server start at: %s:%s' % server_addr)
print('wait for connection...')

while True:

