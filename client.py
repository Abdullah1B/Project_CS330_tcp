import socket
import os


class client(object):
    def __init__(self, HostIP, port):
        self.HOST_IP = HostIP
        self.PORT = port
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        self. change_mode = True
        self.choice = ""
        self.count_2 = 0

    def start(self):
        self.clinet_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clinet_socket.connect((self.HOST_IP, self.PORT))
        connection = True
        input = self.client_muen()
        while connection:
            
            if input == 1:
                print("hello 111111" )
                self.send_data("hello from client from 1")
                self.receive_data()
                
                input = self.client_muen()
            elif input == 2:
                self.count_2 = 1
                print("hello 22222" )
                self.send_data("hello from client from 2")
                self.receive_data()
                input = self.client_muen()
            elif input == 3:
                print("hello 33333333" )
                self.send_data("hello from client from 3")
                self.receive_data()
                connection = False
                #self.clinet_socket.close()
                
                
   
    def client_muen(self):
     
        IN = input("Enter \n1- open mode\n2- secure mode\n3-quit app\nEnter: ")
        if(IN == "1" ):
            self.clinet_socket.send("OP".encode(self.FORMAT))
        elif (IN == "2" ):
            self.clinet_socket.send("SM".encode(self.FORMAT))
        elif IN == "3":
            self.clinet_socket.send("CO".encode(self.FORMAT))
        return int(IN)
           
    def clear(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')


    def receive_data(self):
        full_message = ''
        new_msg = True
        T = True
        while T:
            msg = self.clinet_socket.recv(16)
            if new_msg:
                msg_length = int(msg[:self.HEADER])
                new_msg = False
            full_message += msg.decode(self.FORMAT)

            if len(full_message) - self.HEADER == msg_length:
                print(
                    f"received message from server {full_message[self.HEADER:]}")
                new_msg = True
                T = False

    def send_data(self, message2):
        message = message2
        message = f'{len(message):<{self.HEADER}}' + message
        self.clinet_socket.send(message.encode(self.FORMAT))

if __name__ == "__main__":
    
    Client = client("127.0.0.1", 4040)
    Client.start()


