
graph={'A':['D','B'],
       'B':['A','E','C','F'],
       'C': ['B','F'],
       'D': ['A','E'],
       'E':['D','B'],
       'F':['B','C']}  

# Breadth First Traversal

def breadth_first_traversal(node):
 stack = []                                       
 stack.append(node)                        
 visited.append(node)
  
 while stack:                                  
  node = stack.pop(0)                   
  print (node, end = " ")                
  for i in graph[node]:                     
   if i not in visited:
    stack.append(i) 
    visited.append(i) 
              
print("Breadth First Traversal")
visited=[]
breadth_first_traversal("A")


# Depth First Traversal

print("\nDepth First Traversal")
def depth_first_traversal(node): 
 visited.append(node)
 print (node, end = " ")
 for i in graph[node]: 
  if i not in visited: 
   depth_first_traversal(i)
 return visited

visited = []               
print(depth_first_traversal('A'))  

#Depth first traversal iterative
# This returns a differnt path
# compared withe the recursive approach 

print("\nDepth First Traversal - iterative")
def depth_first_traversal_iterative(node):
 
 stack=[node]
 visited =[]
 print(node,"".join(stack),"".join(visited))
 while stack:
  node = stack.pop()
  print(node,"".join(stack),"".join(visited))
  if node not in visited:
   visited.append(node)
   print(node,"".join(stack),"".join(visited))
   for i in graph[node]:
    stack.append(i)
    print(node,"".join(stack),"".join(visited),i)

 return visited

print(depth_first_traversal_iterative("A"))





