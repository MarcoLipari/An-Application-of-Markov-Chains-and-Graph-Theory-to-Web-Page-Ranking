from WebCrawler import BaseUrlToDigraph
from MatrixClass import Matrix
from WebDigraph import Digraph
from DigraphStorer import get_saved_digraph

def DigraphToTransitionMatrix(Directed_graph):
    """Convert a directed graph into a transition matrix."""
    # Digraph is a list of lists, where each sublist represents a row in the matrix
    # and each element in the sublist represents a column in the matrix.
    # The transition matrix is a square matrix where each element represents the probability
    # of moving from one state to another.
    # The sum of each row in the transition matrix should equal 1.
    # The transition matrix is created by normalizing the rows of the directed graph.
    # The normalization is done by dividing each element in the row by the sum of the row.
    # The transition matrix is then returned as a Matrix object.
    # Used to handle dangling nodes: https://www.researchgate.net/publication/321056905_Toward_Efficient_Hub-Less_Real_Time_Personalized_PageRank#pf4 

    def stochasticnormalization(row):
        """Return a list where the sum of all items equals 1."""
        row_sum = sum(row) # Sum of all values in the row
        row_len = len(row) # Number of values in the row
        vi = 1/row_len     # 1 divided by the sum of all values in the row
        for i in range(len(row)):
            row[i] = (row[i]/row_sum) if row_sum != 0 else vi # Handles dangling nodes using S = A + dw

    for row in Directed_graph:

        stochasticnormalization(row)

    transitionmatrix = Directed_graph.transpose() 

    return transitionmatrix

def pagerank(url):
    """ Ranks pages within a web domain using an algorithm based on Google's PageRank.

    Args:
        url (str): Any url of the form https://example.com

    Returns:
        list: list of tuples, [(webpage, corresponding rank)]
    """
    DigraphD = get_saved_digraph(url) # BaseUrlToDigraph(url) 
    digraph = DigraphD[0] # Domains corresponding digraph
    P = DigraphToTransitionMatrix(digraph) # Domains corresponding transition matrix
    P_steadystate = P.steadystate() # Steady state vector of the transition matrix

    D = DigraphD[1] # Domains corresponding {url : position in the matrix} dictionary
    count = 0 # Initialize count of the number of pages
    for i in D:
         D[i] = P_steadystate[count][0] # P_steadystate is a column vector, so we need to get the first element of the column
         count += 1 
    # Now D is a dictionary where the keys are the urls and the values are the pagerank vectors of the urls
    urlsvector = tuple(zip(D.keys(), D.values())) # Creates a list of tuples with the url and the pagerank vector
    urlsvector = sorted(urlsvector, key=lambda x: x[1], reverse=True) # Sorts the list of tuples by the pagerank vector in descending order
    # The list of tuples is sorted in descending order, so the first element is the highest pagerank vector

    return urlsvector

# Main code to run the pagerank function
# This code is used to test the pagerank function and to get user input for the url
if __name__ == '__main__':

    x = True

    while x == True:

        url = input("Which webpage would you like to rank?\n"
            "1: www.marianopolis.edu\n"
            "2: quotes.toscrape.com\n"
            "3: champlainsaintlambert.ca\n"
            "Or enter a any other URL.\n"
            "Enter 0 to exit.\n> ")

        if url == "0":
            x = False

        elif url == "1":
            r = pagerank("https://www.marianopolis.edu")
            count = 0
            for i in r:
                count+=1
                print(count, i[0], i[1])
        elif url == "2":
            r = pagerank("https://quotes.toscrape.com")
            count = 0
            for i in r:
                count+=1
                print(count, i[0], i[1])
        elif url == "3":
            r = pagerank("https://champlainsaintlambert.ca")
            count = 0
            for i in r:
                count+=1
                print(count, i[0], i[1])
        else:
            r = pagerank(url)
            count = 0
            for i in r:
                count+=1
                print(count, i[0], i[1])

