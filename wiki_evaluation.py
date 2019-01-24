#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 29 14:00:09 2018

@author: medich
"""

import sys
import urllib2

GRAPH_X_LEFT = 80
GRAPH_X_SCALE = 1070
GRAPH_X_COMPL = 1200
GRAPH_X_RIGHT = GRAPH_X_LEFT + GRAPH_X_SCALE + 10

GRAPH_Y_BOTTOM = 290
GRAPH_Y_SCALE = 270
GRAPH_Y_COMPL = 400
GRAPH_Y_TOP = GRAPH_Y_BOTTOM - GRAPH_X_SCALE - 10



HTML_GRAPHS_PRE = "<html> \
	<style> \
		.graph { \
			margin-left: 30px; \
		} \
	</style> \
 \
	<h1> Graphs </h1>"
    
HTML_GRAPHS_POST = "</html>"

HTML_GRAPHS_AXIS = "  		<line x1=" + str(GRAPH_X_LEFT) + " y1=" + str(GRAPH_Y_BOTTOM) + " x2=" + str(GRAPH_X_LEFT) + " y2=" + str(GRAPH_Y_TOP) + " style=\"stroke:rgb(0,0,0);stroke-width:2\" /> \
		<line x1=" + str(GRAPH_X_LEFT) + " y1=" + str(GRAPH_Y_TOP) + " x2=" + str(GRAPH_X_LEFT - 5) + " y2=" + str(GRAPH_Y_TOP + 10) + " style=\"stroke:rgb(0,0,0);stroke-width:2\"/> \
		<line x1=" + str(GRAPH_X_LEFT) + " y1=" + str(GRAPH_Y_TOP) + " x2=" + str(GRAPH_X_LEFT + 5) + " y2=" + str(GRAPH_Y_TOP + 10) + " style=\"stroke:rgb(0,0,0);stroke-width:2\"/> \
		 \
		<line x1=" + str(GRAPH_X_LEFT) + " y1=" + str(GRAPH_Y_BOTTOM) + " x2=" + str(GRAPH_X_RIGHT) + " y2=" + str(GRAPH_Y_BOTTOM) + " style=\"stroke:rgb(0,0,0);stroke-width:2\" /> \
		<line x1=" + str(GRAPH_X_RIGHT) + " y1=" + str(GRAPH_Y_BOTTOM) + " x2=" + str(GRAPH_X_RIGHT - 10) + " y2=" + str(GRAPH_Y_BOTTOM + 5) + " style=\"stroke:rgb(0,0,0);stroke-width:2\"/> \
		<line x1=" + str(GRAPH_X_RIGHT) + " y1=" + str(GRAPH_Y_BOTTOM) + " x2=" + str(GRAPH_X_RIGHT - 10) + " y2=" + str(GRAPH_Y_BOTTOM - 5) + " style=\"stroke:rgb(0,0,0);stroke-width:2\"/>"


graphHTML = HTML_GRAPHS_PRE

if (len(sys.argv) < 2):
    sys.exit("\npython wiki_evaluation.py -in <input-file>\n\
             Add '-vh' to use for each url version history data\n\
             Add '-html' to create an html output with graphs (only if -vh is given)")

vh = 0
htmlOutPut = 0
argC = 0
urls = ""

"""
Draws a graph to the given list and returns the updated html output.
Takes the actual html, the graphs heading, a list with values to put
into the graph and the graph color as a string for html code.
"""
def drawGraph(htmlText, locTitle, valueList, color, revList):
    htmlText = htmlText + "<h3> " + locTitle + " </h3>\n \
    <svg class=\"graph\" width=" + str(GRAPH_X_COMPL) + " height=" + str(GRAPH_Y_COMPL) + ">\n"
    htmlText = htmlText + HTML_GRAPHS_AXIS
    
    maxV = max(valueList)
    i = 0
    incr = 2.0
    if (maxV > 50):
        incr = 5.0
        if (maxV > 100):
            incr = 10.0
    while(i < maxV):
        i += incr
    maxV = i
    
    yr = 0
    if (max(valueList) > 0):
        yr = GRAPH_Y_SCALE / maxV
    
    xr = 0
    if (len(valueList) > 0):
        xr = GRAPH_X_SCALE / (len(valueList) - 1)
    
    v = 0
    for i in range(10):
        v = maxV / 10 * (i + 1)
        if (maxV > 20):
            v = int(v)
        y = GRAPH_Y_BOTTOM - ((i + 1) * GRAPH_Y_SCALE/10)
        htmlText = htmlText + "<line x1=" + str(GRAPH_X_LEFT - 3) + " y1=" + str(y) + " x2=" + str(GRAPH_X_LEFT + 3) + " y2=" + str(y) + " style=\"stroke:rgb(0,0,0);stroke-width:2\"/>"
        htmlText = htmlText + "<text x=" + str(0) + " y=" + str(y + 8) + ">" + str(v) + "</text>"
    
    points = ""
    c = 0
    for entry in valueList:
        x = GRAPH_X_LEFT + xr * c
        y = GRAPH_Y_BOTTOM - (entry * yr)
        points = points + str(x) + "," + str(y) + " "
        htmlText = htmlText + "<line x1=" + str(x) + " y1=" + str(GRAPH_Y_BOTTOM + 3) + " x2=" + str(x) + " y2=" + str(GRAPH_Y_BOTTOM - 3) + " style=\"stroke:rgb(0,0,0);stroke-width:2\"/>"
        htmlText = htmlText + "<text x=" + str(-360) + " y=" + str(x + 3) + " transform=\"rotate(-90 0,0)\"> " + str(revList[c][21:28:]) + "</text>"
        c = c + 1
        
    htmlText = htmlText + "<polyline points=\"" + points + "\" style=\"fill:none;stroke:" + color + ";stroke-width:3\" />\n"
    htmlText = htmlText + "</svg>\n"
    return htmlText
    

#check arguments from command input and handle exceptions
for x in range(len(sys.argv)):
    argC = argC + 1
    if (argC >= len(sys.argv)):
        break
    arg = sys.argv[argC]
    if (arg == "-vh"):
        vh = 1
    if (arg == "-html"):
        htmlOutPut = 1
    if (arg == "-in"):
        if (argC + 1 < len(sys.argv)):
            argC = argC + 1
            if (sys.argv[argC].find(".txt") <= 0):
                sys.exit("ERROR: Inputfile is not a text file")
            try:
                inputFile = open(sys.argv[argC])
                urls = inputFile.readlines()
                inputFile.close()
            except:
                sys.exit("ERROR: Given Input is not a File or missing")
if (urls == ""):
    sys.exit("ERROR: Input is missing")

#init text variable for endfile
endText = ""
#check all URLs
for url in urls:

    allURLs = []
    allURLs.append(url)
    
    #if version histery check is disired, init version history check
    if (vh):
        #build URL to version history and save its html
        allURLs = []
        urlBaseEnd = url.find("index.php") + len("index.php") + 1
        title = url[urlBaseEnd:]
        title = title[0:-1]
        urlBase = url[0:urlBaseEnd -1]
        vhURL = urlBase + "?title=" + title + "&action=history"
        response = urllib2.urlopen(vhURL)
        vhHTML = response.read()
        
        #extract all URLs to all versions from the version history html
        k = 0
        l = 0
        oldIDList = []
        while k > -1:
            k = vhHTML.find("oldid=", k+1)
            if k > -1:
                l = vhHTML.find("\"", k+1)
                oldIDList.append(int(vhHTML[(k + len("oldid=")):l]))
        
        #remove duplicates
        uniques = []
        for item in oldIDList:
            added = 0
            for item2 in uniques:
                if (item == item2):
                    added = 1
            if (added == 0):
                uniques.insert(0, item)
        oldIDList = uniques
        oldIDList.sort()
        
        #save all URLs in list
        for oldID in oldIDList:
            vhURL = urlBase + "?title=" + title + "&oldid=" + str(oldID)
            allURLs.append(vhURL)
        
    print(title)
    #run extra URLs (may be only single URL or all history URLs)
    wordList = []
    linkList = []
    imgList = []
    revList = []
    for exURL in allURLs:
    
        #print("load URL...")
        response = urllib2.urlopen(exURL)
        html = response.read()
         
        #print("get html content...") 
        i = html.find("<h1")
        j = html.find("</h1>")
        title = html[i:j]
        #print(title)
        
        #if version history check, save revision date
        if (vh):
            k = html.find("Revision as of")
            l = html.find(" by <", k+1)
            revision = html[k:l]
            print(revision)
    
        #find beginning and end of inner wiki content
        #specify beginning and end string
        startString = "<div id=\"mw-content-text\""
        i = html.find(startString)
        if (i != -1):
            i = i
        else:
            startString = "<div id=\"toctitle\" class=\"toctitle\">"
            i = html.find(startString)
        htmlStart = i
        endString = "<!-- \nNewPP limit report"
        j = html.find(endString)
        #get content
        htmlContent = html[i:j]
        #append to title to count its words as well
        realContent = title + " " + htmlContent
    
        #remove all tags from the real content to get only the content without
        #the html
        i = 1
        while (i >= 0):
            i = realContent.find("<")
            j = realContent.find(">")
            realContent = realContent[:i] + realContent[j+1:]
    
        #count worlds seperated by spaces
        words = realContent.split()
        wordCount = len(words) * 0.5
        print("Number of Words: " + str(int(wordCount)))
        
        #count links
        #skip links in table of contents
        endOfTOC = 0
        k = htmlContent.find("<li class=\"toclevel", 0)
        while (k > -1):
            l = htmlContent.find("<li class=\"toclevel", k+1)
            if (l == -1):
                endOfTOC = htmlContent.find("</ul>", k+1)
            k = l
        
        #start counting real links
        k = endOfTOC + 1
        links = 0
        while k > -1:
            k = htmlContent.find("<a ", k+1)
            if k > -1:
                links = links + 1
        
        #count images
        k = 0
        imgs = 0
        while k > -1:
            k = htmlContent.find("<img ", k+1)
            if k > -1:
                imgs = imgs + 1
        #remove links from liks in images from the link count
        links = links - imgs
        print("Number of links: " + str(links))
        print("Number of images: " + str(imgs))
        
        #specify URL name, that belongs to fetched information
        urlText = exURL
        if (vh):
            urlText = exURL + " - " + revision
        endText = endText + urlText + "\nNumber of words: " + str(wordCount) \
        + "\nNumber of links: " + str(links) \
        + "\nNumber of images: " + str(imgs) + "\n\n"
        
        #save values to lists
        wordList.append(wordCount)
        linkList.append(links)
        imgList.append(imgs)
        revList.append(revision)
        
    #create graphs from lists
    graphHTML = graphHTML + "<h2>" + title + "</h2>\n"
    if (len(wordList) > 1 and max(wordList) > 0):
        graphHTML = drawGraph(graphHTML, "Number of words", wordList, "green", revList)
    if (len(linkList) > 1 and max(linkList) > 0):
        graphHTML = drawGraph(graphHTML, "Number of links", linkList, "blue", revList)
    if (len(imgList) > 1 and max(imgList) > 0):
        graphHTML = drawGraph(graphHTML, "Number of images", imgList, "red", revList)
    
    
    
    
    
graphHTML = graphHTML + HTML_GRAPHS_POST
outFile = file("wiki_evaluation_out.html", "w")
outFile.write(graphHTML)
outFile.close()
        
outFile = file("wiki_evaluation_out.txt", "w")
outFile.write(endText)
outFile.close()

if (htmlOutPut and vh):
    print("htmlOut")
    outPutFile = file("wiki_evaluation_out.txt", "r")
    lines = outPutFile.readlines()
    outPutFile.close()
    
    #get data i datablocks
    getCount = 0
    title = ""
    newTitle = ""
    dataBlock = []
    dataBlockValues = []
    dataBlocks = []
    #dataBlock structure:
    #[URL, [revision, words, links, imgs], [revision, ...], ...]
    for line in lines:
        text = line[0:len(line) - 1]
        if (getCount == 0):
            if (text.find("http") > -1):
                newTitle = text[(text.find("title=") + len("title=")):text.find("&oldid")]
                if (newTitle == title):
                    #keep data block
                    dataBlockValues = [text[text.find("Revision"):]]
                    getCount = 1
                else:
                    if (len(dataBlock) > 0):
                        dataBlocks.append(dataBlock)
                    #create new graph data block
                    dataBlock = []
                    dataBlock.append(newTitle)
                    dataBlockValues = [text[text.find("Revision"):]]
                    getCount = 1
                
                title = newTitle
        elif (getCount == 1):
            dataBlockValues.append(text[len("Number of words: "):len(text)-2])
            getCount = 2
        elif (getCount == 2):
            dataBlockValues.append(text[len("Number of links: "):])
            getCount = 3
        elif (getCount == 3):
            dataBlockValues.append(text[len("Number of images: "):])
            getCount = 0
            dataBlock.append(dataBlockValues)
                
    dataBlocks.append(dataBlock)
    #print(dataBlocks)
    
    #create html output graphs
    
    
    #create final html
    finalHTML = ""
    
    finalHTMLFile = file("wiki_evaluation.html", "w")
    finalHTMLFile.write(finalHTML)
    finalHTMLFile.close()
    
    