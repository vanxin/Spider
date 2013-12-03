#!/usr/bin/env python
# -*- coding: GBK -*-
import re
import urllib
import md5
from sgmllib import SGMLParser
from collections import deque

p = re.compile('^/wiki/')
p1 = re.compile('^/wiki/Category:')
pEx = re.compile('.*[:#].*')


class URLLister(SGMLParser):
    def reset(self):
        SGMLParser.reset(self)
        self.urls = []
        
    def start_a(self, attrs):
        href = [v for k, v in attrs if k == 'href']
        if href:
            self.urls.extend(href)

mypath = r'http://zh.wikipedia.org'
q = deque(['/wiki/算法', '/wiki/数据结构', '/wiki/编译器', '/wiki/计算机', '/wiki/图灵机'])

def search(name):
    url = mypath + name
    print ("Search: " + url)
    sock = urllib.urlopen(url)
    htmlSource = sock.read()
    sock.close()
    #print htmlSource
    f = file('test', 'w')
    f.write(htmlSource)
    f.close()
    parser = URLLister()
    parser.feed(htmlSource)
    for urlx in parser.urls:
        if ((not pEx.match(urlx)) and p.match(urlx)) or p1.match(urlx):
            q.append(urlx)
            print ("push: " + urlx)
            myurl = mypath + urlx
            print ("get: " + myurl)
            sock2 = urllib.urlopen(myurl)
            html2 = sock2.read()
            sock2.close()
            # 保存到文件
            name = md5.new(urlx[6:]).hexdigest()
            print ("save as: " + name)
            f2 = file(name, 'w')
            f2.write(html2)
            f2.close()




#print parser.urls

while len(q) > 0:
    name = q.popleft()
    #print name
    search(name)
    

