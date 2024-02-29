import linked_list_db as db
#linkedlistdb = db.linkedList()
#linkedlistdb.load_all_data()
#linkedlistdb.linked_append("asd0@gmail.com", "asd", "12345", 94537, 100)
#linkedlistdb.linked_append("asd1@gmail.com", "asd", "12345", 94537, 100)
#linkedlistdb.listprint()
#linkedlistdb.save_all_data()
#while linkedlistdb.head != None:
#    print(linkedlistdb.head.name)
#    if linkedlistdb.head.name == "win5@gmail.com":
#       break
#    linkedlistdb.head = linkedlistdb.head.next
class Voting:
    def __init__(self):
        self.students = {0: {"name": "James", "v_mark": 0, "voter": []},
                         1: {"name": "John", "v_mark": 0, "voter": []},
                         2: {"name": "Rooney", "v_mark": 0, "voter": []},
                         3: {"name": "Ronaldo", "v_mark": 0, "voter": []},
                         4: {"name": "Messi", "v_mark": 0, "voter": []}
                         }
        self.linkedlistdb: db = db.linkedList()
        self.id: int = 0

        self.l_id: int = 0
        self.linkedlistdb.load_all_data()

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
            self.linkedlistdb.save_all_data()
            exit(1)
        else:
            print("Invalid Option")
            self.main_option()

    def register(self):
        print("This is register option ")
        try:
            r_email = input("Enter your email address to register!")
            flag = self.email_checking(r_email)
            if flag == 1:
                is_exist,u_data = self.email_db_check(r_email)
                if is_exist == -1:
                    while True:
                        pass1 = input("Enter your password to register:")
                        pass2 = input("Enter your password Again  to register:")
                        if pass1 == pass2:
                            r_name = input("Enter your name to register!")
                            r_phone = int(input("Enter your phone to register!"))
                            r_point = int(input("Enter your point:"))
                            self.linkedlistdb.linked_append(r_email,r_name,pass1,r_phone,r_point)
                            break
                        else:
                            print("Password not match!")
                else:
                    print("Email already exist!")
                    self.register()
            else:
                print("Email Form Invalid\nTry Again! ")
                self.register()
            
        except Exception as err:
            print("Invalid User Input!Try Again Sir!")
            self.register()

        print("Registration success :\n")
        self.linkedlistdb.printlast()
        self.main_option()

    def login(self):
        try:
            l_email = input("Enter your email to login:")
            flag = self.email_checking(l_email)
            if flag == 1:
                l_pass = input("Enter your password to login:")
                is_valid,user_db  = self.login_check(l_email, l_pass)
                if is_valid:
                    self.user_option(user_db)
                else:
                    print("Incorrect email or password!")
                    self.main_option()
        except Exception as e:
            print(e)
            self.login()
    
    def user_option(self, user_db):
        try:
            option = int(input("Press 1 to transfers point\nPress 2 to Exit:"))
        except Exception as err:
            # print(err)
            print("Pls insert only Integer eg:1,2,3")

        if option == 1:
            self.transfer_point(user_db)
        elif option == 2:
            self.linkedlistdb.save_all_data()
            exit(1)
        else:
            print("Invalid Option")
            self.user_option()

    def transfer_point(self, userdb):
        try:
            print("your current point is: ",userdb.point)
            t_point = int(input("Enter amount to transfer:"))
            if t_point <= userdb.point:
                t_email = input("Enter where you want to transfer:")
                is_exist,t_db = self.email_db_check(t_email)
                if is_exist == 1:
                    userdb.point -= t_point
                    t_db.point += t_point
                    print("transfer complete!your current point is ", userdb.point)
                    self.user_option(userdb)
                else:
                    print("email not exist")
                    self.transfer_point(userdb)
            else:
                print("Over limit!")
                self.transfer_point(userdb)
        except Exception as err:
            print(err)
            self.transfer_point(userdb)
            
    def login_check(self, email, password):
        temp = self.linkedlistdb.head
        valid = False
        while temp != None:
            if temp.email == email and temp.password == password:
                valid = True
                break
            temp = temp.next
        return valid,temp

    def email_db_check(self, r_email):
        temp = self.linkedlistdb.head
        exist = -1
        while temp != None:
            if temp.email == r_email:
                exist = 1
                break
            temp = temp.next
        return exist,temp
        
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

if __name__ == '__main__':
    voting = Voting()
    voting.main_option()