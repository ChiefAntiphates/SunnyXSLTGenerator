import re
import csv
from lxml import etree
from collections import Counter, deque
from sunny_misc import *



def transformToCsv(inputXmlTemplate, outputCsvTemplate):

	
	delim = "," # Chosen because excel default delimiter is comma
	
	headings = []
	values = []
	
	with open(outputCsvTemplate) as csv_file:
		reader = csv.reader(csv_file, delimiter=delim)
		header_unpassed = True
		for line in reader:
			if header_unpassed:
				headings = line
				header_unpassed = False
			else:
				values.append(line)
	
			
	
	value_paths = getPathValues(inputXmlTemplate, values)

	f = open("TV_listings.xml", "r")
	inputXml = f.read()
	f.close()
	looping_tag = getLoopingTag(inputXml, len(values), value_paths)
	value_of, for_each_path = creatingCorrectPaths(value_paths, looping_tag)
	

	f = open("current.xslt", "w+")
	f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
	f.write('<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">\n')
	f.write('\t<xsl:output method="text" omit-xml-declaration="yes" indent="yes"/>\n')
	f.write('<xsl:template match ="/">\n')
	for i in range(len(headings)):
		if (i == len(headings)-1):
			f.write("<xsl:text>%s</xsl:text>\n" % headings[i])
		else:
			f.write("<xsl:text>%s%s</xsl:text>\n" % (headings[i],delim))
	f.write("<xsl:text>&#10;</xsl:text>\n")
	f.write('<xsl:for-each select ="%s">\n' % for_each_path)
	for i in range(len(value_of)):
		f.write('<xsl:value-of select="%s"/>' % value_of[i])
		if (i != len(value_of)-1):
			f.write("<xsl:text>%s</xsl:text>\n" % delim)
	f.write("<xsl:text>&#10;</xsl:text>\n")
	f.write('</xsl:for-each>\n')
	f.write('</xsl:template>\n')
	f.write('</xsl:stylesheet>')
	f.close()


	fileGenerated()

