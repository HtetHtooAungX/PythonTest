import binaryst as bst
bst.insert_new_data

class Customer:
    def __init__(self):
        self.root = bst.Node(1,"name20","email20","password",12345)
        self.root = bst.insert_new_data(2,"name10","email5","password",12345, self.root)
        self.root = bst.insert_new_data(3,"name10","email10","password",12345, self.root)
        self.root = bst.insert_new_data(4,"name10","email15","password",12345, self.root)
        self.root = bst.insert_new_data(5,"name10","email25","password",12345, self.root)
        self.root = bst.insert_new_data(6,"name10","email30","password",12345, self.root)
        self.root = bst.insert_new_data(7,"name10","email35","password",12345, self.root)
        bst.show_all_data(self.root)
        self.id = 7

    def main_option(self):
        option = 0
        try:
            option = int(input("Press 1 to add new customer:\nPress 2 to update customer data:\nPress 3 to delete:\nPress 4 to show all customer:\nPress 5 to search by:\nPress 6 to exit:"))
        except Exception as err:
            # print(err)
            print("Pls insert only Integer eg:1,2,3")

        if option == 1:
            self.add_n_cus()
        elif option == 2:
            self.update_cus()
        elif option == 3:
            self.delete_cus()
        elif option == 4:
            bst.show_all_data(self.root)
            self.main_option()
        elif option == 5:
            self.search()
        elif option == 6:
            exit(1)
        else:
            print("Invalid Option")
            self.main_option()

    def add_n_cus(self):
        try:
            r_email = input("Enter your email address to register!")
            flag = 1
            if flag == 1:
                is_exist,cus_n = bst.exist(r_email, self.root)
                if is_exist == False:
                    while True:
                        pass1 = input("Enter your password to register:")
                        pass2 = input("Enter your password Again  to register:")
                        if pass1 == pass2:
                            r_name = input("Enter your name to register!")
                            r_phone = int(input("Enter your phone to register!"))
                            self.id += 1
                            bst.insert_new_data(self.id, r_name, r_email, pass1, r_phone, self.root)
                            break
                        else:
                            print("Password not match!")
                else:
                    print("Email already exist!")
                    self.add_n_cus()
            else:
                print("Email Form Invalid\nTry Again! ")
                self.add_n_cus()
            
        except Exception as err:
            print("Invalid User Input!Try Again Sir!")
            self.add_n_cus()

        print("Registration success :\n")
        bst.show_all_data(self.root)
        self.main_option()
    
    def update_cus(self):
        o_email = input("Enter target email to update:")
        flag, u_node = bst.exist(o_email, self.root)
        if flag:
            id, name, email, password, phone = bst.get_node(u_node)
            while True:
                option = int(input("Press 1 to username:\nPress 2 to email:\nPress 3 to password:\nPress 4 to phone:\nPress 5 to confirm update:"))
                if option == 1:
                    n_name = input("Enter new name:")
                    name = n_name
                    print("____________________")
                elif option == 2:
                    n_email = input("Enter new email:")
                    email = n_email
                    print("____________________")
                elif option == 3:  
                    n_password = input("Enter new password:")
                    password = n_password
                    print("____________________")
                elif option == 4:
                    n_phone = input("Enter new phone:")
                    phone = n_phone
                    print("____________________")
                elif option == 5:
                    bst.update(self.root, o_email, int(id), name, email, password, int(phone))
                    bst.show_all_data(self.root)
                    self.main_option()
        else:
            print("Invalid email!")
            self.update_cus()
    
    def delete_cus(self):
        d_email = input("Enter customer email to delete:")
        flag, u_node = bst.exist(d_email, self.root)
        if flag:
            bst.delete(d_email, self.root)
            print("deletion complete")
            bst.show_all_data(self.root)
            self.main_option()
        else:
            print("email not exist!")
            self.delete_cus()
    
    def search(self):
        try:
            option = int(input("Press 1 to search by email:\nPress 2 to search by phone no:\nPress 3 to go back:"))
            #while True:
            if option == 1:
                t_email = input("Enter target email:")
                temp = bst.search_by(self.root, "email", t_email)
                if temp:
                    id, name, email, password, phone = bst.get_node(temp)
                    print(str(id)+ " " + name + " " + email + " " + password + " " + str(phone))
                    print("____________________")
                    self.search()
                else:
                    print("email not exist")
                    self.search()
                
            elif option == 2:
                t_phone = int(input("Enter target phone:"))
                temp = bst.search_by(self.root, "phone", t_phone)
                if temp:
                    id, name, email, password, phone = bst.get_node(temp)
                    print(str(id)+ " " + name + " " + email + " " + password + " " + str(phone))
                    print("____________________")
                    self.search()
                else:
                    print("Phone not exist")
                    self.search()
                
            else:
                self.main_option()
                    
        except Exception as e:
            print(e)
            self.search()

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
        
if __name__ == "__main__":
    customer = Customer()
    customer.main_option()