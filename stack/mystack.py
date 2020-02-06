class Stack:
    def __init__(self):
        self.elements = []

    def push(self, element):
        self.elements.append(element)

    def pop(self):
        return self.elements.pop()

    def isEmpty(self):
        if self.elements == []:
            return True
        else:
            return False

    def size(self):
        return len(self.elements)

    def peek(self):
        if self.isEmpty() is False:
            return self.elements[-1]
        else:
            return None