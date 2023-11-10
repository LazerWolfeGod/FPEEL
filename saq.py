class Queue: 
    def __init__(self, max_size): 
        self.items = []  
        self.max_size = max_size     
            
    def enqueue(self, item): 
        if self.is_full(): 
            print('Queue is full') 
            return -1 
        self.items.append(item) 
        print(self.items) 

    def dequeue(self):  
        if not self.is_empty(): 
            self.items.pop(0) 
            print(self.items) 

    @property 
    def front(self): 
        return self.items[0] 
    
    @property 
    def back(self): 
        return self.items[-1] 

    def is_empty(self): 
        return not self.items  
    
    def is_full(self): 
        return len(self.items) == self.max_size 

class Stack: 
    def __init__(self, max_size): 
        self.items = []   
        self.max_size = max_size 
    
    def push(self, item): 
        if self.is_full(): 
            print('Stack Overflow Error') 
            return -1 
        self.items.append(item) 
        print(self.items)  
    
    def pop(self): 
        if self.is_empty(): 
            print('Stack Underflow Error')  
            return -1 
        self.items.pop() 
        print(self.items)    

    @property    
    def top(self): 
        return self.items[-1] 
    
    @property 
    def bottom(self): 
        return self.items[0]       

    def is_full(self): 
        return len(self.items) == self.max_size           
    
    def is_empty(self): 
        return not self.items 


q = Queue(5) 
q.enqueue(1)  
q.enqueue(2)
q.enqueue(3) 
q.enqueue(4) 
q.enqueue(5)  
q.enqueue(6) 
q.dequeue()  
q.dequeue() 
q.dequeue()  

s = Stack(5) 
s.push(1) 
s.push(2) 
s.push(3) 
s.push(4) 
s.push(5) 
s.push(6) 
s.pop() 
s.pop() 
s.pop() 