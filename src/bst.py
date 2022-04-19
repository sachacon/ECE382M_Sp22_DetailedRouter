class ITNode:
    def __init__(self, low, high):
        self.low = low 
        self.high = high 
        self.max = high 
        self.left = None 
        self.right = None 

def InsertInterval(root, low, high):
    if(root is None):
        return ITNode(low, high)

    temp_l = root.low
    if(low < temp_l):
        root.left = InsertInterval(root.left, low, high)
    else:
        root.right = InsertInterval(root.right, low, high)

    if(root.max < high):
        root.max = high 
    return root 

def doOverlap(low1, high1, low2, high2):
    if(low1 <= high2 and low2 <= high1):
        return True
    return False 

# Return True if overlap found, False otherwise 
def OverlapSearch(root, low, high):
    if(root == None):
        return None
  
    if(doOverlap(root.low, root.high, low, high)):
        return True 

    if(root.left != None and root.left.max >= low):
        return OverlapSearch(root.left, low, high)

    return OverlapSearch(root.right, low, high) 

def Inorder(root):
    if(root == None):
        return 
    Inorder(root.left)
    print("[", root.low, ", ", root.high, "]", " max = ", root.max)
    Inorder(root.right)
    return


class Node: 
    def __init__(self, data):
        self.data = data 
        self.left = None 
        self.right = None 

    def insert(self,data):
        if self.data:
            if data < self.data: 
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            else:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data 

    def findval(self, val) -> bool:
        if val < self.data: 
            if self.left is None:
                return False
            return self.left.findval(val)
        elif val > self.data:
            if self.right is None:
                return False
            return self.right.findval(val)
        else:
            return True 


class Height: 
    def __init__(self):
        self.height = 0 

def isBSTbalanced(root, height) -> bool:
    left_height = Height()
    right_height = Height()

    if root is None: 
        return True 

    l = isBSTbalanced(root.left, left_height)
    r = isBSTbalanced(root.right, right_height)

    height.height = max(left_height.height, right_height.height) + 1

    if(abs(left_height.height - right_height.height) <= 1):
        return l and r 

    return False 

def main():
    print("Testing Interval BST")
    intervals = [(15,20), (10,30), (17,19), (5,20), (12,15), (30,40)]
   
    root = None  
    for i in range(len(intervals)):
        root = InsertInterval(root, intervals[i][0], intervals[i][1])

    Inorder(root)

    return 

if __name__ == "__main__":
    main()
