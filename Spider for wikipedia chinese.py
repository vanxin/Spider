#!/usr/bin/env python
# -*- coding: GBK -*-
import re
import urllib
import md5
from sgmllib import SGMLParser
from collections import deque
from urllib import unquote

p = re.compile('/wiki/[%A-Ba-z0-9]')
#p1 = re.compile('^/wiki/Category:')
#pEx = re.compile('.*[:#].*')


class URLLister(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.urls = []
        
    def start_a(self, attrs):
        href = [v for k, v in attrs if k == 'href']
        if href:
            self.urls.extend(href)  
            
mypath = r'http://zh.wikipedia.org'
q = deque(['/wiki/%e7%ae%97%e6%b3%95', '/wiki/%e6%95%b0%e6%8d%ae%e7%bb%93%e6%9e%84', '/wiki/%e7%bc%96%e8%af%91%e5%99%a8', '/wiki/%e8%ae%a1%e7%ae%97%e6%9c%ba', '/wiki/%e5%9b%be%e7%81%b5%e6%9c%ba'])

def search(name):
    url = mypath + name
    print ("Search: " + url)
    sock = urllib.urlopen(url)
    htmlSource = sock.read()
    sock.close()

    first_name = unquote(name[6:]).decode('utf8')
    
    f = file(first_name, 'w')
    f.write(htmlSource)
    f.close()
    parser = URLLister()
    parser.feed(htmlSource)


    
    for urlx in parser.urls:
        if p.match(urlx):
        #if ((not pEx.match(urlx)) and p.match(urlx)) or p1.match(urlx):
            q.append(urlx)
            print ("push: " + urlx)
            myurl = mypath + urlx
            print ("get: " + myurl)
            sock2 = urllib.urlopen(myurl)
            html2 = sock2.read()
            sock2.close()

            temp = urlx[6:]
            decod = unquote(temp).decode('utf8')
            
            #保存到文件
            name = md5.new(urlx[6:]).hexdigest()
            print ("save as: " + decod)
            f2 = file(decod, 'w')
            f2.write(html2)
            f2.close()



#print parser.urls

while len(q) > 0:
    name = q.popleft()
    #print name
    search(name)
    

