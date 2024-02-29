import threading
import socket
import time
import encry_decrypt
import json

class Auction_client():

    def __init__(self):
        self.target_ip = "localhost"
        self.target_port = 8888
        self.my_data = {}
        self.userKey = self.getting_key()
        self.active_list = {}
        self.activate_F = True
        self.room_data = {}
        self.room_id = 0
        self.flag = False
        self.auction_lobby = {}
        self.client_menu()
    
    def countdown(self):
        while self.activate_F:
            for i in list(self.active_list.keys()):
                if self.active_list[i] > 0:
                    self.active_list[i] -= 1
                else:
                    self.active_list.pop(i)
                    self.auction_lobby.pop(str(i))
            if self.flag:
                if self.room_data[str(self.room_id)]["remaining time"]:
                    if self.room_data[str(self.room_id)]["remaining time"] > 0:
                        self.room_data[str(self.room_id)]["remaining time"] -= 1
                    else:
                        self.flag = False
            time.sleep(1)
    
    def show_countdown(self, id):
        while self.flag:
            print("[" + str(self.active_list[id]) + "]", end="\r")
            time.sleep(1)
            
    def receive_data_background(self, client):
        while self.activate_F:
            try:
                if not self.receive_data_event.is_set():
                    recv_info = client.recv(4096)
                    if not recv_info:
                        break  # Connection closed by the server
                    recv_encrypted = recv_info.decode("utf-8")
                    decry = encry_decrypt.A3Decryption()
                    recv_decrypted = decry.startDecryption(recv_encrypted)
                    recv_decrypted = json.loads(recv_decrypted)
                    print("$:", recv_decrypted)
                    if "update" in recv_decrypted:
                        id = str(recv_decrypted["update"]["id"])
                        if int(id) == self.room_id:
                            highest_bid = int(recv_decrypted["update"]["highest bid"])
                            u_name = str(recv_decrypted["update"]["username"])
                            self.room_data[id].update({"highest bid": highest_bid, "username" : u_name})
                            print("Update Highest offer!" + u_name+ str(highest_bid))
                    elif "finish" in recv_decrypted:
                        id = str(recv_decrypted["finish"]["id"])
                        if int(id) == self.room_id:
                            print("Auction over! Winner is "+ self.room_data[id]["username"]+" with "+self.room_data[id]["highest bid"])
                            self.flag = False
                    elif "err" in recv_decrypted:
                        print(recv_decrypted["err"])
                        self.enter_auction()
                time.sleep(0.1)
            except Exception as e:
                print(f"Error receiving data: {e}")
                break

    def getting_key(self):
        userKey: str = input("Enter your encryption key for the whole process:")
        return userKey

    def client_runner(self):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.target_ip, self.target_port))
            return client  # to send and receive data
        except ConnectionAbortedError as e:
            print(f"Connection aborted: {e}")
        except Exception as e:
            print(f"An error occurred while connecting: {e}")

    def client_menu(self):
        print("This is client menu:")
        user_data = input("Press 1 to login:\nPress 2 to register:")
        if user_data == '1':
            self.login()
        elif user_data == '2':
            self.register()
            
    def sending_encrypted(self, client, raw_data: str):
        encry = encry_decrypt.A3Encryption()
        decry = encry_decrypt.A3Decryption()
        encrypted_data = encry.start_encryption(raw_data, self.userKey)
        client.send(bytes(encrypted_data, "utf-8"))
        recv_info = client.recv(4096)
        recv_encrypted = recv_info.decode("utf-8")
        print("Received Encrypted Data : ", recv_encrypted)

        recv_decrypted = decry.startDecryption(recv_encrypted)
        print("$:", recv_decrypted)
    
    def register(self):
        try:
            client = self.client_runner()
            r_email = input("Enter email for registration :")
            flag = self.email_checking(r_email) 

            if flag == 1:
                while True:
                    pass1 = input("Enter your password to register:")
                    pass2 = input("Enter your password Again  to register:")
                    if pass1 == pass2:
                        u_name = input("Enter your username:")
                        phone = int(input("Enter your phone number:"))
                        data_form = "register" + " " + r_email + " " + pass1 + " " + u_name + " " + str(phone)
                        print(data_form)
                        encry = encry_decrypt.A3Encryption()
                        decry = encry_decrypt.A3Decryption()
                        encrypted_data = encry.start_encryption(data_form, self.userKey)
                        client.send(bytes(encrypted_data, "utf-8"))
                        recv_info = client.recv(4096)
                        recv_encrypted = recv_info.decode("utf-8")
                        recv_decrypted = decry.startDecryption(recv_encrypted)
                        recv_decrypted = json.loads(recv_decrypted)
                        print(recv_decrypted)
                        client.close()
                        break
                    else:
                        print("Password not match!")
            else:
                print("Email Form Invalid\nTry Again! ")
                self.register(client)
        except Exception as e:
            print(e)

    def email_checking(self, r_email):
        name_counter = 0
        for i in range(len(r_email)):
            if r_email[i] == '@':
                break
            name_counter += 1

        print("Name counter: ", name_counter)

        email_name = r_email[0:name_counter]
        email_form = r_email[name_counter:]

        # print(email_name)
        print(email_form)

        # checking for name
        name_flag = 0
        email_flag = 0
        for i in range(len(email_name)):
            aChar = email_name[i]
            if (ord(aChar) > 31 and ord(aChar) < 48) or (ord(aChar) > 57 and ord(aChar) < 65) or (
                    ord(aChar) > 90 and ord(aChar) < 97) or (ord(aChar) > 122 and ord(aChar) < 128):
                name_flag = -1
                break

        domain_form = ["@facebook.com", "@ncc.com", "@mail.ru", "@yahoo.com", "@outlook.com", "@apple.com", "@zoho.com",
                       "@gmail.com"]

        for i in range(len(domain_form)):

            if domain_form[i] == email_form:
                email_flag = 1
                break

        if name_flag == -1 or email_flag == 0:
            return -1
        else:
            return 1

    def login(self):
        try:
            client = self.client_runner()
            while True:
                l_email = input("Enter your email to login:")
                flag = self.email_checking(l_email)
                if flag == 1:
                    l_pass = input("Enter your password to login:")
                    data_form = "login" + " " + l_email + " " + l_pass
                    encry = encry_decrypt.A3Encryption()
                    decry = encry_decrypt.A3Decryption()
                    encrypted_data = encry.start_encryption(data_form, self.userKey)
                    client.send(bytes(encrypted_data, "utf-8"))
                    recv_info = client.recv(4096)
                    recv_encrypted = recv_info.decode("utf-8")
                    print("Received Encrypted Data : ", recv_encrypted)
                    recv_decrypted = decry.startDecryption(recv_encrypted)
                    recv_decrypted = json.loads(recv_decrypted)
                    if(any("err" in x for x in recv_decrypted)):
                        print(recv_decrypted["err"])
                    else:
                        client.close()
                        self.my_data.update(recv_decrypted)
                        self.auction_section()
                        break
                else:
                    print("Email Form Invalid\nTry Again! ")
        except Exception as e:
            print(e)
    
    def auction_section(self):
        try:
            option = input("Press 1 to create auction room:\nPress 2 to enter auction room:\nPress 3 to go back:")
            if option == '1':
                self.create_auction()
            elif option == '2':
                self.enter_auction()
            elif option == '3':
                self.client_menu()
        except Exception as e:
            print(e)
            self.auction_section()

    def create_auction(self):
        try:
            client = self.client_runner()
            au_title = input("Enter auction title:")
            au_description = input("Enter auction description:")
            au_timelimit = input("Enter auction destinated end time in minute:")
            data_form = "create_auction" + " " + str(self.my_data["id"]) + " " + au_title + " " + au_description + " " + au_timelimit
            encry = encry_decrypt.A3Encryption()
            decry = encry_decrypt.A3Decryption()
            encrypted_data = encry.start_encryption(data_form, self.userKey)
            client.send(bytes(encrypted_data, "utf-8"))

            recv_info = client.recv(4096)
            recv_encrypted = recv_info.decode("utf-8")
            print("Received Encrypted Data : ", recv_encrypted)
            recv_decrypted = decry.startDecryption(recv_encrypted)
            recv_decrypted = json.loads(recv_decrypted)
            print(recv_decrypted)
            client.close()
        except Exception as e:
            print(e)
        finally:
            self.auction_section()

    def enter_auction(self):
        try:
            client = self.client_runner()
            encry = encry_decrypt.A3Encryption()
            decry = encry_decrypt.A3Decryption()
            encrypted_data = encry.start_encryption("get_all_auction", self.userKey)
            client.send(bytes(encrypted_data, "utf-8"))

            recv_info = client.recv(4096)
            recv_encrypted = recv_info.decode("utf-8")
            recv_decrypted = decry.startDecryption(recv_encrypted)
            recv_decrypted = json.loads(recv_decrypted)
            client.close()
            if(any("err" in x for x in recv_decrypted)):
                print(recv_decrypted["err"])
            else:
                self.auction_lobby.update(recv_decrypted)
                for i in recv_decrypted:
                    self.active_list.update({int(i): self.auction_lobby[i]["remaining time"]})
                print(self.auction_lobby)

                self.activate_F = True
            
                counter = threading.Thread(target=self.countdown, args=(), daemon=True)
                counter.start()

                auction_id = int(input("Enter auction id to bid or Enter q to quit:"))
                if auction_id in self.active_list:
                    self.room_id = auction_id
                    print(self.room_id)
                    self.auction_lobby_in()
                else:
                    self.room_id = 0
                    print("lobby expired!")
                    self.enter_auction()
        except Exception as err:
            pass
            #print(err)
        finally:
            self.activate_F = False
            self.auction_section()
    
    def auction_lobby_in(self):
        try:
            print(self.flag)
            self.flag = True
            client = self.client_runner()
            encry = encry_decrypt.A3Encryption()
            decry = encry_decrypt.A3Decryption()
            data = "inside_lobby" + " " + str(self.room_id)
            encrypted_data = encry.start_encryption(data, self.userKey)
            client.send(bytes(encrypted_data, "utf-8"))

            recv_info = client.recv(4096)
            recv_encrypted = recv_info.decode("utf-8")
            recv_decrypted = decry.startDecryption(recv_encrypted)
            recv_decrypted = json.loads(recv_decrypted)
            self.room_data.update(recv_decrypted)
            print(self.room_data)
            client.close()

            #monitor = threading.Thread(target=self.show_countdown, args=(self.room_id,), daemon=True)
            #monitor.start()
            while self.flag:
                currency = int(input("Enter currency to bid or press 1 to quit:"))
                if currency:
                    self.place_bid(currency)
                    print(self.room_data)
        except Exception as err:
            print(err)
        finally:
            self.room_data.pop(str(self.room_id))
            self.flag = False
            self.room_id = 0
            self.enter_auction()
                
    def place_bid(self, currency):
        client = self.client_runner()
        encry = encry_decrypt.A3Encryption()
        decry = encry_decrypt.A3Decryption()
        data = "place_bid" + " " + str(self.room_id) + " " + str(self.my_data["id"])+ " " +str(currency)
        encrypted_data = encry.start_encryption(data, self.userKey)
        client.send(bytes(encrypted_data, "utf-8"))

        recv_info = client.recv(4096)
        recv_encrypted = recv_info.decode("utf-8")
        recv_decrypted = decry.startDecryption(recv_encrypted)
        recv_decrypted = json.loads(recv_decrypted)
        if "update" in recv_decrypted:
            id = recv_decrypted["update"]["id"]
            if id == self.room_id:
                highest_bid = recv_decrypted["update"]["highest bid"]
                u_name = recv_decrypted["update"]["username"]
                self.room_data[str(id)].update({"highest bid": highest_bid, "username" : u_name})
                print("Success!Current Highest offer: " + u_name+ " with " +str(highest_bid))
        elif "fail" in recv_decrypted:
            id = recv_decrypted["fail"]["id"]
            if id == self.room_id:
                highest_bid = recv_decrypted["fail"]["highest bid"]
                u_name = recv_decrypted["fail"]["username"]
                self.room_data[str(id)].update({"highest bid": highest_bid, "username" : u_name})
                print("Fail!Current Highest offer: " + u_name+ " with " +str(highest_bid))
        elif "finish" in recv_decrypted:
            id = recv_decrypted["finish"]["id"]
            highest_bid = recv_decrypted["finish"]["highest bid"]
            u_name = recv_decrypted["finish"]["username"]
            self.room_data[str(id)].update({"highest bid": highest_bid, "username" : u_name})
            print("Auction over! Winner : " + u_name+ " with " +str(highest_bid))
            time.sleep(3)
            self.flag = False
        elif "err" in recv_decrypted:
            print(recv_decrypted["err"])
            self.flag = False
        client.close()

if __name__ == "__main__":
    auction_client: Auction_client = Auction_client()

    while True:
        auction_client.client_menu()