class Node:

    def __init__(self, id, name, email, password, phone):
        self.id :int= id
        self.username :str = name
        self.email :str = email
        self.password :str = password
        self.phone :int =phone
        self.left = None
        self.right = None


def insert_new_data(id, name, email, password, phone, node: Node):
    
    if node == None:
        root = Node(id, name, email, password, phone)
        return root
    
    if email < node.email:
        node.left = insert_new_data(id, name, email, password, phone, node.left)
    elif email > node.email:
        node.right = insert_new_data(id, name, email, password, phone, node.right)
    else:
        node.id = id
        node.username = name
        node.email = email
        node.password = password
        node.phone = phone

    return node

def show_all_data(node: Node):
    
    if node:
        show_all_data(node.left)
        print("data => ", node.id, node.username, node.email, node.password, node.phone)
        show_all_data(node.right)

def exist(email: str, node: Node):
    temp : Node= node
    if temp == None:
        return False, temp
    
    if temp.email == email:
        return True, temp
    
    if email < temp.email:
        return exist(email, temp.left)

    if email > temp.email:
        return exist(email, temp.right)
    
def update(node: Node, email: str, **data):
    if node == None:
        return node
    
    if email < node.email:
        return update(node.left , email, **data)
    
    if email > node.email:
        return update(node.right, email, **data)
    
    if email == node.email:
        if "email" not in data.keys():
            for key, value in data.items():
                node.key: Node = value

def delete(email: str, node: Node):
    if node == None:
        return node
    elif node.email > email:
        node.left = delete(email, node.left)
    elif node.email < email:
        node.right = delete(email, node.right)
    else:
        if node.left == None and node.right == None:
            return None
        elif node.left == None:
            return node.right
        elif node.right == None:
            return node.left
        else:
            temp: Node = get_min(node.right)
            node.id = int(temp.id)
            node.username = temp.username
            node.email = temp.email
            node.password = temp.password
            node.phone = int(temp.phone)
            node.right = delete(temp.email, node.right)
    return node

def get_min(node: Node):
    temp = node
    while temp.left:
        temp = temp.left
    return temp

def get_max(node: Node):
    temp = node
    while temp.right:
        temp = temp.right
    return temp

if __name__ == "__main__":
    root = Node(1,"name20","email20","password",12345)
    root = insert_new_data(1,"name10","email5","password",12345, root)
    root = insert_new_data(1,"name10","email10","password",12345, root)
    root = insert_new_data(1,"name10","email15","password",12345, root)
    root = insert_new_data(1,"name10","email25","password",12345, root)
    root = insert_new_data(1,"name10","email30","password",12345, root)
    root = insert_new_data(1,"name10","email35","password",12345, root)
    show_all_data(root)
    stat ,root1 = exist("email5",root)
    root1.phone = 123
    print(stat)
    print(exist("email15",root))
    print(exist("email35",root))
    print(exist("email25",root))
    print(exist("email45",root))
    print(get_min(root))
    print(get_max(root))
    #delete("email10", root)
    #show_all_data(root)
    print("____________________")
    #delete("email5", root)
    #show_all_data(root)
    print("____________________")
    delete("email20", root)
    show_all_data(root)
    print("____________________")
    #update(root, "email10", password = 123)
    #show_all_data(root)