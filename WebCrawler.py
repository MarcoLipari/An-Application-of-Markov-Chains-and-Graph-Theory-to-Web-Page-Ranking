# Based on implementation found on https://www.scrapingdog.com/blog/web-crawling-with-python/ 

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from WebDigraph import Digraph

def BaseUrlToDigraph(base_url):
    """Takes a base url and utilizes breadth first search to create a graph of it's edges.

    Args:
        base_url (str): url

    Returns:
        AdjMatrix, D (tuple) : (Adjacency matrix representention of a digraph. Multiple edges created if there are multiple links., {url : position in adjacency matrix}) 
    """


    # Function to crawl a page and extract links
    def crawl_page(url):
        """Crawl a page and extract links"""
        nonlocal urlcount
        nonlocal D
        countlinksfrompage = 0
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            soup = BeautifulSoup(response.content, "html.parser")

            # Extract links and enqueue new URLs
            links = []
            for link in soup.find_all("a", href=True):
                next_url  = urljoin(url, link["href"])
                next_domain = urlparse(next_url).netloc

                if next_domain != base_domain: #Skip links outside base domain
                    continue 
                
                if not next_url in D:
                    D[next_url] = urlcount
                    urlcount +=1

                AdjMatrix.addEdge(D[url], D[next_url])
                

                links.append(next_url)

            return (links, countlinksfrompage)

        except requests.exceptions.RequestException as e:
            print(f"Error crawling {url}: {e}")
            return []

    visitscount = 0 #Counts how many website visits made
    D = {}  # url : position in adjacency matrix

    # URL of the website to crawl
    
    base_domain = urlparse(base_url).netloc

    # Set to store visited URLs
    visited_urls = set()

    # List to store URLs to visit next
    urls_to_visit = [base_url]

    D[base_url] = 0 # Base url is state 0

    pagenumber = 0  # Counts which page currently at
    urlcount = 1 # Counts how many urls associated with in D

    AdjMatrix = Digraph((0, 0))  # Creates an adjacent matrix that allows for parallel edges

    # Crawl the website
    #for i in range(10):
    while urls_to_visit:

        current_url = urls_to_visit.pop(0)  # Dequeue the first URL
        pagenumber +=1  #Count increase with formation of parent node
        

        if current_url in visited_urls:
            continue

        print(f"Crawling: {current_url}")
        visitscount += 1

        visited_urls.add(current_url)

        pagedata = crawl_page(current_url) # (List of outgoing links, number of outgoing links)
        if pagedata: # If there is an error crawling pagedata is an empty list, so avoids IndexError
            new_links = pagedata[0]
            urls_to_visit.extend(new_links)




    print(pagenumber, "different pages")
    print("Crawling finished.")

    return AdjMatrix, D

#TEST CODE
if __name__ == "__main__":
    x = BaseUrlToDigraph("https://quotes.toscrape.com")
    x = BaseUrlToDigraph("https://www.marianopolis.edu")
    print(x)
