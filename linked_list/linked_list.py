class Node():

    def __init__(self,name: str):
        self.name = name
        self.next = None

class linkedList():

    def __init__(self):
        self.head = None
    
    def listprint(self):
      temp = self.head
      while temp != None:
         print (temp.name)
         temp = temp.next

    def linked_append(self, data):
        newNode = Node(data)
        tempNode = self.head
        while tempNode.next != None:
            tempNode = tempNode.next
        tempNode.next = newNode

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