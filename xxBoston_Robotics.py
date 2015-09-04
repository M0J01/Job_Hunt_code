'''
#It appears that the links on Indeed us either /rc or /cmp as links to jobs. Though they are always between 'href=" STUFF RIGHT HERE" target="_blank"'
#It appears that some of the links will not work unless the directing website is Indeed.com directly. I cannot access the sites from a cold URL (aka I cannot go to them directly... Future project is figure out how to go there from indeed first, though some of them do not seem to care, and just do not work...
#7/16/2015 1:34 AM, it apears some HTML tags with TITLE, have <title .....> name </title> in them. I must account for the ....
#7/16/2015 2:57 AM, it appears file.write() will only take in a string value, as such I must convert fromlist to string format first
#7/16/2015 6:02 AM, it may behoove my cause to convert all HTML inbound to lower case... however this would be difficult without downloading another function to facilitate, or some very very long checking functions... as of now I have a patched fix applied (Check for <title, and <TITLE>)... we will see if Patchwerk monster can get the job done.
#7/16/2015 7:22 AM, Keep up.
#7/16/2015 7:38 AM, There are some sites which I recieve an error page when I attempt to download the html data in to an object. So far Apple is one of the big ones.
#7/18/2015 8:00 AM, Added Mechanize Support, functional for the moment. I believe "AJAX" websites are causing some problems... Will need to investigate what AJAX is. 
'''

import webbrowser	#Used for opening pages in a webbrowser
import urllib		#used for reading webpages
import re			#Used for parsing data
import mechanize	#Used for faking browser
import cookielib	#Used for populating fake browser with cookies


#Pass in: a url, 
#Returns: an object containing the text of that URL
def get_webpage(url):
	
	br = mechanize.Browser()				#used to emulate browser
	cj = cookielib.LWPCookieJar()			#used to emulate cookies
	br.set_cookiejar(cj)					#sets the cookies to active?
		
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)		#I think it refreshes the page if there is no result returned
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]	#This specifies what type or brwoser we will be emulating

	br.set_handle_equiv(True)			#use handling procedure when ...
	br.set_handle_redirect(True)		#Use hadnling procedure when redirected
	br.set_handle_referer(True)			#use handling procedure when it asks for a referer
	br.set_handle_robots(False)			#use handling procedure when there is a robots.txt
	#br.set_handle_gzip(True)
	
	try:						#Try reading the website
		r = br.open(url)
		htmltextz = r.read()
	except:						#if not, put it in the unreadable section
		unreadable.append(url)
		htmltextz = '0'
	
	return htmltextz
	
#Pass in: pattern outside of links and a text/object/file containing data to search
#Returns: all instances of recognized pattern
def get_target_data(patern, filez):
	patternz = re.compile(patern)
	links = re.findall(patternz,filez)
	return links

#Pass in: A list of links of link to open in a web-browser, a root webpage to concatenate the links to
#Returns: Null, though it will open some web pages!
#Not used ATM
def go_to_sites(linkz,rootz):
	for link in linkz:
		link = rootz+link
		webbrowser.open(url_destinationz);
	return

#Pass in: link list and root to append list to
#Returns: Index full of visit-able sites	
def make_full_link(linkz,rootz):
	i = 0
	url_destination=[]
	while i < len(linkz):
		url_destination.append(rootz + linkz[i])
		i+=1
	return url_destination

#Pass in: an index to store site data, and links to get data from
#Returns: an index where index[i][0]=sitelink, [i][1]=htmlinfo
def fill_index(indexz,full_linkz):
	i = 0
	indexz = []
	temp = [] 
	
	while i < len(full_linkz):
		temp = []
		temp.append(full_linkz[i])
		temp.append(get_webpage(full_linkz[i]))
		indexz.append(temp)
		i+=1
	return indexz	

#Pass in: an index with index[i][0]=sitelink, [i][1]=htmlinfo
#Returns: an index where index[i][2]=job_name			##Based on extracted info
def get_name(indexz):

	i = 0
	while i < len(indexz):
		title = get_target_data(name_style,indexz[i][1])
		if title:
			title = str(title)
			indexz[i].append(title)	
		else:
			start = indexz[i][1].find("<title>")
			end = indexz[i][1].find("</title>",start)
			if start == -1:
				start = indexz[i][1].find("<TITLE>")
				end = indexz[i][1].find("</TITLE>",start)
				if start == -1:
					start = indexz[i][1].find("<h1>")
					end = indexz[i][1].find("</h1>",start)
					title = indexz[i][1][start+4:end]
				else:
					title = indexz[i][1][start + 7 : end]
			else:
				title = indexz[i][1][start + 7:end]
			
			title = title.split()
			title = ''.join(title)
			#title = "['" + title + "']"
			indexz[i].append(title)
			
		i+=1
	return indexz

#Pass in: Keyword list , and an index where index[i][0]=sitelink, [i][1]=htmlinfo, [i][2]=job_name
#Returns: an index with index[i][3]=Rating Count      	## Rating Count based on Keyword matching
def rating_count(indexz,keywordz,dQz):
	
	dQindex = []
	
	i = 0 
	while i < len(indexz):

		dQ_count = 0
		dQ_limit = 0	
		ranks = 0
		count = 0
		
		while ranks < len(keywordz):
		
			word = 1
			multiplier = keywordz[ranks][0]		#print multiplier, '<< This is the multiplier \n'	
			while word < len(keywordz[ranks]):
			
				match = re.findall(keywordz[ranks][word],indexz[i][1])		#print len(match), ' :: ', multiplier
				count += int(len(match))*int(multiplier)
				word+=1
			
			ranks+=1	
			
		for items in dQz:
			dQ_Count = 0
			dQ_limit = items[0]
			dQ_Penatly = items[1]
			for word in items[2]:
				#for word in words:
				#print word
				matched = re.findall(word, indexz[i][1])
				dQ_Count += len(matched)
			if dQ_Count >= dQ_limit:
				print "DQ'ed"
				count += -1*dQ_Penatly
				print items[2]
				tempster = indexz[i]
				dQindex.append(tempster)
				tempster = []
				print indexz[i][2], indexz[i][0]
				
		indexz[i].append(count)
		i+=1
	return indexz, dQindex

#Pass in: an Unsorted Index
#Returns: an Sorted Index
def sort_index(indy):
	
	tempy = []			#temporary list to store new sorted elements in
	loco_sto = []		#tracks the location of the already sorted elements
	
	c = 0				#keeps track of # of elements sorted
	i = 1				#keeps track of current elements sorted
	
	max = -1				#keeps track of local max values for run through
	loco = 0			#local location element position
	
	while c < len(indy):
		while i < len(indy):
			if i not in loco_sto:
				if indy[i][3] > max:
					max = indy[i][3]
					loco = i
			i+=1
		
		tempy.append(indy[loco])
		loco_sto.append(loco)

		max = -1
		i = 0
		c+=1
	
	return tempy
	
#Define your base page here
url_base ="http://www.indeed.com/jobs?q=Robotics&l=Boston%2C+MA"	#Boston Base
'''
url_base = "http://www.indeed.com/jobs?q=Robotics&l=NYC%2C+NY"		#NewYork Base
url_base = "http://www.indeed.com/jobs?q=Robotics&l=California"	#California Base
url_base = "http://www.indeed.com/jobs?q=Lab&l=Richmond%2C+VA"		#***Ethans Base
'''


#Define your root page to add web address to
#and files to write to.
root = "http://indeed.com"
write_text_page = open("00_BA_Robotics.txt","w")
write_dQ_page = open("00_BA_Robotics_DQ.txt","w")
write_unreadable_page = open("00_BA_Robotics_UnRead.txt","w")

#Define your patterns to look for
link_style = 'href="(.+?)" target="_blank"'
name_style = '<title[^.]*>(.+?)</title>'

#Initialize our list containers
index = []
keyword_list = []
dQ_list = []
unreadable = []

#Regular Expression to allow for processing of correct C
rank1 = [10,' c,',' C,',' c ', ' C ', ' c.' ' C.','c\+\+','C\+\+', 'control', 'Control', 'controls','Controls','entry','Entry','matlab','Matlab','python','Python','lua','Lua','microcontroller','Microcontroller','microcontrollers','Microcontrollers','robots', 'Robots','robotic', 'Robotic', 'robotics','Robotics','hardware','Hardware','prototyping','Prototyping','prototype','Prototype', 'prototypes', 'Prototypes', 'PLC', 'PLCs', 'PLCS']
rank2 = [10, 'electrical engineer', 'Electrical Engineer', 'ELECTRICAL ENGINEER', 'Electrical engineer']
rank3 = [50, 'new graduate', 'New graduate', 'New Graduate', 'new Graduate', 'NEW GRADUATE']
rank4 = [100, 'Entry', 'entry', 'ENTRY']
keyword_list.append(rank1)
keyword_list.append(rank2)
keyword_list.append(rank3)
keyword_list.append(rank4)


#Define your DQ List here
'''
#Make everything Lower Case --Look in to multithreading --getting rid of <Styles and such can increase speed
#Intro to NLP
#Computational Linguistics MAsters Degree David
'''
dQ1 = [3, 10000, ['Nurse', 'nurse', 'NURSE']]
dQ2 = [10, 100, ['Senior', 'SENIOR', 'senior']]
dQ3 = [10, 100, ['health','Health','HEALTH']]
dQ4 = [4, 1000, ['oncology','Oncology','ONCOLOGY', 'physician', 'Physician', 'PHYSICIAN']]
dQ5 = [1, 1000, ['5+', '6+', '7+', '8+', '9+', '10+', '5 years']]
dQ6 = [1, 1000, ['assist in surgery']]
dQ7 = [1, 10000, ['Chuck E. Cheese']]	
dQ8 = [1, 100, ['4+']]
dQ_list.append(dQ1)
dQ_list.append(dQ2)
dQ_list.append(dQ3) #It is not even added...
dQ_list.append(dQ4)
dQ_list.append(dQ5)
dQ_list.append(dQ6)
dQ_list.append(dQ7)
dQ_list.append(dQ8)



#Now we start
first = 0
url_end = 0
while url_end <= 300:
	temp_index = []
	if first == 1:
		url_start = url_base+'&start=' + str(url_end)
	else:
		first = 1
		url_start = url_base
	urlfile = get_webpage(url_start)
	links = get_target_data(link_style,urlfile)
	full_links = make_full_link(links,root)
	temp_index = fill_index(temp_index, full_links)
	temp_index = get_name(temp_index)
	temp_index, dQQ = rating_count(temp_index,keyword_list,dQ_list)

	for a in temp_index:
		index.append(a)		
	print url_start
	url_end += 10

		# write_text_page.write(str(a[3]) + ' : ' + a[2] + ' : ' + a[0])		##a[3] is type int, so needs to be forced str()
		# write_text_page.write('\n')
	
	
index = sort_index(index)
print index[1][3]
	
for a in index:
	write_text_page.write(str(a[3]) + ' : ' + a[2] + ' : ' + a[0])		##a[3] is type int, so needs to be forced str()
	write_text_page.write('\n')
for b in dQQ:
	write_dQ_page.write(str(b[3]) + ' : ' + b[2] + ' : ' + b[0])
	write_dQ_page.write('\n')
print len(dQQ)	 
	 
	 # for link in links:
	# print link
	# url = "http://www.indeed.com" + symbolslist[i] 
	# htmlfile = urllib.urlopen(url)
	# htmltext = htmlfile.read()
	# regex = '<span id="yfs_l84_' + symbolslist[i] + '">(.+?)</span>'		
	# pattern = re.compile(regex)
	# price = re.findall(pattern,htmltext)
	# print "price of ", symbolslist[i], "is ",price 
	# i+=1
# #while i < len(urls):
# #	htmlfile = urllib.urlopen(urls[i])
# #	htmltext = htmlfile.read()
# #	titles = re.findall(pattern,htmltext)
	
# #	print titles
# #	i+=1

	
	
	
	# new=2

# url="http://google.com";

# webbrowser.open(url,new=new);

