
from utils import BinaryTree, TreeNode
    
class BST(BinaryTree):
    def __init__(self, arr, sort = False):
        super().__init__()
        if sort:
            #order array
            arr = sorted(arr)
            sortedArr = []
            
            def sortArray(arr):
                #Append the middle value in arr into sortedArr
                if len(arr) == 0:
                    return
                if len(arr) == 1:
                    sortedArr.append(arr[0])
                else:
                    mid = len(arr)//2
                    #use recursion to keep getting middle values and return sorted binary serach tree
                    sortedArr.append(arr[mid])
                    sortArray(arr[:mid])
                    sortArray(arr[mid+1:])
            
            #call function sorted array
            sortArray(arr)

            #go through sorted Array and add each element to a node
            for value in sortedArr:
                self.addNode(value)
            
        else: #do this if sorted is false
            for value in arr:
                self.addNode(value)        
    def addNode(self,data):
        if self.root==None:
            #make root if tree does not already have a root
            self.root = TreeNode(data)
        else:
            #assign data to appropriate node (keep searching until it is less than a node in the tree)
            cur = self.root
            while True:
                if data < cur.data: #go to left
                    if cur.less == None:
                        cur.less = TreeNode(data)
                        return
                    else:
                        #assign new node to current
                        cur = cur.less
                else:#go to the right
                    if cur.more == None:
                        cur.more = TreeNode(data)
                        return
                    else:
                        cur = cur.more
                
    def removeNode(self,data):
        #assign parent and node
        parent = self.root
        node = self.root
        side = 0
        while True:
            #go through tree until data = node.data
            if node == None:#special case node == None
                return None
            if data < node.data:
                parent = node
                side = 0
                node = node.less
            elif data > node.data:
                parent = node
                side = 1
                node = node.more
            else:
                break
        
        if node.more == None and node.less == None:#if node is leaf
            if side == 0:
                parent.less = None
            else:
                parent.more = None
        elif node.more == None and node.less != None: #only has a less child
            node.data = node.less.data
            node.less = None
        elif node.less == None and node.more != None: #only has a more child
            node.data = node.more.data
            node.more = None
        else:
            #has two children
            inorderSuccessor = node.more
            while True:
                #go down right subtree
                if inorderSuccessor.less == None:
                    break
                else:
                    inorderSuccessor = inorderSuccessor.less
            node.data = inorderSuccessor.data
            self.removeNode(inorderSuccessor.data)
                    
    
    def search(self, data):
        
        if self.root==None:#root not set
            return False
        elif self.root.data == data:#root is the same as data
            return True
        else:
            cur = self.root
            while True:
                if cur == None:
                    return False
                #go through tree keep reassigning current value until data is found
                if data < cur.data:
                    cur = cur.less
                elif data > cur.data:
                    cur = cur.more
                else:
                    return True
    def findNode(self, data):
        cur = self.root
        while True:
            if cur == None:
                return None
            #go through tree and keep reassigning current value until data is found
            if data < cur.data: #go to left of tree
                cur = cur.less
            elif data > cur.data: #go to the right of the tree
                cur = cur.more
            else:
                return cur
            
    def tolist(self):
        ret = [] #keep track of sorted array
        
        def inOrder(node, ret):
            if node==None:
                return
            #recursion, to find values in the middle
            inOrder(node.less, ret)
            ret.append(node.data)
            inOrder(node.more, ret)
        inOrder(self.root, ret)
        return ret
            
    def height(self,data):
        #calculate height of child 1
        node = self.findNode(data)
        
        #recursive function
        def traverse(node):
            if node == None:
                #leaf node
                return 0
            else:
                #incrememnt with 1 until the leaf node is reached
                return 1 + max(traverse(node.less), traverse(node.more))
        return traverse(node)
    
    def balancefactor(self,data):
        
        #assign node to data
        node = self.findNode(data)
        
        
        if node == None:
            return 0
        

        if node.less == None:
            x = 0 #makes part of equation 0 if node.less does not exist
        else:
            x = node.less.data
            
        if node.more == None:
            y = 0 #makes part of equation 0 if node.more does exist
        else:
            y = node.more.data
            
        #balance factor is the height of one side minus the height of the other side
        return abs(self.height(x)-self.height(y))
    
    #Time complexity: O(n), where n is the depth of the search tree
