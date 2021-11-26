import socket
from cryptography.fernet import Fernet
from colorama import init , Fore
import threading
init(convert=True)

FORMAT = "utf-8"
HEADERSIZE = 64
key = "f4Uo9jGxFpMMXokg0Bap6zV-3RgGlz9CPEmtsY72D6c=" # shread key to encrypt and decrypt
SECRET_KEY = Fernet(key)
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[5m'

class server(object):
    def __init__(self,HostIP,port):
        self.HostIP = HostIP
        self.port = port
       
    
    
    def handle_client(self,client,address):
        """
            handle connection in which client exchange message with server 
                    

            Parameters:
            client (Socket) :  the client socket which used to send and receive data
            address (list)  :  the address which have the IP of client and port nubmer

            Returns:
             None

        """
        
        Mode = client.recv(512) # receive the optin mode from client 
        Mode = Mode.decode() # convert from byte to string 
        
        connection = True
        while connection:
            if Mode == "Open_mode": # receive message and send it back to  client in open mode
                msg  = self.receive_data(client= client, address= address)
                self.send_data(client= client, address= address, msg= msg.upper())

            elif Mode == "Secure_mode": # receive message and send it back to  client in Secure mode
              
                encrypted_msg= self.receive_encrypted_msg(client= client, address= address) # receive a encrypted message and decrypted        
                # print a encrypted message and decrypted message       
                print(f"encrypted message: {Fore.LIGHTRED_EX + BOLD}{encrypted_msg[0]}{ENDC}\n") 
                print(f"Decrypted message: {Fore.GREEN + BOLD}{encrypted_msg[1]}{ENDC}\n")

                self.send_encrypted_msg(client= client, address= address, msg= str(encrypted_msg[1]).upper()) # send a encrypted message to client 


                
            elif Mode == "Quit_application":
                msg  = self.receive_data(client= client , address= address)
                self.send_data(client= client,address= address,msg= f"DISCONNECTED from {address[0]} ".upper())
                connection = False

            Mode = client.recv(512) # receive the optin mode from client 
            Mode = Mode.decode()
        client.close() # close the connetion between client and server 

    def receive_encrypted_msg(self,client,address):
        """
           Receiving Encrypted message and decrypt the message 

            Parameters:
            client (Socket) :  the client socket which used to send and receive data
            address (list)  :  the address which have the IP of client and port nubmer

            Returns:
            list: return a list contains on Encrypted message and decrypted message 

        """
        encrypted_msg = self.receive_data(client=client, address= address) # receive the message
        decrypted_msg = SECRET_KEY.decrypt(
            bytes(encrypted_msg[1:len(encrypted_msg)], FORMAT)).decode() # decrypt the message the convert it from byte to string 
        return (encrypted_msg, decrypted_msg) 
    

    def send_encrypted_msg(self,client,address, msg:str):
        """
           Sending Encrypted message to the client  

            Parameters:
            client (Socket) :  the client socket which used to send and receive data
            address (list)  :  the address which have the IP of client and port nubmer
            msg (String)    :  the message that want to send to the client  

            Returns:
            None

        """
        encrypted_msg = SECRET_KEY.encrypt(msg.encode(FORMAT)) # encrypt the message 
        self.send_data(client= client, address= address , msg= encrypted_msg)
    
        
    def Start(self):
        """
            setup the socket and bind it to IP address and Port Number and start to listening to the client 
            and setup the threding to hold multiple connection at the same time

            Parameters:
            None

            Returns:
            None
        """
        self.server_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)# create socket and defind the family and type of socket 
        self.server_Socket.bind((self.HostIP, self.port)) # socket with ip address and port number 
        self.server_Socket.listen() # start to listen to incoming connections
        
        print(f"{UNDERLINE + BOLD}[LISTENING] Server Start to listening\n{ENDC}")
        while True:
            client , address = self.server_Socket.accept() # make connection establish
            print(f"{BOLD + Fore.GREEN}[CONNECTION] connection establish {address[0]}:{address[1]}{ENDC}\n")

            thread = threading.Thread(target= self.handle_client,args= (client,address)) # create a thread to handle a multi-connection
            thread.start()
            
    
    def send_data(self,client,address,msg):
        """
           Sending message from server to the client  

            Parameters:
            client (Socket) :  the client socket which used to send and receive data
            address (list)  :  the address which have the IP of client and port nubmer
            msg (String)    :  the message that want to send to the client  

            Returns:
            None

        """
        message = str(msg)
        message = f'{len(message):<{HEADERSIZE}}' + message # add the HEADERSIZE to the message
        print(f"{Fore.YELLOW + BOLD}[SENDING]send a message to {address[0]} : {msg}{ENDC}\n")
        client.send(message.encode(FORMAT))# send to client 


               
                
    def receive_data(self,client,address):
        """
          receiving message from Client to the server and buffer the received data in proper way

            Parameters:
            client (Socket) :  the client socket which used to send and receive data
            address (list)  :  the address which have the IP of client and port nubmer

            Returns:
            message (String) : return the received message form client
                
        """
        full_message = ''
        new_msg = True
        while True:
            
            msg = client.recv(64) # receive message up to 64 bytes
            if new_msg: # if it a new message then 
                msg_length = int(msg[:HEADERSIZE]) # message lenght up to HEADERSIZE 
                new_msg = False
            full_message += msg.decode(FORMAT) # convet the received part of the message from byte to string
            
            if len(full_message) - HEADERSIZE == msg_length: # if the length of Full message - HEADERSIZE == message length then we received the whole message 
                print(f"{Fore.GREEN + BOLD}[RECEIVED] received message from {address[0]}:{full_message[HEADERSIZE:]}{ENDC}\n")
                new_msg = True
                message = full_message[HEADERSIZE:]
                full_message = ''
                return message
                

Server = server("",4041)
Server.Start()
