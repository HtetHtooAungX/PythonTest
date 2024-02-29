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
    
def update(node: Node, email: str, *data):
    stat, n = exist(email, node)
    if email == n.email:
        if data[2] == email:            
            insert_new_data(data[0], data[1], data[2], data[3], data[4], node)
        else:
            delete(email, node)
            insert_new_data(data[0], data[1], data[2], data[3], data[4], node)
                

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

def search_by(node: Node ,*data):
    if data[0] == "email":
        flag, temp = exist(data[1], node)
        return temp
    elif data[0] == "phone":
        temp = search_ph(node, data[1])
        return temp

def search_ph(node: Node, phone):
    if node == None:
        return node
    if phone == node.phone:
        return node
    left = search_ph(node.left, phone)
    right = search_ph(node.right, phone)
    if left != None:
        return left
    if right != None:
        return right
    return None


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

def get_node(node: Node):
    if node:
        return node.id, node.username, node.email, node.password, node.phone
        

if __name__ == "__main__":
    root = Node(1,"name20","email20","password",12345)
    root = insert_new_data(2,"name10","email5","password",12345, root)
    root = insert_new_data(3,"name10","email10","password",12345, root)
    root = insert_new_data(4,"name10","email15","password",12345, root)
    root = insert_new_data(5,"name10","email25","password",12345, root)
    root = insert_new_data(6,"name10","email30","password",12345, root)
    root = insert_new_data(7,"name10","email35","password",1234, root)
    show_all_data(root)
    #stat, root1 = exist("email5", root)
    #n_password = root1.password
    #n_password = 124
    #update(root, "email35",1,"name10","email35","password1",12345)
    #show_all_data(root)
    #delete("email35", root)
    #update(root, "email35",1,"name10","email55","password1",12345)
    #show_all_data(root)
    #id, name, email, password, phone = search_by(root,"email", "email5")
    #print(name + " " + email + " " + password + " " + str(phone))
    r = search_by(root, "phone", 1234)
    print(r)