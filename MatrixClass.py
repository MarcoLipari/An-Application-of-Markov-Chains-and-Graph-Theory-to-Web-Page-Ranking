class Matrix(list):
    """Take a list of lists and turn it into a matrix object.
    The matrix object  has method size that returns a tuple (rows, columns).
    The matrix object  has method steadystate that returns the steady state of the matrix.
    The matrix object  has method test that returns True if the matrix is a valid stochastic transition matrix and False otherwise.
    """
    
    
    def size(self):
        '''Returns the size of the matrix as a tuple (rows, columns)'''
        return len(self), len(self[0])

    def transpose(self):
        '''Transposes the matrix'''
        return Matrix([list(row) for row in zip(*self)]) #transposes the matrix
    
    def __mul__(self, other):
        '''Matrix multiplication'''

        if not isinstance(other, Matrix):
            raise TypeError('Matrix multiplication is only defined for two matrices')
        if self.size()[1] != other.size()[0]:
            raise ValueError('Matrix dimensions do not match')
        
        return Matrix([[sum(a*b for a,b in zip(row,col)) for col in zip(*other)] for row in self])
    
    def __pow__(self, n):
        '''Matrix power'''
        if n == 0: #identity matrix
            return Matrix([[1 if i == j else 0 for j in range(self.size()[0])] for i in range(self.size()[1])])
        elif n == 1: #matrix itself
            return self
        else: #recursive calculation
            return self * self**(n-1)

    def stochastictest(self):
        '''Returns True if the matrix is a valid stochastic transition matrix and False otherwise'''
        column_sums = [sum(col) for col in zip(*self)] #creates list of column sums
        return all(abs(s - 1.0) < 1e-9 for s in column_sums) # checks if all column sums are close to 1 or zero
     
    def steadystate(self, tolerance = 1e-6, maxpower=1000): 
        '''Returns the steady state of the matrix ursing power iteration method. The power parameter is the number of iterations. The tolerance parameter is the stopping criterion.'''
        if not self.stochastictest():
            raise ValueError('Matrix is not a valid stochastic transition matrix')
        if self.size()[0] != self.size()[1]:
            raise ValueError('Matrix is not square')

        def l1_norm(v1, v2):
            '''Returns the manhattan norm of two vectors'''
            
            # Transpose because its easier to take the row sums
            v1T = v1.transpose() # v1 transposed
            v2T = v2.transpose() # v2 transposed
            v1norm = 0 # Initialize norm of v1
            v2norm = 0 # Initialize norm of v2
            for i in range(len(v1T[0])):
                v1norm += abs(v1T[0][i]) # Sum of absolute value of every component in v1
                v2norm += abs(v2T[0][i]) # Sum of absolute value of every component in v1

            return abs(v1norm - v2norm)
        
        n = self.size()[0] # Number of rows/columns in transition matrix

        #Creates v as a uniform distribution column vector
        v = [1/n]*n # initial guess
        v = Matrix([v])
        v = v.transpose() # convert to column vector

        # Power iteration method for computing steady state vector
        for _ in range(maxpower): 

            v_next = self*v
            #Check for convergence
            l1 = l1_norm(v, v_next)
            if l1 < n * tolerance: # Scale the tolerence to according to number of compenents
                return v_next

            v = v_next

        return v
    
    def __repr__(self):
        '''Returns a formatted string representation of the matrix with aligned columns and numbered rows/columns.'''
        col_widths = [max(len(f"{num:.4f}") for num in col) for col in zip(*self)]  # Find max width per column
        col_headers = "    " + "  ".join(f"{i}".rjust(col_widths[i]) for i in range(len(self[0])))  # Column numbers

        rows = [f"{i} [" + "  ".join(f"{num:.4f}".rjust(col_widths[j]) for j, num in enumerate(row)) + "]" 
                for i, row in enumerate(self)]  # Row numbers

        return col_headers + "\n" + "\n".join(rows)

        
    
#TEST CODE
if __name__ == '__main__':
    m = Matrix([[1, 0.5], [0, 0.5]])
    n = Matrix([[1, 0], [0, 1]])
    p = Matrix([[0.8, 0.2, 0.0], [0.2, 0.5, 0.2], [0.0, 0.3, 0.8]])
    M = Matrix([
    [0, 0.5, 0.5],
    [1, 0.5, 0.5],
    [0, 0, 0]
    ])
    print(m)
    print(m.size())
    print(m.stochastictest())
    m.transpose()
    print(m)
    m.transpose()
    print(m)
    print("mxn:","\n"+str(m*n))
    print(M.steadystate())
    assert m*m == m**2
    assert m*m*m == m**3

    p = Matrix([[0.8, 0.2, 0.0], [0.2, 0.5, 0.2], [0.0, 0.3, 0.8]])
    print("Test Case 3: 3x3 Transition Matrix")
    print(p)
    print("Size of p:", p.size())
    print("Is p a valid stochastic matrix?", p.stochastictest())
    print("Steady state of p:")
    print(p.steadystate())
    print("\n")

    
