import threading 
import json 
import socket
import os
import time

class date_process():

    def __init__(self):
        
        self.Max_Bytes = 65535
        self.server_addr = ("127.0.0.1",57414)
        #取得自己的ip位置
        self.name = socket.gethostname()    #取代nickname


        self.ip_address = socket.gethostbyname(self.name)

        #自己的位置資料 預設port為57414
        self.my_address = (self.ip_address, 57414)

        #對方的位置資料
        self.his_address = ("127.0.0.1", 57414)

        #socket 初始化
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        self.msgdict = {
            "type": 1,
            "nickname": self.name
        }
        
        # 轉成JSON字串，再轉成bytes
        self.data = json.dumps(self.msgdict).encode('utf-8')
        # 將Enter Request送到Server
        self.sock.sendto(self.data, self.server_addr)

        # 等待並接收Server傳回來的訊息，若為Enter Response則繼續下一步，否則繼續等待
        self.is_entered = False
        while not is_entered:
            try:
                self.data, address = self.sock.recvfrom(self.Max_Bytes)
                msgdict = json.loads(data.decode('utf-8'))
                if msgdict['type'] == 2:
                    is_entered = True
                    print('成功進入伺服器!!!')
            except:
                print("伺服器連線失敗,5秒後重試")
                for i in range(5):
                    time.sleep(1)
                    print(".", end="",flush = True)
                print()
                data = json.dumps(msgdict).encode("utf-8")
                self.sock.sendto(data, self.server_addr)

    def connect(self):
        return self.is_entered

    def send_message(self):
        print("開始執行send message")
        while(True):
            # 取得使用者輸入的聊天訊息
            self.msgtext = input('請輸入聊天訊息：')
            if self.msgtext[:2] == "%%" and self.msgtext[-2:] == "%%":
                if self.msgtext[2:7] == "Leave":
                    msgdict = {
                        "type" : 6,
                        "nickname" : self.name
                    }
            else:    
                # 建立Message Request訊息的dict物件
                msgdict = {
                    "type": 3,
                    "nickname": self.name,
                    "message": self.msgtext
                }
    # 轉成JSON字串，再轉成bytes
            msgdata = json.dumps(msgdict).encode('utf-8')
            print(msgdata)
            # 將Enter Request送到Server
            self.sock.sendto(msgdata, self.server_addr)
            if (msgdict["type"] == 6):
                print("leave")
                os._exit(0)

    def recv_message(self):
        print("開始執行recv_message")
        while(True):
            # 接收來自Server傳來的訊息
            data, address = self.sock.recvfrom(self.Max_Bytes)
            self.msgdict = json.loads(data.decode('utf-8'))
            # 依照type欄位的值做對應的動作
            ## Message Response(4)：這是之前Message Request的回應訊息
            if self.msgdict['type'] == 4:
                # 不需做任何處理
                print('Get Message Response from server.') # 除錯用
                pass 
            ## Message Transfer(5)：這是其他Client所發布的訊息
            if self.msgdict['type'] == 5:
                print('Get Message Transfer from server.') # 除錯用
                # 以「nickname: message content」的格式印出
                print(self.msgdict['nickname'] + ': ' + self.msgdict['message'])




        


