#!/bin/env python2.7
#author: treint
#given a list of item urls, returns the item values as txt
#will require modules to be imported first before running

from bs4 import BeautifulSoup
import cookielib
import urllib2
import mechanize

#disgusting mess
class User(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        #browser setup??
        self.br = mechanize.Browser() # this will be used as our browser, and will help automate forms
        self.br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.2.8) Gecko/20100722 Firefox/3.6.8 GTB7.1 (.NET CLR 3.5.30729)')]
        self.cookies = cookielib.LWPCookieJar() #finish building our browser, and cookies 
        self.br.open("http://www.gaiaonline.com/")
        self.br.set_handle_robots(False)

        self.br.select_form(nr=0)
        self.br["username"] = self.username
        self.br["password"] = self.password
        self.br.submit()
        
        self.login = self.br.response().get_data()

        if "Logout" in self.login:
            print "User successfully logged in"

    def itemSearch(self, url, file):
        #MP search
        search = self.br.open(url).read()
        
        soup = BeautifulSoup(search, "lxml")
        soup.encode('utf-8')

        #grabbing item name
        name = soup.find("h2", {"id": "vend_item_title"}).get_text(strip=True)
        name = name.replace('\\n'," ").encode("utf-8")

        #grabbing item value
        price = soup.find("strong", string="Average Buy Price:")
        value = price.next_sibling.encode()

        #write to file
        file.write(name + " " + value)

if __name__ == '__main__':
    bot = User(<USERNAME>,<PASSWORD>) #replace with your own credentials here
    itemFile = open('itemValues.txt', 'w+')

    count = 0

    with open('itemUrls.txt') as f:
        url = f.readline()
        while url:
            bot.itemSearch(url, itemFile)
            url = f.readline()

    itemFile.close()