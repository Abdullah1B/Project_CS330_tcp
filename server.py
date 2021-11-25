import socket
from cryptography.fernet import Fernet
from colorama import init 
init(convert=True)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    BGRED = '\033[41m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[5m'

class server(object):
    def __init__(self,HostIP,port):
        self.HostIP = HostIP
        self.port = port
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        self.address = ""
        self.key = None
        
    def handle_client(self,client):
        input_key = client.recv(512)
        input_key = input_key.decode()
        
        connection = True
        while connection:
            if input_key == "Open_mode":
                msg  = self.receive_data(client)
                self.send_data(client,msg.upper())

            elif input_key == "Secure_mode":
                Secrt_key = client.recv(2024)
                Secrt_key = Secrt_key.decode()
                self.key = Fernet(Secrt_key)# shared key to encrypt and decrypt message

                msg  = self.receive_data(client)
                msg2 = self.Decrypt(self.convert_to_bytes(msg))
                print(f"encrypted message: {bcolors.OKGREEN +bcolors.BOLD}{msg}{bcolors.ENDC}")
                print(f"Decrypted message: {bcolors.OKGREEN +bcolors.BOLD}{msg2}{bcolors.ENDC}")

                encrypted_msg = self.encrypt(msg2.upper())
                self.send_data(client,encrypted_msg)


                
            elif input_key == "Quit_application":
                msg  = self.receive_data(client)
                self.send_data(client, msg.upper())
                connection = False

            input_key = client.recv(512)
            input_key = input_key.decode()
        client.close()

    def encrypt(self,msg):
        return self.key.encrypt(msg.encode(self.FORMAT))
           
    def convert_to_bytes(self,msg):
        return bytes(msg[1:len(msg)],self.FORMAT)    

    def Decrypt(self,msg):
        return self.key.decrypt(msg).decode()
        
    def start(self):
        self.server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_Socket.bind((self.HostIP, self.port))
        self.server_Socket.listen()
        
        print(f"{bcolors.OKGREEN+ bcolors.BOLD}[LISTENING] Server Start to listening\n{bcolors.ENDC}")
        while True:
            client , address = self.server_Socket.accept()
            print(f"{bcolors.BOLD}{bcolors.OKGREEN}[CONNECTION] connection establish {address[0]}:{address[1]}{bcolors.ENDC}\n")
            self.address = address[0]
            self.handle_client(client)
            
    
    def send_data(self,client,data):
        message = str(data)
        message = f'{len(message):<{self.HEADER}}' + message
        print(f"{bcolors.YELLOW + bcolors.BOLD}[SENDING]send a message to {self.address} : {data}\n")
        client.send(message.encode(self.FORMAT))


               
                
    def receive_data(self,client):
        full_message = ''
        new_msg = True
        while True:
            msg = client.recv(16)
            if new_msg:
                msg_length = int(msg[:self.HEADER])
                new_msg = False
            full_message += msg.decode(self.FORMAT)
            
            if len(full_message) - self.HEADER == msg_length:
                print(f"{bcolors.OKGREEN + bcolors.BOLD}[RECEIVED] received message from {self.address}:{full_message[self.HEADER:]}{bcolors.ENDC}\n")
                new_msg = True
                message = full_message[self.HEADER:]
                full_message = ''
                return message
                
        

Server = server("",4041)
Server.start()