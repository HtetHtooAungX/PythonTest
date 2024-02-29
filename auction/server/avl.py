import sys

class Node:

    def __init__(self, id, owner_id, title, description,participants, expired_time):
        self.id :int= id
        self.owner_id :int = owner_id
        self.title :str = title
        self.description :str = description
        self.participants :dict = participants
        self.expired_time :int = expired_time
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:

    def insert_node(self, root, id, owner_id, title, description, participants, expired_time):

        # Find the correct location and insert the node
        if not root:
            return Node(id, owner_id, title, description, participants, expired_time)
        elif id < root.id:
            root.left = self.insert_node(root.left, id, owner_id,title, description, participants, expired_time)
        else:
            root.right = self.insert_node(root.right, id, owner_id,title, description, participants, expired_time)

        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        # Update the balance factor and balance the tree
        balanceFactor = self.getBalance(root)
        if balanceFactor > 1:
            if id < root.left.id:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)

        if balanceFactor < -1:
            if id > root.right.id:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)

        return root
    
    # Function to delete a node
    def delete_node(self, root, id):

        # Find the node to be deleted and remove it
        if not root:
            return root
        elif id < root.id:
            root.left = self.delete_node(root.left, id)
        elif id > root.id:
            root.right = self.delete_node(root.right, id)
        else:
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
            temp = self.getMinValueNode(root.right)
            root.id = temp.id
            root.right = self.delete_node(root.right,
                                          temp.id)
        if root is None:
            return root

        # Update the balance factor of nodes
        root.height = 1 + max(self.getHeight(root.left),
                              self.getHeight(root.right))

        balanceFactor = self.getBalance(root)

        # Balance the tree
        if balanceFactor > 1:
            if self.getBalance(root.left) >= 0:
                return self.rightRotate(root)
            else:
                root.left = self.leftRotate(root.left)
                return self.rightRotate(root)
        if balanceFactor < -1:
            if self.getBalance(root.right) <= 0:
                return self.leftRotate(root)
            else:
                root.right = self.rightRotate(root.right)
                return self.leftRotate(root)
        return root

    def get_total_nodes(self, root):
        if not root:
            return 0
        return 1 + self.get_total_nodes(root.left) + self.get_total_nodes(root.right)
    
    # Function to perform left rotation
    def leftRotate(self, root):
        y = root.right
        temp = y.left
        y.left = root
        root.right = temp
        root.height = 1 + max(self.getHeight(root.left),
                           self.getHeight(root.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    # Function to perform right rotation
    def rightRotate(self, root):
        y = root.left
        temp = y.right
        y.right = root
        root.left = temp
        root.height = 1 + max(self.getHeight(root.left),
                           self.getHeight(root.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        return y

    # Get the height of the node
    def getHeight(self, root):
        if not root:
            return 0
        return root.height

    # Get balance factore of the node
    def getBalance(self, root):
        if not root:
            return 0
        return self.getHeight(root.left) - self.getHeight(root.right)
    
    def getMinValueNode(self, root):
        if root is None or root.left is None:
            return root
        return self.getMinValueNode(root.left)
    
    def printHelper(self, currPtr, indent, last):
        if currPtr != None:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "
            print(currPtr.id, currPtr.height)
            self.printHelper(currPtr.left, indent, False)
            self.printHelper(currPtr.right, indent, True)

    def get_all_node_data(self, root):
        result = []
        self.collect_node_data(root, result)
        return result

    def collect_node_data(self, curr_ptr, result):
        if curr_ptr is not None:
            node_data = {
                "id": curr_ptr.id,
                "owner_id": curr_ptr.owner_id,
                "title": curr_ptr.title,
                "description": curr_ptr.description,
                "participants": curr_ptr.participants,
                "expired_time": curr_ptr.expired_time
            }
            result.append(node_data)
            self.collect_node_data(curr_ptr.left, result)
            self.collect_node_data(curr_ptr.right, result)
    
if __name__ == "__main__":
    myTree = AVLTree()
    root = None
    nums = [33, 13, 52, 9, 21, 61, 8, 11]
    for num in nums:
        root = myTree.insert_node(root, num , 1 , "title1","description",{"as" : 200}, 12345)
    myTree.printHelper(root, "", True)
    total_nodes = myTree.get_total_nodes(root)
    print("Total Nodes in the AVL Tree:", total_nodes)
    id = 33
    root = myTree.delete_node(root, id)
    print("After Deletion: ")
    myTree.printHelper(root, "", True)
    root.participants.update({"a33" : 12345})
    print(root.participants)
    total_nodes = myTree.get_total_nodes(root)
    print("Total Nodes in the AVL Tree:", total_nodes)
    all_node_data = myTree.get_all_node_data(root)
    print("All Node Data:")
    for node_data in all_node_data:
        print(node_data)