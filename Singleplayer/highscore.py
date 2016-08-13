# Authors                  Connor Pacala(Network Developer),
#                          Joseph Vidal(Engine Developer),
#                          Paul Zotz(Input and Tools Developer)
# Date Created:            7/19/2016
# Date Last Modified:      7/22/2016
# File Name:               highscore.py
#
# Overview: 	Class to read, update, and write a single high score number.
#	    	Uses Python ElementTree library to create, read from, and write
#	    	to an xml file. 
#          
# Citations: 	Python ElementTree documentation:
#	     	https://docs.python.org/2/library/xml.etree.elementtree.html
			
import xml.etree.ElementTree as ET
import os.path

class highScore():
    def __init__(self, filename):
        self.filename = filename
	self.tree = None 
	self.root = None
        self.highscore = None #convert to list if multiple scores
    
    def readFile(self):
        if os.path.isfile(self.filename):
            self.tree = ET.parse(self.filename)
            self.root = self.tree.getroot()
    
    def readScore(self):
        if self.root != None:
            for child in self.root: #only child in file is score now
                self.highscore = child.text 
    
    def writeScore(self):
        if self.tree == None: #no score read; build xml file
            self.root = ET.Element("highscore")
            scoreElement = ET.SubElement(self.root, "score")
            scoreElement.text = str(self.highscore)
            self.tree = ET.ElementTree(self.root)        
        else:
            for score in self.root.iter('score'):
                score.text = str(self.highscore)

        self.tree.write(self.filename, encoding='utf-8', xml_declaration = True)

    def getScore(self):
	if self.highscore == None:
          return 0	
        return int(self.highscore)

    def setScore(self, newScore):
        self.highscore = newScore
