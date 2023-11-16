import socket
import threading

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sever_iP="0.0.0.0"
sever_port=57414
s.bind((sever_iP,sever_port))
s.listen()
