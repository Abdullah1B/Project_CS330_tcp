import socket
from cryptography.fernet import Fernet
from colorama import init
import os
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
    UNDERLINE = '\033[4m'

class client(object):
    def __init__(self, HostIP, port):
        self.HOST_IP = HostIP
        self.PORT = port
        self.HEADER = 64
        self.FORMAT = 'utf-8'
        self.secret_key = Fernet.generate_key()
        self.key = Fernet(self.secret_key)
        

    def start(self):
        self.clinet_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clinet_socket.connect((self.HOST_IP, self.PORT))
        connection = True
        input_key = self.client_muen()
        while connection:
            
            if input_key == 1:
                message = input("Enter the message: ")
                self.send_data(message)
                self.receive_data()
                input_key = self.client_muen()
                self.clear()

            elif input_key == 2:

                self.clinet_socket.send(self.secret_key)
                message = input("Enter the message: ")
                encrypted_msg = self.encrypt(message)
                
                self.send_data(encrypted_msg)
                msg  = self.receive_data()
                msg2 = self.Decrypt(self.convert_to_bytes(msg))
                print()
                print(f"encrypted message:{bcolors.BOLD + bcolors.OKGREEN} {msg}{bcolors.ENDC}")
                print(f"Decrypted message:{bcolors.BOLD + bcolors.OKGREEN} {msg2}{bcolors.ENDC}")

                
                input_key = self.client_muen()
                self.clear()

            elif input_key == 3:
                print("")
                self.send_data("Disconnecting ....")
                self.receive_data()
                connection = False
                
            else:
                input_key = self.client_muen()
                
                
    def convert_to_bytes(self,msg):
        return bytes(msg[1:len(msg)],self.FORMAT)    

    def Decrypt(self,msg):
        return self.key.decrypt(msg).decode()  

    def encrypt(self,msg):
        return self.key.encrypt(msg.encode(self.FORMAT))
        
    def client_muen(self):
        IN = input("Choice one of option:\n1-Open mode\n2-Secure mode\n3-Quit application\nEnter: ")
        if(IN == "1" ):
            self.clinet_socket.send("Open_mode".encode(self.FORMAT))
        elif (IN == "2" ):
            self.clinet_socket.send("Secure_mode".encode(self.FORMAT))
        elif IN == "3":
            self.clinet_socket.send("Quit_application".encode(self.FORMAT))
        else:
            return 0
        return int(IN)


    def clear(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')


    def receive_data(self):
        full_message = ''
        new_msg = True
        while True:
            msg = self.clinet_socket.recv(16)
            if new_msg:
                msg_length = int(msg[:self.HEADER])
                new_msg = False
            full_message += msg.decode(self.FORMAT)

            if len(full_message) - self.HEADER == msg_length:
                print(
                    f"{bcolors.OKGREEN + bcolors.BOLD}Received message from server: {full_message[self.HEADER:]}{bcolors.ENDC}")
                new_msg = True
                message = full_message[self.HEADER:]
                full_message = ''
                return message

    def send_data(self, message2):
        message = str(message2)
        message = f'{len(message):<{self.HEADER}}' + message
        print(f"{bcolors.YELLOW + bcolors.BOLD}Send to server: {message2}{bcolors.ENDC}")
        self.clinet_socket.send(message.encode(self.FORMAT))

if __name__ == "__main__":
    
    Client = client("put the ip of the server", 4041)
    Client.start()


