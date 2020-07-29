import urllib.request
from html.parser import HTMLParser
from urllib.error import URLError, HTTPError
import string
import os
from urllib.parse import urlparse

#defines a global variable for all links found in a page
allLinks = []
#string containing all vaild chars for a file name, used for title sanatization
valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

#defines a parser class as a child of HTMLParser to search for the 'a' tag to find links
class MyHTMLParser(HTMLParser):
    def __init__(self):
        #adds a variable for the title of the doc and a flag to record the data after a tag
        self.title = None
        self.rec = False
        HTMLParser.__init__(self)

    #method for what to do when the parser encounters a starting tag
    def handle_starttag(self, tag, attrs):
        #checks to see if that tag is a 'a' tag for links
        if tag == 'a':
            #creates a dictionary from that tag
            attr = dict(attrs)
            #adds the new dict to the global list
            allLinks.append(attr)
        elif tag == 'title':
            #if the tag is set to true set the rec flag to true
            self.rec = True

    def handle_data(self, data):
        if self.rec:
            #if rec = true save the data found as the title
            self.title = data

    def handle_endtag(self, tag):
        if tag == 'title':
            #if the closing tag is a 'title' tag, set rec to false so title isn't overwritten
            self.rec = False

def getResultLinks(url):
    #creates a request for that url
    req = urllib.request.Request(url)

    #**********TO EDIT********** -- maybe a better solution than throwing the error
    #especially error 403?
    #handles errors with the url
    try:
        #stores the response of that request
        response = urllib.request.urlopen(req)
    except HTTPError as e:
        #throws HTTP errors
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
    except URLError as e:
        #throws URL errors
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
    else:
        #the response is saved as bytes so it needs to be decoded. So we decode it using utf8, to store as a string to parse
        html = response.read().decode("utf8")
        #creates a MyHTMLParser object called parser
        parser = MyHTMLParser()
        #feeds the html string to the parser
        parser.feed(html)

        #defines a list of links to return
        links = []

        #checks all links added to allLinks from when parser.feed(html) is called
        for link in allLinks:
            #checks for keywords such as yahoo, tumblr and # as they're unneeded links on every yahoo page, not needed for the crawler, also makes sure the each dict has an href
            if "href" in link.keys():
                if "yahoo" not in link['href'] and "tumblr" not in link['href'] and "#" not in link['href']:
                    #adds the link to the list to return
                    links.append(link["href"])

        return links

#saves the found webpages as a txt file containing the html
def saveFiles(links, folder):
    c = 0
    #**********TO EDIT********** -- saves all links, potentially limit it to 10?
    #-- also potentially check file size or length to make sure each page has enough info?
    for link in links:
        #creates a request for that url
        req = urllib.request.Request(link)
        #**********TO EDIT********** -- maybe a better solution than throwing the error
        #especially error 403?
        #handles errors with the url
        try:
            #stores the response of that request
            response = urllib.request.urlopen(req)
        except HTTPError as e:
            #throws HTTP errors
            print('The server couldn\'t fulfill the request.')
            print('Error code: ', e.code)
        except URLError as e:
            #throws URL errors
            print('We failed to reach a server.')
            print('Reason: ', e.reason)
        else:
            #the response is saved as bytes so it needs to be decoded. So we decode it using utf8, to store as a string to parse
            html = response.read().decode("utf8")
            #creates a MyHTMLParser object called parser
            parser = MyHTMLParser()
            #feeds the html string to the parser
            parser.feed(html)
            #if the article has a title
            if parser.title != None:
                #converts the title of the page to a valid filename
                title = "".join(c for c in parser.title if c in valid_chars)
                #gets the directory of the pyhton file being run
                here = os.path.dirname(os.path.realpath(__file__))
                #sets up the directory for the dataset
                dir = os.path.join(here,"Dataset")
                #if there isn't already a subdirectory called Dataset in the same directory as the python file
                if not os.path.exists(dir):
                    #make a new direcotry
                    os.makedirs(dir)
                #same as above but for the dataset subdirecories based on keywords
                subDir = os.path.join(here,dir,folder)
                if not os.path.exists(subDir):
                    os.makedirs(subDir)
                #sets up the file path to save the files
                filepath = os.path.join(here,dir,subDir,title+".txt")
                #saves the html file from the url with the title grabed and sanatized above to the filepath specified above
                urllib.request.urlretrieve(link,filepath)
                c = c + 1
                if c >= 30:
                    return

def main():
    #defines a list of out keywords, words are seperated by '+'s as yahoo follows this format
    keywords = ["self+driving+cars", "quantum+computing", "evil+robots"]
    #defines a master url for yahoo search that we can append out keywords to, so we can get a page with results for each keyword
    masterUrl = "https://ca.search.yahoo.com/search?p="
    #loops through each keyword
    for word in keywords:
        #header for what its about to print
        print("getting files for: " + word)
        links = getResultLinks(masterUrl+word)
        #print(links)
        #clears allLinks, so that links from the previous keyword aren't inluded in the next set
        allLinks.clear
        #runs the save files method to save the html files found at each link
        saveFiles(links,word)

#runs the main method
if __name__ == "__main__":
    main()

