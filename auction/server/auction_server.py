import threading
import socket
import time
import json
import s_encrypt_and_decrypt
import datetime

auction_lobby = {1: {'owner_id': 0, 'title': 'w', 'description': 'w', 'participant': {0: 1000}, 'created_at' : '27/11/2023 15:50:31','expired_time': 1000}}
client_data = {0 : {"email" : "1@gmail.com", "name" : "gg", "password" : '1111', "phone" : 1234}}
active_list = {}


class ReceiveThread(threading.Thread):
    def __init__(self, client_socket, client_data, active_dist, connected_clients, auction_lobby):
        super().__init__()
        self.decrypt = s_encrypt_and_decrypt.A3Decryption()
        self.encrypt = s_encrypt_and_decrypt.A3Encryption()
        self.client_data = client_data
        self.client_socket = client_socket
        self.active_dist = active_dist
        self.connected_clients = connected_clients
        self.auction_lobby = auction_lobby

    def send_message(self, message):
        sms = bytes(message, 'utf-8')
        self.client_socket.send(sms)

    def broadcast_message(self, message):
        for client_thread in self.connected_clients:
            client_thread.send_message(message)
    
    def register(self, decrypted_list):
        try:
            not_exist = True
            r_email = decrypted_list[1]
            for i in client_data:
                if client_data[i]["email"] ==  r_email:
                    not_exist = False
            if not_exist:
                data_form = {"email": r_email, "password": decrypted_list[2], "name": decrypted_list[3], "phone": int(decrypted_list[4])}
                id = len(client_data)
                client_data.update({id: data_form})
                print("Registration success for :", client_data)
                sms = {"Reg_success": data_form}
                sms = json.dumps(sms)
            else:
                sms = {"err": "email already exist!"}
                sms = json.dumps(sms)
            sms = self.encrypt.start_encryption(sms, 'servertcp')
            str_data = bytes(sms, 'utf-8')
            self.client_socket.send(str_data)
        except Exception as e:
            error_message = {"err": str(e)}
            error_message = json.dumps(error_message)
            encrypted_message = self.encrypt.start_encryption(error_message, 'servertcp')
            str_data = bytes(encrypted_message, 'utf-8')
            self.client_socket.send(str_data)

    def login_checking(self, decrypted_list):
        l_email = decrypted_list[1]
        l_password = decrypted_list[2]
        flag = -1
        sms = {}
        for i in self.client_data:
            if self.client_data[i]["email"] == l_email and self.client_data[i]["password"] == l_password:
                flag = 1
                sms = {"id" : i, "email": self.client_data[i]["email"], "phone": self.client_data[i]["phone"]}
                sms = json.dumps(sms)
                break

        if flag == 1:
            sms = self.encrypt.start_encryption(sms, 'servertcp')
            str_data = bytes(sms, 'utf-8')
            self.client_socket.send(str_data)
        else:
            sms =  {"err" : "User name and password not found!"}
            sms = json.dumps(sms)
            sms = self.encrypt.start_encryption(sms, 'servertcp')
            str_data = bytes(sms , 'utf-8')
            self.client_socket.send(str_data)
        
    def create_lobby(self, data):
        try:
            lobby_id = len(self.auction_lobby) + 1
            created = datetime.datetime.now()
            created_str = created.strftime("%d/%m/%Y %H:%M:%S")
            e_time = int(data[4])
            self.auction_lobby.update({lobby_id:{"owner_id" : int(data[1]), "title" : data[2], "description" : data[3], "participant" : {0 :1000}, 'created_at' : created_str, "expired_time" : e_time}})
            print(self.auction_lobby)
            self.active_dist.update({lobby_id : (e_time*60)})
            sms = {"success": "Successfully created!"}
            sms = json.dumps(sms)
            sms = self.encrypt.start_encryption(sms, 'servertcp')
            str_data = bytes(sms, 'utf-8')
            self.client_socket.send(str_data)
        except Exception as e:
            sms = {"err": str(e)}
            sms = json.dumps(sms)
            sms = self.encrypt.start_encryption(sms, 'servertcp')
            str_data = bytes(sms, 'utf-8')
            self.client_socket.send(str_data)
    
    def get_all_auction(self):
        try:
            dataform :dict = {}
            if len(self.active_dist):
                for i in self.active_dist:
                    u_name_highbid :str = ""
                    highest_bid :int = 0
                    if len(self.auction_lobby[i]["participant"]) > 0:
                        for j in self.auction_lobby[i]["participant"]:
                            if self.auction_lobby[i]["participant"][j] > highest_bid:
                                highest_bid = self.auction_lobby[i]["participant"][j]
                                u_name_highbid = self.client_data[j]["name"]
                    dataform.update({int(i):{"title" : self.auction_lobby[i]["title"], "description" :  self.auction_lobby[i]["description"],"highest bid": highest_bid, "username" : u_name_highbid, "remaining time" : self.active_dist[i]}})
                    print(dataform)
            else:
                dataform.update({"err": "No lobby found!"})
            sms = json.dumps(dataform)
            data = self.encrypt.start_encryption(sms, 'servertcp')
            str_data = bytes(data, 'utf-8')
            self.client_socket.send(str_data)
        except Exception as e:
            error_message = {"err": str(e)}
            error_message = json.dumps(error_message)
            encrypted_message = self.encrypt.start_encryption(error_message, 'servertcp')
            str_data = bytes(encrypted_message, 'utf-8')
            self.client_socket.send(str_data)

    def send_lobby_detail(self, data):
        try:
            dataform :dict = {}
            id = int(data[1])
            u_name_highbid :str = ""
            highest_bid :int = 0
            if len(self.auction_lobby[id]["participant"]) > 0:
               for j in self.auction_lobby[id]["participant"]:
                    if self.auction_lobby[id]["participant"][j] > highest_bid:
                        highest_bid = self.auction_lobby[id]["participant"][j]
                        u_name_highbid = self.client_data[int(j)]["name"]
            if id in active_list:
                dataform.update({id:{"title" : self.auction_lobby[id]["title"], "description" :  self.auction_lobby[id]["description"],"highest bid": highest_bid, "username" : u_name_highbid, "remaining time" : self.active_dist[id]}})
            else:
                dataform.update({"finish": {"id": id}})
            sms = json.dumps(dataform)
            data = self.encrypt.start_encryption(sms, 'servertcp')
            str_data = bytes(data, 'utf-8')
            self.client_socket.send(str_data)
        except Exception as e:
            error_message = {"err": str(e)}
            error_message = json.dumps(error_message)
            encrypted_message = self.encrypt.start_encryption(error_message, 'servertcp')
            str_data = bytes(encrypted_message, 'utf-8')
            self.client_socket.send(str_data)
    
    def update_lobby(self, data):
        try:
            print(data)
            dataform :dict = {}
            id = int(data[1])
            u_id = int(data[2])
            u_name_highbid :str = self.client_data[u_id]["name"]
            highest_bid = int(data[3])

            n_u_name_highbid :str = ""
            n_highest_bid :int = 0

            if len(self.auction_lobby[id]["participant"]) > 0:
                for j in self.auction_lobby[id]["participant"]:
                        if self.auction_lobby[id]["participant"][j] > n_highest_bid:
                            n_highest_bid = self.auction_lobby[id]["participant"][j]
                            n_u_name_highbid = self.client_data[int(j)]["name"]
                if id in active_list:                
                    if n_highest_bid < highest_bid:
                        self.auction_lobby[id]["participant"].update({u_id : highest_bid})
                        dataform.update({"update" : {"id" : id, "highest bid": highest_bid, "username" : u_name_highbid}})
                    else:
                        dataform.update({"fail" : {"id" : id, "highest bid": n_highest_bid, "username" : n_u_name_highbid}})
                        print(self.auction_lobby)
                else:
                    dataform.update({"finish": {"id": id, "highest bid": n_highest_bid, "username" : n_u_name_highbid}})
                    print(dataform)
            else:
                self.auction_lobby[id]["participant"].update({u_id : highest_bid})
                dataform.update({"update" : {"id" : id, "highest bid": highest_bid, "username" : u_name_highbid}})
                print(self.auction_lobby)
            sms = json.dumps(dataform)
            encrypted_message = self.encrypt.start_encryption(sms, 'servertcp')
            str_data = bytes(encrypted_message, 'utf-8')
            self.client_socket.send(str_data)
        except Exception as e:
            error_message = {"err": str(e)}
            error_message = json.dumps(error_message)
            encrypted_message = self.encrypt.start_encryption(error_message, 'servertcp')
            str_data = bytes(encrypted_message, 'utf-8')
            self.client_socket.send(str_data)

            
    def run(self):
        try:
            data = self.client_socket.recv(1024).decode("utf-8")
            decrypted = self.decrypt.startDecryption(data)
            print("#:", decrypted)
            decrypted_list = decrypted.split(' ')

            data = ''
            if decrypted_list[0] == 'info':
                data = 'data received from client:' + decrypted_list[0]
            elif decrypted_list[0] == 'register':
                self.register(decrypted_list)
            elif decrypted_list[0] == 'login':
                self.login_checking(decrypted_list)
            elif decrypted_list[0] == 'get':
                self.get_items_info()
            elif decrypted_list[0] == 'create_auction':
                self.create_lobby(decrypted_list)
            elif decrypted_list[0] == 'get_all_auction':
                self.get_all_auction()
            elif decrypted_list[0] == 'inside_lobby':
                self.send_lobby_detail(decrypted_list)
            elif decrypted_list[0] == 'place_bid':
                self.update_lobby(decrypted_list)
        except Exception as e:
            print(f"Error in ReceiveThread: {e}")

        finally:
            # Handle client disconnect
            self.client_socket.close()
            self.connected_clients.remove(self)
            writeFile()

def countdown(active_list):
    while True:
        for i in list(active_list.keys()):
            if active_list[i] > 0:
                active_list[i] -= 1
            else:
                active_list.pop(i)
                print(auction_lobby)
        time.sleep(1)
        #print(active_list)

def readfile():
    with open("db/users.txt",'r') as dbfile:
        datas=dbfile.readlines()
        for one in datas:
            oneData = one.split(" ")
            id = int(oneData[0])
            data_form = {id:{"email":oneData[1],"name":oneData[2],"password":oneData[3],"phone":int(oneData[4].strip())}}
            client_data.update(data_form)
        print(client_data)
        dbfile.close()

    with open("db/auction_lobby.txt",'r') as dbfile:
        datas=dbfile.readlines()
        for one in datas:
            oneData = one.split("#")
            id = int(oneData[0])
            participant = json.loads(oneData[4])
            participant = {int(key): value for key, value in participant.items()}
            data_form = {id:{'owner_id': int(oneData[1]), 'title': oneData[2], 'description': oneData[3], 'participant': participant, 'created_at' : oneData[5], 'expired_time': int(oneData[6].strip())}}
            auction_lobby.update(data_form)
        print(auction_lobby)
        dbfile.close()

def writeFile():
    with open("db/users.txt", 'w') as dbfile:
        for i in client_data:
            email = client_data[i]["email"]
            user_name = client_data[i]["name"]
            password = client_data[i]["password"]
            phone = client_data[i]["phone"]
            total_user_data = str(i) + ' ' + email + ' ' + user_name + ' ' + password + ' ' + str(phone)
            dbfile.write(total_user_data)
            dbfile.write("\n")
        dbfile.close()
    #{1: {'owner_id': 0, 'title': 'w', 'description': 'w', 'participant': {0: 1000}, 'expired_time': 1000}}
    with open("db/auction_lobby.txt", 'w') as dbfile:
        for i in auction_lobby:
            owner_id = auction_lobby[i]["owner_id"]
            title = auction_lobby[i]["title"]
            description = auction_lobby[i]["description"]
            participant = json.dumps(auction_lobby[i]["participant"])
            created_str = auction_lobby[i]["created_at"]
            expired_time = auction_lobby[i]["expired_time"]
            total_user_data = str(i) + '#' + str(owner_id) + '#' + title + '#' + description + '#' + participant + '#' + created_str + "#" + str(expired_time)
            dbfile.write(total_user_data)
            dbfile.write("\n")
        dbfile.close()
    
def time_calculator(created_time, expired_time):
    result = 0
    c_time = datetime.datetime.strptime(created_time, "%d/%m/%Y %H:%M:%S")
    e_time = datetime.timedelta(minutes=expired_time)
    t_time = c_time + e_time
    curr_time = datetime.datetime.now()
    if t_time > curr_time:
        duration = t_time - curr_time
        result = duration.seconds
    return result

def main():
    host = "localhost"
    port = 8888

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print("Server listening on port:{} and ip{}".format(host, port))

    connected_clients = []

    counter = threading.Thread(target=countdown, args=(active_list,), daemon=True)
    counter.start()
    #boot up server
    readfile()
    for i in auction_lobby:
        created_str = auction_lobby[i]["created_at"]
        e_time = auction_lobby[i]["expired_time"]
        duration = time_calculator(created_str, e_time)
        if duration:
            active_list.update({int(i) : duration})
    try:
        while True:
            client, address = server.accept()
            print("Accepted Connection from -{} : {}".format(address[0], address[1]))

            new_thread = ReceiveThread(client, client_data, active_list, connected_clients, auction_lobby)
            new_thread.start()

            connected_clients.append(new_thread)
    except Exception as err:
        print(err)

if __name__ == "__main__":
    main()