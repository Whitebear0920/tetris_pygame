import socket
import threading

class date_process():

    def __init__(self):
        
        self.Max_Bytes = 65535

        #取得自己的ip位置
        self.name = socket.gethostname()    
        self.ip_address = socket.gethostbyname(self.name)

        #自己的位置資料 預設port為57414
        self.my_address = (self.ip_address, 57414)

        #對方的位置資料
        self.his_address = ("127.0.0.1", 57414)

        #socket 初始化
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        

        #接收端
        self.sock.bind("0.0.0.0", self.address[1])
        
        #傳送端
        self.sock


    def client(self):
        pass

    def server(self):
        pass

if __name__ == "__main__":
    
    x = date_process()

