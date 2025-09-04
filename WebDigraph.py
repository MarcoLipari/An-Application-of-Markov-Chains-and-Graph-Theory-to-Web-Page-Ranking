#Directed graph class based on Topic 8 slides
from MatrixClass import Matrix


class Digraph(Matrix):
    """Create a directed edge class utilizing an adjacency matrix. Allows for multiple edges)."""
    # A directed edge is an edge that has a direction, meaning it goes from one vertex to another.
    # A directed edge is represented by an ordered pair of vertices (v, w), where v is the starting vertex and w is the ending vertex.
    
    def __init__(self, size):
        '''Creates a matrix with all the nodes but no links. 
        Size is a tuple (number_of_columns, number_of_rows).'''
        self.size = size[0] # matrix is square so nxm = nxn
        matrix = [] # Initialize the matrix
        
        columnlength = size[1]
        for i in range(columnlength):
            row = [0] * (size[0])
            matrix.append(row)
            
        if not matrix: #Avoids bugs coming from initial size = 0
            matrix = [[0,0],[0,0]]


        super().__init__(matrix)

    def addEdge(self, v, w):
        """Adds an edge from v to w. 
        If edge is already created, adds another edge."""
        #Increase matrix size if neccesary
        vsizediff = v - self.size + 1 # size difference compared to v
        
        if vsizediff > 0: 

            for row in self: #Extend rows
                row.extend([0]*vsizediff)
                
            self.size = len(self[0])

            for i in range(vsizediff): #Add columns
                self.append([0]*self.size)

        wsizediff = w - self.size + 1 # size difference compared to v

        if wsizediff > 0:

            for row in self: #Extend rows
                row.extend([0]*wsizediff)
            self.size = len(self[0])

            for i in range(wsizediff):
                self.append([0]*self.size)
                
        self[v][w]+=1    

# TEST CODE
if __name__ == "__main__":
     # Create a DirectedEdge object with a 4x4 matrix.
    # The size parameter is a tuple (number_of_columns, number_of_rows)
    de = Digraph((4, 4))
    
    # Print the initial matrix (all zeros)
    print("Initial matrix:")
    print(de)
    
    # Add some directed edges
    de.addEdge(0, 1)
    de.addEdge(1, 2)
    de.addEdge(2, 3)
    de.addEdge(3, 0)
    de.addEdge(6, 7)
    
    # Print the matrix after adding edges
    print("\nMatrix after adding edges:")
    print(de)

    de = Digraph((0, 0))

    # Add some directed edges
    de.addEdge(0, 1)
    de.addEdge(1, 2)
    de.addEdge(2, 3)
    de.addEdge(3, 0)
    de.addEdge(6, 7)
    
    # Print the matrix after adding edges
    print("\nMatrix after adding edges:")
    print(de)

