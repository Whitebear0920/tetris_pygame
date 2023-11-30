import threading 
import json 
import socket
import os
import time
from game import Game
"""
data = {
            "type" : ,
            "value" :
        }

"""

class date_process():

    def __init__(self):
        #self.game = Game()
        self.Max_Bytes = 65565
        self.is_entered = False
        #server
        self.Server_IP="127.0.0.1"
        self.Server_port = 57414
        self.Server_addr = ((self.Server_IP,self.Server_port))
        #socket 初始化
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
    def connect(self):
        self.msgdict = {
            "type": "connecting"
        }
        self.data = json.dumps(self.msgdict).encode('utf-8')
        # 將Enter Request送到Server
        self.sock.sendto(self.data, self.Server_addr)

        # 等待並接收Server傳回來的訊息，若為Enter Response則繼續下一步，否則繼續等待
        while not self.is_entered:
            try:
                self.data, self.address = self.sock.recvfrom(self.Max_Bytes)
                self.msgdict = json.loads(self.data.decode('utf-8'))
                if self.msgdict['type'] == "connected":
                    self.is_entered = True
                    print('connect successfully!!!')
            except:
                print("Server connection failed, try again in 5 seconds")
                for i in range(5):
                    time.sleep(1)
                    print(".", end="",flush = True)
                print()
                data = json.dumps(self.msgdict).encode("utf-8")
                self.sock.sendto(data, self.Server_addr)

    def send_message(self,type,value):
        self.Senddata ={
            "type" : type,
            "value" : value
        }
        self.Senddata = json.dumps(self.Senddata).encode()
        self.sock.sendto(self.Senddata,self.Server_addr)

    def recv_message(self):
        print("recv_message Start")
        while(True):
            # 接收來自Server傳來的訊息
            self.Recdata, self.address = self.sock.recvfrom(self.Max_Bytes)
            self.Recdata = json.loads(self.Recdata.decode('utf-8'))
            if self.Recdata["type"] == "GameOver": #GameOver
                if self.Recdata["value"] == True:
                    #self.game.gameover = True
                    print("win")
            elif self.Recdata["type"] == "Attack": #Attack Line
                print("got attack!")
                #self.game.check_attack_row(self.Recdata["value"])


            
            




        


