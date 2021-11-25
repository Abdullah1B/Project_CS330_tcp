import socket

class server(object):
    def __init__(self,HostIP,port):
        self.HostIP = HostIP
        self.port = port
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        
    def handle_client(self,client,address):
        input_key = client.recv(512)
        input_key = input_key.decode()
        print(input_key)
        connection = True
        while connection:
            if input_key == "OP":
                self.send_data(client, "hello you are in open mode")
                msg  = self.receive_data(client,self.HEADER)
            elif input_key == "SM":
                self.send_data(client, "hello you are in seucre mode ")
                msg  = self.receive_data(client,self.HEADER)
            elif input_key == "CO":
                self.send_data(client, "closiing")
                msg  = self.receive_data(client,self.HEADER)
                connection = False
            input_key = client.recv(512)
            input_key = input_key.decode()
        client.close()
           
                
                



        
    
    def start(self):
        self.server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_Socket.bind((self.HostIP, self.port))
        self.server_Socket.listen()
        print(f"[LISTENING] server is listening on {self.HostIP}")
        while True:
            client , address = self.server_Socket.accept()
            print(f"[CONNECTION] connection establish {address[0]}:{address[1]}")
            
            self.handle_client(client, address)
            
    
    def send_data(self,client,data):
        message = data
        message = f'{len(message):<{self.HEADER}}' + message
        client.send(message.encode(self.FORMAT))
        
    def receive_data(self,client,value):
        full_message = ''
        new_msg = True
        T = True
        while T:
            msg = client.recv(16)
            if new_msg:
                msg_length = int(msg[:self.HEADER])
                new_msg = False
            full_message += msg.decode(self.FORMAT)
            
            if len(full_message) - self.HEADER == msg_length:
                print(f"received message from client {full_message[self.HEADER:]}")
                new_msg = True
                full_message = ''
                T = False
        

Server = server("127.0.0.1",4040)
Server.start()