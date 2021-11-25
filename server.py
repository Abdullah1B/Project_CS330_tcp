import socket
from cryptography.fernet import Fernet
from colorama import init , Fore
import threading
init(convert=True)
FORMAT = "utf-8"
HEADERSIZE = 64
key = "f4Uo9jGxFpMMXokg0Bap6zV-3RgGlz9CPEmtsY72D6c="
SECRET_KEY = Fernet(key)


ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[5m'

class server(object):
    def __init__(self,HostIP,port):
        self.HostIP = HostIP
        self.port = port
       
    
        
    def handle_client(self,client,address):
        input_key = client.recv(512)
        input_key = input_key.decode()
        
        connection = True
        while connection:
            if input_key == "Open_mode":
                msg  = self.receive_data(client= client, address= address)
                self.send_data(client= client, address= address, msg= msg.upper())

            elif input_key == "Secure_mode":
              
                encrypted_msg= self.receive_encrypted_msg(client= client, address= address)                
                print(f"encrypted message: {Fore.LIGHTRED_EX + BOLD}{encrypted_msg[0]}{ENDC}\n")
                print(f"Decrypted message: {Fore.GREEN + BOLD}{encrypted_msg[1]}{ENDC}\n")

                self.send_encrypted_msg(client= client, address= address, msg= str(encrypted_msg[1]).upper())


                
            elif input_key == "Quit_application":
                msg  = self.receive_data(client= client , address= address)
                self.send_data(client= client,address= address,msg= f"DISCONNECTED from {address[0]} ".upper())
                connection = False

            input_key = client.recv(512)
            input_key = input_key.decode()
        client.close()

    def receive_encrypted_msg(self,client,address):
        encrypted_msg = self.receive_data(client=client, address= address)
        decrypted_msg = SECRET_KEY.decrypt(
            bytes(encrypted_msg[1:len(encrypted_msg)], FORMAT)).decode()
        return (encrypted_msg, decrypted_msg)
    

    def send_encrypted_msg(self,client,address, msg:str):
        encrypted_msg = SECRET_KEY.encrypt(msg.encode(FORMAT))
        self.send_data(client= client, address= address , msg= encrypted_msg)
    
        
    def Start(self):
        self.server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_Socket.bind((self.HostIP, self.port))
        self.server_Socket.listen()
        
        print(f"{UNDERLINE + BOLD}[LISTENING] Server Start to listening\n{ENDC}")
        while True:
            client , address = self.server_Socket.accept()
            print(f"{BOLD + Fore.GREEN}[CONNECTION] connection establish {address[0]}:{address[1]}{ENDC}\n")
            thread = threading.Thread(target= self.handle_client,args= (client,address))
            thread.start()
            
    
    def send_data(self,client,address,msg):
        message = str(msg)
        message = f'{len(message):<{HEADERSIZE}}' + message
        print(f"{Fore.YELLOW + BOLD}[SENDING]send a message to {address[0]} : {msg}{ENDC}\n")
        client.send(message.encode(FORMAT))


               
                
    def receive_data(self,client,address):
        full_message = ''
        new_msg = True
        while True:
            
            msg = client.recv(64)
            if new_msg:
                msg_length = int(msg[:HEADERSIZE])
                new_msg = False
            full_message += msg.decode(FORMAT)
            
            if len(full_message) - HEADERSIZE == msg_length:
                print(f"{Fore.GREEN + BOLD}[RECEIVED] received message from {address[0]}:{full_message[HEADERSIZE:]}{ENDC}\n")
                new_msg = True
                message = full_message[HEADERSIZE:]
                full_message = ''
                return message
                
        

Server = server("",4041)
e = 3
Server.Start()