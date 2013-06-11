'''

     MarketCancer.py
	 
	Post messages on a Yahoo! Finance message board
	automatically.
	
	Example Usage:
	
		$ python marketcancer.py username@yahoo.com password1234 GOOG "topics.txt" 1 5
			-post under username@yahoo.com in the GOOG message board using 
			messages from topics.txt behind a proxy 5 times
		
		$ python marketcancer.py "record.txt" GOOG "topics.txt" 0 8
			-post under usernames found in record.txt in the GOOG message board using 
			messages from topics.txt without proxy 8 times

    Greg Thompson Jr.
        (c) 2013

'''

import os
import sys
import time
import random
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import *
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 

class Cell:
    login_page = "https://login.yahoo.com/config/login?" #default login page
    hitch = 4 #number of seconds to pause on each hitch. A hitch is a pause.
    dr = webdriver.Firefox() #default web driver
    topics = "cancer.txt" #default 
    wait = WebDriverWait(dr,10) #default wait period as the driver loads a page

    def __init__(self, username, password, symbol, topics, proxy_on):
	'''
		CLASS Cell(...)
		
		Description: 
			Create an object usable for logging in, posting, and signing out
			of Yahoo!.
		
		Constructor Parameters:
			- username 	- This is the account username. 
			- password	- This is the account password.
			- symbol 	- This is the market symbol to the stock. ex: GOOG, MJNA 
			- topics 	- This is a file name string. The file holds subject lines and corresponding messages.
			- proxy_on	- Use a proxy? 0 for no; any number > 0 for yes
		
	'''
        self.username = username
        self.password = password
        self.proxy_on = proxy_on
        self.symbol = symbol
        self.topics = topics
        self.proxy = "89.160.116.194:443" #default proxy value
        self.p = Proxy({'proxyType': ProxyType.MANUAL,
              'httpProxy': self.proxy,
              'ftpProxy': self.proxy,
              'sslProxy': self.proxy,
              'noProxy': ''
          })

    def create_driver(self):
	'''
		Name: create_driver()
		
		Description: 
			Create the web driver used 
		
		Parameters:
			None.
		
			Returns web driver.
	'''
        if self.proxy_on == 1:
            self.dr = webdriver.Firefox(proxy=self.p)
        else:
            self.dr = webdriver.Firefox()
        return self.dr

    
    def login(self):
	'''
		Name: login()
		
		Description: 
			Login using the login credentials.
		
		Parameters:
			None.
		
			No return value.
	'''
        print "Logging in as '" + self.username + "' with password '" + self.password + "'..."
        #get login page
        self.dr.get(self.login_page)

        #get elements
        user_elem = WebDriverWait(self.dr, 10).until(EC.presence_of_element_located((By.NAME, "login")))
        pass_elem = WebDriverWait(self.dr, 10).until(EC.presence_of_element_located((By.NAME, "passwd")))

        #send credentials
        user_elem.send_keys(self.username)
        pass_elem.send_keys(self.password)
        pass_elem.send_keys(Keys.RETURN)
        
        #Handle contact alternative reminder. Pops up every once in a while upon log in.
        if self.dr.title == "Account Information":
            self.dr.find_element_by_link_text("Remind me later").click()
            print "Successfully beat the contact reminder. Continuing..."
        else:
            print "No contact reminder. Continuing..."

        print "Successfully logged in."
        hitch(self.hitch) #wait after login
    
    #open login page
    def open_login(self):
	'''
		Name: open_login()
		
		Description: 
			Load the Yahoo! login page.
		
		Parameters:
			None.
		
			No return value.
	'''
        self.dr.get(self.login_page)

    #sign out
    def signout(self):
	'''
		Name: signout()
		
		Description: 
			Log/sign out of the currently-logged-in Yahoo! account.
		
		parameters:
			None.
		
			No return value.
	'''
        if self.dr.title == "Sign in to Yahoo!":
            self.dr.find_element_by_link_text("Sign Out").click()
        else:
            menu_elem = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".yucs-menu-access.sp.yuhead-bullet-down")))
            menu_elem.click()
            
            snout_elem = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Sign Out")))
            snout_elem.click()
        print "Successfully logged out."

    #exit web driver
    def close_driver(self):
	'''
		Name: close_driver()
		
		Description: 
			Closes the driver. 
		
		parameters:
			None.
		
			No return value.
	'''
        self.dr.close()

    def access_msg_board(self):
	'''
		Name: access_msg_board
		
		Description: 
			Load the message board in the web driver.
		
		Parameters:
			None.
		
			No return value.
	'''
		#use the specified symbol to create the message board link
        msg_board_page = "http://finance.yahoo.com/mb/" + self.symbol + "/"

        print "Accessing the " + self.symbol + " message board..."
        try:
            self.dr.get(msg_board_page)
            print "Successfully reached " + self.symbol + " message board."
            hitch(self.hitch) #wait .5 seconds
        except:
            self.dr.close()
            print "[!] We've got a problem. Check the symbol you've specified."
            exit()


    def metastasis(self):
	'''
		Name: metastasis()
		
		Description: 
			Post on the message board.  After the post, load the message board
			main page again.
		
		Parameters:
			None.
		
			No return value.
	'''

        #access the message board page
        self.access_msg_board()

        #send dummy subject line and message
        try:
            print "Clicking 'New topic.'"
            newtopic_elem = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "New Topic")))
            newtopic_elem.click()

            #assimilate subject and message text fields
            print "Conjuring post with dummy data..."
            subject_elem = self.wait.until(EC.presence_of_element_located((By.NAME, "subject")))
            message_elem = self.wait.until(EC.presence_of_element_located((By.NAME, "message")))

            #get subject line/topic 
            sub_msg_combo = get_sub_msg(self.topics)

            #fill forms with dummy data
            subject_elem.send_keys(sub_msg_combo[0])
            message_elem.send_keys(sub_msg_combo[1])

            #post
            print "Metastasizing..."
            postmsg_elem = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".yom-button.mb-post")))
            postmsg_elem.click()
            self.access_msg_board()
        except Exception, e:
            logging.exception("Metastasis failed.")
            hitch(self.hitch+10)
            
        logging.debug("Finished")


def multi_login_post(record, symbol, topics, proxy_on, posts):
	'''
		Name: multi_login_post(...)
	
		Description: 
			Logs into each account specified in a login credentials record.
			The record is a CSV file wherein each line is in the format:
						username,password
			After logging in, a post is made using a subject/message pulled
			from the topics file (which is also a CSV) wherein each line is in the 
			format:
						subject,message
			After the post, the account is signed out, and the web driver is 
			directed to the login page so that another account may be logged into
			to repeat the process.
		
		Parameters:
			- record 	- This is is a file name string. The file holds login credentials. 
			- symbol 	- This is the market symbol to the stock. ex: GOOG, MJNA 
			- topics 	- This is a file name string. The file holds subject lines and corresponding messages.
			- proxy_on	- Use a proxy? 0 for no; any number > 0 for yes
			- posts		- How many times should all of the accounts on record be used? This is an integer.
		
			No return value.
	'''

	print "[!] Multiple accounts being used."
	cell_count = 0 #keeps track of the number of logins/posts; they're the same.
	
	#if the user wants to use a proxy, ask them to specify it in the form SERVER:PORT
	if int(proxy_on) > 0:
		proxy_on == raw_input('\n<SERVER:PORT>: ')
		print "\n[!] Operating behind proxy.\n"
	else:
		proxy_on = 0
		print "\n[!] Operating on direct connection.\n"

	for i in xrange(0, int(posts)):
		for login in get_logins(record):
			cancer = Cell(login[0],login[1], symbol, topics, proxy_on)
			cancer.login() #login
			cancer.metastasis() #post
			cancer.signout() #log out
			cancer.open_login() #open login screen
			cell_count+=1 #add to cell count
			print ""
			print 4 * "---"

	print "\n\n\tCell Count: %d cells" % cell_count
	cancer.close_driver()

def single_login_post(username, password, symbol, topics, proxy_on, posts):
	'''
		Name: single_login_post(...)
	
		Description: 
			Logs into one account. The credentials are specified in the function call.
			After logging in, a post is made using a subject/message pulled
			from the topics file (which is also a CSV) wherein each line is in the 
			format:
						subject,message
			After the post, the account is signed out, and the web driver is 
			directed to the login page so that another account may be logged into
			to repeat the process.
		
		Parameters:
			- username 	- This is the account username. 
			- password	- This is the account password.
			- symbol 	- This is the market symbol to the stock. ex: GOOG, MJNA 
			- topics 	- This is a file name string. The file holds subject lines and corresponding messages.
			- proxy_on	- Use a proxy? 0 for no; any number > 0 for yes
			- posts		- How many times should all of the accounts on record be used? This is an integer.
		
			No return value.
	'''
	print "[!] Single account being used."
	keep_posting = True
	cell_count = 0
	
	#if the user wants to use a proxy, ask them to specify it in the form SERVER:PORT
	if int(proxy_on) > 0:
		proxy_on == raw_input('<SERVER:PORT>: ')
		print "\n[!] Operating behind proxy.\n"
	else:
		proxy_on = 0
    
	cancer = Cell(username,password, symbol, topics, proxy_on)
	cancer.login()

	for x in xrange(0, int(posts)):
		cancer.metastasis() #post
		cell_count+=1  
		print "\n\n\tCell Count: %d cells" % cell_count
		print 4 * "---"
	
	cancer.close_driver()

	print "\n[!] Final cell count: %d\n\a" % cell_count

def get_logins(record):
	'''
		Name: get_logins(...)
	
		Description: 
			Login credentials are pulled from the credentials record file (a CSV file) wherein each line is 
			in the format:
						username,password
		
		Parameters:
			- record 	- Record file name. ex: "record.txt"
		
			Returns usernames and passwords in groups in the list form of [[username,password], [username,password], ...].
				Therefore, accessing the username and password yielded is as such:
						get_logins("records.txt")[random_number][0] #for random username
						get_logins("records.txt")[random_number][1] #for random password
	'''
	
	logins = []
	with open(record) as f:
		for line in f.readlines():
			logins.append( (line.rstrip('\n').split(',')) )
	return logins

def get_sub_msg(info_file):
	'''
		Name: get_sub_msg(...)
	
		Description: 
			Subject lines and their corresponding messages are pulled 
			from the topics file (a CSV file) wherein each line is in the format:
						subject,message
		
		Parameters:
			- info_file 	- Topics file name. ex: "record.txt"
		
			Returns a random subject line and corresponding message in the form of a list.
				Therefore, to access the yielded subject and message:
						get_sub_msg("topics.txt")[0] #for the subject line
						get_sub_msg("topics.txt")[1] #for the message
	'''
	sub_msg = []
  
	with open(info_file) as f:
		for line in f.readlines():
			sub_msg.append(line.rstrip('\n').split('\n'))
    
	num = random.randint(0, len(sub_msg)-1 ) #random number for random messages

	return sub_msg[num][0].split(',')

def hitch(seconds):
	'''
		Name: hitch(...)
	
		Description: 
			Pause for a moment (in seconds). Sometimes, this is useful because
			simulation of a user's actions may require varied
			pauses. 
		
		Parameters:
			- seconds 	- number of seconds to pause (float or int)
		
			No return value.
	'''
	time.sleep(seconds)

def intro():
	'''
		Name: intro(...)
	
		Description: 
			Prints an introductory message (somewhat of a splash).
		
		Parameters:
			None.
		
			No return value.
	'''
	print "\n\nMarket Cancer v1.0.0\n\n\tGreg Thompson Jr. (c) 2013\n\nTime to infect a board.\n\n" + 8 * "-----"
    
if __name__=="__main__":
    # Test cell.  This is for testing purposes only.
    #   Logs in, posts on the message board, then signs out.
    #
    #cancer = Cell("coolandysavage@yahoo.com","foobar4321", "GOOG", "cancer.txt", 0)
    #cancer.login()
    #cancer.metastasis()
    #cancer.signout()
    #

    #single login
    #  sys.args:
    #   1 - username
    #   2 - password
    #   3 - symbol
    #   4 - topics file
    #   5 - proxy? 0 for no; 1 (or any n > 0) for yes
    #   6 - number of posts
    #
	
	intro()
	
	if (len(sys.argv) == 7):
		single_login_post(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])

    #multiple logins
    #  sys.args:
    #   1 - login credentials filename (credential records)
    #   2 - symbol
    #   3 - topics file
    #   4 - proxy? 0 for no; 1 (or any n > 0) for yes
    #   5 - posts
	elif (len(sys.argv) == 6):
		multi_login_post(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])

    #error
	else:
		print "---\n\nUsage: %s username password symbol \"topics_file_name.txt\" proxy? spreads?\n\n" % os.path.basename(sys.argv[0])
		sys.exit('Usage: %s "record_file_name.txt" symbol "topics_file_name.txt" proxy? spreads?\n\n---\n' 
					% os.path.basename(sys.argv[0]))