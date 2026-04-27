class Node:
    def __init__(self, data=None):
        self.data = data
        self.prev = None
        self.next = None


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.last = None

    def insert(self, data):
        if self.head is None:
            node = Node(data)
            self.head = node
            self.last = node
        else:
            node = Node(data)
            self.last.next = node
            node.prev = self.last
            self.last = node

    def combine_node(self, data_1, data_2):
        ptr = self.head
        while ptr.data != "_":
            if ptr.data == data_1 and ptr.next.data == data_2:
                ptr.data += ptr.next.data
                ptr.next.next.prev = ptr
                ptr.next = ptr.next.next
                break
            else:
                ptr = ptr.next

    def print_ll(self):
        ptr = self.head
        while ptr is not None:
            print(f"{ptr.data}->")
            ptr = ptr.next
