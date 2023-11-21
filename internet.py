import socket
import threading

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client.connect(("127.0.0.1",57414))

