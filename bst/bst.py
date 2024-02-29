class Node:

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def insert_new_data(new_data, node: Node):
    
    if node == None:
        root = Node(new_data)
        return root
    
    if new_data < node.data:
        node.left = insert_new_data(new_data, node.left)
    else:
        node.right = insert_new_data(new_data, node.right)

    return node

def show_all_data(node: Node):
    
    if node:
        show_all_data(node.left)
        print("data => ", node.data)
        show_all_data(node.right)


if __name__ == "__main__":
    root = Node(20)
    root = insert_new_data(10, root)
    root = insert_new_data(30, root)
    root = insert_new_data(5, root)
    root = insert_new_data(15, root)
    root = insert_new_data(25, root)
    root = insert_new_data(35, root)
    show_all_data(root)