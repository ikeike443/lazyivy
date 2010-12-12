#! /usr/bin/python
import os
import sys
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import urllib2
import re
import optparse

def searchr(soup,nowurl,querystring):
    metadata = soup.find("a",href="maven-metadata.xml")
    if(metadata):
        msoup = BeautifulStoneSoup(urllib2.urlopen(nowurl+metadata["href"]))
        groupid = msoup.find("groupid")
        artifactid = msoup.find("artifactid")
        for elem in msoup.findAll("version"):
            asoup = BeautifulSoup(urllib2.urlopen(nowurl+elem.text+"/"))
            for jarname in asoup.findAll("a",href=re.compile(elem.text+"\.jar$")):
                print "%-25s" % jarname.text,groupid.text+":"+artifactid.text,"   ("+nowurl+elem.text+")"
    else:
        aTag = soup.findAll("a",href=re.compile(".*"+querystring+".*"))
        if(aTag):
            for attr in aTag:
                hsoup = BeautifulSoup(urllib2.urlopen(nowurl+attr["href"]))
                searchr(hsoup,nowurl+attr["href"],querystring)

if __name__ == "__main__":
    #parse args
    parser = optparse.OptionParser()
    parser.add_option('--quick', action="store_true",default=False,dest="quick",help="quick list")
    parser.add_option('-l', action="store",dest="query",help="search artifact")
    parser.add_option('-a', action="store", dest="artifact", help="add dependency tag into ivy.xml")
    parser.add_option('-f', action="store", dest="filename", help="identify file name of ivy.xml")
    parser.add_option('--groupid', action="store", dest="gid", help="restrict target groupid to search")
   
    (options,args) = parser.parse_args() 

    #if no args, print help
    if len(sys.argv) < 2:
        parser.parse_args(["-h",""])       
        sys.exit(0)
    
    if options.query:
        if options.gid:
             gid=options.gid+"/"
        else:
             gid=""
        _mvnrepourl = "http://repo2.maven.org/maven2/"+gid
        try:
            doc = urllib2.urlopen(_mvnrepourl)
        except:
            _mvnrepourl = "http://repo1.maven.org/maven2/"+gid
            doc = urllib2.urlopen(_mvnrepourl)
        soup = BeautifulSoup(doc)
        if(options.quick):
            aTag = soup.findAll("a",href=re.compile(".*"+options.query+".*"))
            if(aTag):
                for attr in aTag:
                   # hsoup = BeautifulSoup(urllib2.urlopen(_mvnrepourl+attr["href"]))
                    print attr["href"]
        else:
            searchr(soup,_mvnrepourl,options.query) 
    if options.artifact:
        print "not implement yet"
    if options.filename:
        if not options.artifact:
            print "what is artifact to add?"
        
