#pip install -r /path/to/requirements.txt
import mechanize
import re
from bs4 import BeautifulSoup
from urllib2 import HTTPError
# from tkinter import *

# master = Tk()
# Label(master, text="First Name").grid(row=0)
# Label(master, text="Last Name").grid(row=1)

# e1 = Entry(master)
# e2 = Entry(master)

# e1.grid(row=0, column=1)
# e2.grid(row=1, column=1)
print 'made it here'

br = mechanize.Browser()
br.set_handle_robots(False)
br.addheaders = [('user-agent', 'Mozilla/5.1 (X11; U; Linux i686; en-US; rv:1.9.2.3) Gecko/20100423 Ubuntu/10.04 (lucid) Firefox/3.6.3'),
('accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')]

#setting debug to True will print headers
br.set_debug_http(False)

#begin compiling a list off all available links to do searching from...
 #15 is not correct :( We need a better way to do this
	# CORRECT WAY is to inspect the original number of results shown. the moment
	# that number is no longer the same we have come across the last page of results and
	# can flag the program to stop and execute the next line of code. 
	# while (number of results is == number of results) print
	# Or we just throw an exception and the rest of the program continues! YAY We'll go this route for now.
	
	### BTW This while loop begins the google search and populates the source_pages Array 
	#with sites we need to visit for contact info.
def startTheShow(): 
	
	#sources of potential contact information
	hard_search_terms =["facebook", "twitter", "email", "e-mail", "linkedin", "linked-in", "telephone", "contact", "Contact", "CONTACT", "Telephone"]

	#if we find another link to search we need to change the url to equal the base url + the new search query link.
	#then we need to execute the function again and push to the same array.
	#afterwards we need to verify that the array contains all of the found results and not just the ones that were pushed last
	source_pages = []	

	#will need to separate this into two parts and encode the search query
	#for now it stays for ease of testing
	baseurl = 'https://www.google.com'
	print "@@@@@Use quotes to do an exact query search."
	query_string = raw_input("What query string would you like to use? ").split(" ")
	exclude_terms = raw_input("Would you like to exclude any terms from your search?(Comma separated)(none to quit) ").split(" ")
	
	#build a search query string
	url = ''	
	if exclude_terms[0] == 'none':
		print 'using if'
		url = baseurl + "/search?q="+("+").join(query_string) 
	elif len(exclude_terms) >= 1 and exclude_terms != "none":
		print 'using elif'
		for i in range(0, len(exclude_terms)):
			url += baseurl + "/search?q=" + ("+").join(query_string) + "+-"+exclude_terms[i];
	else:
		try:
			print 'using else try'
			url = baseurl + "/search?q="+ ("+").join(query_string)
		except:
			print "error setting url: ", url
	
	print "What is url? ", url
	
	tryNextPage = True

	#build a list of urls so we can visit and scrape those pages for contact info.
	while tryNextPage == True:
		text = br.open(url).read()
		soup = BeautifulSoup(text, 'html.parser')		
		test = soup.find_all(attrs={'class':'g'})
		totalResultsFound = soup.find_all(id="resultStats")
		
		#search for Next Page button 
		try:
		
			nextPageLink = soup.find_all('span', string='Next')[0].parent.get('href')
			if nextPageLink:
				query_string = nextPageLink
				url = baseurl + query_string
				print "getting next page..."
			else:
				tryNextPage = False
				print "tryNextPage should now be false: ", tryNextPage
		
		except:

			print "Some error with finding new page link..."
			tryNextPage = False

		print totalResultsFound[0].getText()
		
		for i in range(0, len(test)-1):
			#get the url from the list of links we are presented on a page.
			findSearchableLinks = test[i].find_all('a')[0].get('href').split('&sa')[0].split('q=')[1]
			print findSearchableLinks
			#line.decode('utf-8').strip()
			source_pages += [str(findSearchableLinks)]
	
	#return our results so they may be passed to our inspect pages function in main
	print 'found search pages urls ', source_pages
	return source_pages

def eval_page():
	print 'some awesome function to pull some data from a webpage'

def inspect_pages(linksToSearch):
	print '...execute inspect_pages'
	links_found = []

	#loop through the list of links we found via our search
	for i in range(0, len(linksToSearch)):

		print 'searching', linksToSearch[i]
		try:
			text = br.open(linksToSearch[i]).read()
			soup = BeautifulSoup(text, 'html.parser')

			foundText = soup.find_all(string=["Contact","CONTACT US", "contact us", "Contact Us", "Telephone", "Email", "email", 'telephone', 'e-mail', 'contact', 'CONTACT']);
			links_found.append(foundText);
		except UnicodeDecodeError, e:
			print "UnicodeDecodeError", e
		except HTTPError, e:
			print "Http error code: ", e.code
	if len(links_found) > 0:
		print len(links_found), "links found"
		return links_found
	else:
		print "No links found"

def main():
	usefulLinks = startTheShow()
	listOfUsefulPages = inspect_pages(usefulLinks)
	print listOfUsefulPages

main()