#! /usr/bin/python
import os
import sys
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import urllib2
import re

def searchr(soup,nowurl):
    metadata = soup.find("a",href="maven-metadata.xml")
    if(metadata):
        msoup = BeautifulStoneSoup(urllib2.urlopen(nowurl+metadata["href"]))
        for elem in msoup.findAll("version"):
            print elem.text
    else:
        aTag = soup.findAll("a",href=re.compile(".*"+sys.argv[1]+".*"))
        if(aTag):
            for attr in aTag:
                hsoup = BeautifulSoup(urllib2.urlopen(nowurl+attr["href"]))
                searchr(hsoup,nowurl+attr["href"])

if __name__ == "__main__":
    _mvnrepourl = "http://repo2.maven.org/maven2/"
    doc = urllib2.urlopen(_mvnrepourl)
    soup = BeautifulSoup(doc)
    searchr(soup,_mvnrepourl)


