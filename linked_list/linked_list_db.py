import pymongo

connection = pymongo.MongoClient("localhost", 27017)
database = connection["ncc_dip2"]
collection = database["user_info"]

class Node():

    def __init__(self, email: str, name: str, password: str, phone: int, point: int):
        self.email = email
        self.name = name
        self.password = password
        self.phone = phone
        self.point = point
        self.next = None

class linkedList():

    def __init__(self):
        self.head = None
    
    def listprint(self):
        temp = self.head
        while temp != None:
            print("{0} {1} {2} {3} {4}".format(temp.email, temp.name, temp.password, temp.phone, temp.point))
            temp = temp.next
    
    def printlast(self):
        temp = self.head
        while temp.next != None:
            temp = temp.next
        print("{0} {1} {2} {3} {4}".format(temp.email, temp.name, temp.password, temp.phone, temp.point))
        

    def linked_append(self, email: str, name: str, password: str, phone: int, point: int):
        newNode = Node(email, name, password, phone, point)
        if self.head == None:
            self.head = newNode
        else:
            tempNode = self.head
            while tempNode.next != None:
                tempNode = tempNode.next
            tempNode.next = newNode
    
    def load_all_data(self):
        for i in collection.find({},{"_id":0}):
            self.linked_append(i["email"],i["username"],i["password"],i["phone"],i["point"])
    
    def save_all_data(self):
        while self.head != None:
            collection.replace_one({"email" : self.head.email}, {"email" : self.head.email,"username": self.head.name, "password": self.head.password, "phone": self.head.phone, "point": self.head.point},upsert=True)
            self.head = self.head.next
        
if __name__ == '__main__':
    node1 = Node("one")
    node2 = Node("two")
    node3 = Node("three")

    linkedList = linkedList()
    linkedList.head = node1
    linkedList.head.next = node2
    linkedList.head.next.next = node3

    linkedList.listprint()
    linkedList.linked_append("four")
    linkedList.listprint()
    linkedList.load_all_data()
    linkedList.listprint()
    