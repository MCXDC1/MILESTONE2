
class ListNode:

    def __init__(self, data, link = None):
        self.data = data
        self.link = link

class LinkedList:

    def __init__(self):
        self._head = None
        self._tail = None
    
    def addfirst(self, item):
        self._head = ListNode(item, self._head)
        if self._tail is None:
            self._tail = self._head

    def addlast(self, item):
        if self._head is None:
            self.addfirst(item)
        else:
            self._tail.link = ListNode(item)
            self._tail = self._tail.link

    def removefirst(self):
        item = self._head.data
        self._head = self._head.link
        if self._head is None:
            self._tail = None
        return item
    
    def removelast(self):
        if self._head is self._tail:
            self.removefirst()
        else:
            curr_node = self._head
            while curr_node.link is not self._tail:
                curr_node = curr_node.link
            item = self._tail.data
            self._tail = curr_node
            self._tail.link = None
            return item
        
class LinkedQueue:
    
    def __init__(self):
        self._L = LinkedList()

    def enqueue(self, item):
        self._L.addlast(item)

    def dequeue(self):
        if len(self._L) == 0:
            raise ValueError("Cannot remove from an empty queue.")
        else:
            return self._L.removefirst()

    def peek(self):
        item = self._L.removefirst()
        self._L.addfirst(item)
        return item
    
    def __len__(self):
        return len(self._L)
    
    def isEmpty(self):
        return len(self) == 0





