import socket
from cryptography.fernet import Fernet
from colorama import init, Fore
import os

init(convert=True)

FORMAT = "utf-8"
HEADERSIZE = 64
key = "f4Uo9jGxFpMMXokg0Bap6zV-3RgGlz9CPEmtsY72D6c="
SECRET_KEY = Fernet(key)
ENDC = '\033[0m'
BOLD = '\033[1m'


class client(object):
    def __init__(self, HostIP, port):
        self.HOST_IP = HostIP
        self.PORT = port

    def start(self):
        """

            connect client socket to server socket and show the option menu to make client choice the MODE to send message

            Parameters:
            None

            Returns:
            None
        """
        self.clinet_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.clinet_socket.connect((self.HOST_IP, self.PORT))
        except ConnectionRefusedError:
            print(f"{Fore.RED + BOLD}The server is currently not working{ENDC}")
            exit()

        connection = True
        input_key = self.client_menu()
        while connection:

            if input_key == 1:
                message = input("Enter the message: ")
                self.send_data(message)
                self.receive_data()
                input_key = self.client_menu()
                self.clear()

            elif input_key == 2:

                message = input("Enter the message: ")
                self.send_encrypted_msg(message)
                encrypted_msg = self.receive_encrypted_msg()
                print(
                    f"encrypted message:{Fore.LIGHTRED_EX + BOLD} {encrypted_msg[0]}{ENDC}\n")
                print(
                    f"Decrypted message:{Fore.GREEN + BOLD} {encrypted_msg[1]}{ENDC}\n")

                input_key = self.client_menu()
                self.clear()

            elif input_key == 3:
                print("")
                self.send_data("Disconnecting....")
                self.receive_data()
                connection = False

            else:
                print("ENTER NUMBER BETWEEN 1-3 ...... ")
                input_key = self.client_menu()
                self.clear()

    def receive_encrypted_msg(self):
        """
            Receiving Encrypted message and decrypt the message 

            Parameters:
            None

            Returns:
            list: return a list contains on Encrypted message and decrypted message 

        """
        encrypted_msg = self.receive_data()
        decrypted_msg = SECRET_KEY.decrypt(
            bytes(encrypted_msg[2:len(encrypted_msg)], FORMAT)).decode()
        return (encrypted_msg, decrypted_msg)

    def send_encrypted_msg(self, msg: str):
        encrypted_msg = SECRET_KEY.encrypt(msg.encode(FORMAT))
        self.send_data(encrypted_msg)

    def client_menu(self):
        """
            Display option menu to client in order to chocie MODE to send message and send it to the server  

            Parameters:
            None

            Returns:
            int : retrun the choice of client  

        """
        IN = input(
            "Choice one of option:\n1-Open mode\n2-Secure mode\n3-Quit application\nEnter: ")
        if(IN == "1"):
            self.clinet_socket.send("Open_mode".encode(FORMAT))
        elif (IN == "2"):
            self.clinet_socket.send("Secure_mode".encode(FORMAT))
        elif IN == "3":
            self.clinet_socket.send("Quit_application".encode(FORMAT))
        else:
            return 0
        return int(IN)

    def clear(self):
        """
            it clear the Terminal

            Parameters:
            None

            Returns:
            None

        """
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def receive_data(self):
        """

            receiving message from server to the client and buffering the received data in proper way

            Parameters:
            None

            Returns:
            message (String) : return the received message form Server

        """
        full_message = ''
        new_msg = True
        while True:

            msg = self.clinet_socket.recv(64)
            if new_msg:
                msg_length = int(msg[:HEADERSIZE])
                new_msg = False
            full_message += msg.decode(FORMAT)

            if len(full_message) - HEADERSIZE == msg_length:
                print(
                    f"{Fore.GREEN + BOLD}Received message from server: {full_message[HEADERSIZE:]}{ENDC}\n")
                new_msg = True
                message = full_message[HEADERSIZE:]
                full_message = ''
                return message

    def send_data(self, message):
        """
            Sending message from Clirnt to the Server  

            Parameters:
            message (String)    :  the message that want to send to the client  
       ddd
            Returns:
            None     

        """
        message2 = str(message)
        message2 = f'{len(message2):<{HEADERSIZE}}' + message2
        print(
            f"{Fore.YELLOW + BOLD}Send to server: {message}{ENDC}\n")
        self.clinet_socket.send(message2.encode(FORMAT))


if __name__ == "__main__":
    Client = client("192.168.1.8", 4041)
    Client.start()
