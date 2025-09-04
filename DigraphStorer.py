import os
import pickle
import copy
from urllib.parse import urlparse
from WebCrawler import BaseUrlToDigraph
# Reference for pickle: https://docs.python.org/3/library/pickle.html#module-interface
# Reference for urlparse: https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urlparse

def get_saved_filename(url):
    '''Generate a filename based on the URL for saving the digraph.
    The filename is derived from the netloc (network location) part of the URL.'''
    netloc = urlparse(url).netloc
    return f"digraph_saved_{netloc}.pkl"

def get_saved_digraph(url, saved_file=None):
    '''Load a digraph from a saved file or create a new one if it doesn't exist.
    If a saved file is provided, it will be used instead of generating a new filename.'''
    if saved_file is None:
        saved_file = get_saved_filename(url)
    if os.path.exists(saved_file):
        print("Loading saved digraph...")
        with open(saved_file, "rb") as f:
            # Return a deep copy so the originally saved object graph modified
            digraph_data = copy.deepcopy(pickle.load(f))
    else:
        digraph_data = BaseUrlToDigraph(url)
        with open(saved_file, "wb") as f:
            pickle.dump(digraph_data, f)
    return digraph_data

# TEST CODE
if __name__ == "__main__":
    url = "https://www.marianopolis.edu"
    digraph_data = get_saved_digraph(url)
    print(digraph_data)
    
    url = "https://quotes.toscrape.com"
    digraph_data = get_saved_digraph(url)
    print(digraph_data)

    