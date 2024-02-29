class Voting:
    def __init__(self):
        print("Working in Voting special method or constructor ")
        self.students = {0: {"name": "James", "v_mark": 0, "voter": []},
                         1: {"name": "John", "v_mark": 0, "voter": []},
                         2: {"name": "Rooney", "v_mark": 0, "voter": []},
                         3: {"name": "Ronaldo", "v_mark": 0, "voter": []},
                         4: {"name": "Messi", "v_mark": 0, "voter": []}
                         }
        self.db: dict = {}
        self.id: int = 0

        self.l_id: int = 0
        self.load_all_data()

    def main_option(self):
        option = 0
        try:
            option = int(input("Press 1 to Register\nPress 2 to Login\nPress 3 to Exit:"))
        except Exception as err:
            # print(err)
            print("Pls insert only Integer eg:1,2,3")

        if option == 1:
            self.register()
        elif option == 2:
            self.login()
        elif option == 3:
            self.record_all_data()
            exit(1)
        else:
            print("Invalid Option")
            self.main_option()

    def register(self):
        print("This is register option ")
        pass_match = False
        try:
            r_email = input("Enter your email address to register!")
            r_name = input("Enter your name to register!")
            r_phone = int(input("Enter your phone to register!"))
            r_address = input("Enter your address:")
            r_money = int(input("Enter your money:"))

            while pass_match is False:
                r_pass1 = input("Enter your password to register!")
                r_pass2 = input("Retype your password:")

                if r_pass1 != r_pass2:
                    print("Your passwords not match")

                else:
                    print("Your passwords was recorded!")
                    self.id = len(self.db)
                    data_form: dict = {self.id: {"email": r_email, "name": r_name, "phone": r_phone,
                                                 "address": r_address, "password": r_pass1, "Money": r_money, "Voting Token": 1}}

                    self.db.update(data_form)

                    pass_match = True
        except Exception as err:
            print("Invalid User Input!Try Again Sir!")
            self.register()

        print("Registration success :", self.db[self.id]["name"])
        print(self.db)

        r_option = False
        while r_option is False:
            try:
                user_option = int(input("Press 1 to Login!\nPress 2 Main Option:\nPress3 to Exit!:"))
                if user_option == 1:
                    self.login()
                    break
                elif user_option == 2:
                    self.main_option()
                    break
                elif user_option == 3:
                    self.record_all_data()
                    exit(1)
                else:
                    print("Pls read again for option!")

            except Exception as err:
                print("Invalid Input!", err)

    def login(self):
        print("This is login option ")
        length = len(self.db)
        try:
            l_email = input("Enter your email to Login:")
            l_pass = input("Enter your pass to Login:")
            self.l_id = -1
            for i in range(length):
                if l_email == self.db[i]["email"] and l_pass == self.db[i]["password"]:
                    self.l_id = i
                    break
            if self.l_id != -1:
                self.user_sector(self.l_id)
            else:
                print("Username or Password incorrect!")
                self.login()

        except Exception as err:
            print(err, "\nInvalid input:")

    def user_sector(self, l_id):
        print("Welcome", self.db[l_id]["name"])
        print("Your Current Token: ",self.db[l_id]["Voting Token"])

        print("Please select one!")
        for i in range(len(self.students)):
            print("Id:{} - Name {} - Current Vote Mark: {}".format(i, self.students[i]["name"],
                                                                   self.students[i]["v_mark"]
                                                                   ))

        try:
            v_id = int(input("Just Enter Id number to vote:"))
            if self.db[l_id]["Voting Token"] > 0:
                self.students[v_id]["v_mark"] += 1
                self.students[v_id]["voter"].append(self.db[l_id]["name"])
                self.db[l_id]["Voting Token"] -= 1
                print("Congratulation you are voted!")
                print("{} now voting mark is : {}".format(self.students[v_id]["name"],self.students[v_id]["v_mark"]))

                for i in range(len(self.students[v_id]["voter"])):
                    print("Voter: ",self.students[v_id]["voter"][i])
            else:
                print("Run out of token!Pls buy some:")



        except Exception as err:
            print(err)


        while True:
            try:
                vote_option = int(input("Press 1 to Vote Again!\nPress 2 to get Main Option!\nPress 3 to Buy token:\nPress 4 to Refill Money:\nPress 5 to Force Quit:"))

                if vote_option == 1:
                    self.user_sector(l_id)
                    break
                elif vote_option == 2:
                    self.main_option()
                    break
                elif vote_option == 3:
                    self.exchange_token(l_id)
                    break
                elif vote_option == 4:
                    self.refill_money(l_id)
                    break
                elif vote_option == 5:
                    self.record_all_data()
                    exit(1)
                else:
                    print("Invalid option after vote!")
            except Exception as err:
                print(err)

    def exchange_token(self, l_id):
        print("Your money:",self.db[l_id]["Money"])
        print("Exchange rate: 100 = 1 Token")

        try:
            b_token = int(input("Enter token amount to buy:"))
            if(self.db[l_id]["Money"] >= b_token*100):
                while b_token > 0:
                    self.db[l_id]["Money"] -= 100
                    self.db[l_id]["Voting Token"] += 1
                    b_token -= 1
                print("Complete exchange!Your Current token:", self.db[l_id]["Voting Token"])
            else:
                print("Not enough money!")
        except Exception as err:
            print(err)
            self.exchange_token(l_id)

        while True: 
            try:
                vote_option = int(input("Press 1 to Buy Again!\nPress 2 to get User Sector!\nPress 3 to Force Quit:"))

                if vote_option == 1:
                    self.exchange_token(l_id)
                    break
                elif vote_option == 2:
                    self.user_sector(l_id)
                    break
                elif vote_option == 3:
                    self.record_all_data()
                    exit(1)
                else:
                    print("Invalid option after vote!")
            except Exception as err:
                print(err)
            
    def refill_money(self, l_id):
        try:
            r_money = int(input("Enter the amount to refill or Press 0 to go back:"))
            self.db[l_id]["Money"] += r_money
            print("Process Complete!Your Current Money:", self.db[l_id]["Money"])
            self.user_sector(l_id)
        except Exception as err:
            print(err)
            self.refill_money(l_id)

    def record_all_data(self):
        with open("Votingdb.txt",'w') as dbfile:
            dbfile.write("userdb")
            dbfile.write("\n")
            for i in range(len(self.db)):
                email = self.db[i]["email"]
                user_name = self.db[i]["name"]
                phone = self.db[i]["phone"]
                address = self.db[i]["address"]
                password = self.db[i]["password"]
                money = self.db[i]["Money"]
                token = self.db[i]["Voting Token"]
                
                total_user_data = email + ' ' + user_name + ' ' + str(phone) + ' ' + address +  ' ' + password + ' ' +  str(money) + ' ' + str(token)

                dbfile.write(total_user_data)
                dbfile.write("\n")
            dbfile.write("Voter_list")
            dbfile.write("\n")
            for i in range(len(self.students)):
                Voter_list: str = str(i) + " "
                for j in range(len(self.students[i]["voter"])):
                    if j == len(self.students[i]["voter"])- 1:
                        Voter_list += self.students[i]["voter"][j]
                        break
                    Voter_list += self.students[i]["voter"][j] + ' '
                dbfile.write(Voter_list)
                dbfile.write("\n")
            dbfile.close()

    def load_all_data(self):
        with open("Votingdb.txt",'r') as dbfile:
            datas=dbfile.readlines()
            flag = 0
            for one in datas:
                if one == "userdb\n":
                    flag = 1
                    continue
                elif one == "Voter_list\n":
                    flag = 2
                    continue
                if flag == 1:
                    oneData = one.split(" ")
                    id = len(self.db)
                    data_form = {id:{"email":oneData[0],"name":oneData[1],"phone":int(oneData[2]),"address":oneData[3],"password":oneData[4],"Money":int(oneData[5]),"Voting Token":int(oneData[6].strip())}}
                    self.db.update(data_form)
                elif flag == 2:
                    #one = one.strip()
                    oneData = one.strip().split(" ")
                    s_id = int(oneData[0])
                    if len(oneData) > 1:
                        for i in range(1, len(oneData)):
                            self.students[s_id]["voter"].append(oneData[i])
                            self.students[s_id]["v_mark"] += 1
            print("Loading Complete!")
            print(self.db)
            dbfile.close()