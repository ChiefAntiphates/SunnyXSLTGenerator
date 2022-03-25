import re
from lxml import etree
from collections import Counter, deque
from sunny_misc import *


def transformToText(inputXmlTemplate, outputTxtTemplate):

	def getTextTemplate(text_output):
		g = open(text_output, "r")
		text = g.read()
		g.close()


		#identify most frequent number of times a word appears 
		def most_common(look_list):
			
			most_frequent, highest_frequency = 0, 0
			
			for i in set(look_list):
				frequency = look_list.count(i)
				if (frequency > highest_frequency):
					highest_frequency = frequency
					most_frequent = i
			
			return most_frequent
			
			
			
		def findMostConsistent(list_of_strings):
			
			for string in list_of_strings:
				number_matching = 0
				for string2 in list_of_strings:
					if string2 == string:
						number_matching += 1
				if number_matching > (len(list_of_strings)//2):
					return string
					
			return "ERROR"	




		wordlist = []

		for word in list(text.split()):
			indexes = [wordindex.start() for wordindex in re.finditer((r'[^a-zA-Z0-9\'\"]'+word+r'[^a-zA-Z0-9\'\"]'), " "+text+" ")]
			distance = 0
			if len(indexes) > 1:
				distance = indexes[1] - indexes[0]
			wordlist.append((word, len(indexes), indexes, distance))
	
		

		##the following creates a template
		common_freq = most_common([i[1] for i in wordlist])

		count = 0
		newwordlist = []
		valueslist = []
		prev = False
		
		
		common_words = [word[0] for word in wordlist if word[1] >= common_freq]	
		single_words = [word[0] for word in wordlist if word[1] == common_freq]
		
		common_words = common_words[:common_words[common_words.index(single_words[0])+1:].index(single_words[0])+1]
		
		
		
		
		all_words = [word[0] for word in wordlist]
		temp_string = []
		counter = common_words.index(all_words[0])
		value_pres = False
		for word in all_words:
		
			if word == common_words[counter]:
				value_pres = False
				counter += 1
				if counter == len(common_words):
					counter = 0
				temp_string.append(word)
			
			else:
				if not value_pres:
					value_pres = True
					temp_string.append("!VALUE!")
			
		
		
		stringo_temps = []
		new_string = []
		started = False
		anchor = ""
		for i in range(len(temp_string)):
			if started:
				if temp_string[i] == anchor:
					stringo_temps.append(new_string)
					new_string = []
					new_string.append(temp_string[i])
				else:
					new_string.append(temp_string[i])
					
					if i == len(temp_string)-1:
						stringo_temps.append(new_string)
			
			else:
				if temp_string[i] in single_words:
					anchor = temp_string[i]
					started = True
					new_string.append(temp_string[i])
	
		
		word_template = findMostConsistent(stringo_temps)
		
		
		##this temp for after the following for loop
		temp = repr(text)
		
		value_with_words = [word[0] for word in wordlist]
		value_with_words2 = value_with_words
		for word in value_with_words2:
			if word not in word_template:
				index = value_with_words.index(word)
				value_with_words[index] = "!VALUE!"
				
				
		print("value with words")
		print(value_with_words)
		print("value with words")
				
		counter = 0
		for i in range(len(wordlist)):
			
			value = wordlist[i][0]
			if (wordlist[i][1] < common_freq):
				
				if prev:
					valueslist.append((wordlist[i][0], -1))
					continue
					
				else:
					valueslist.append((wordlist[i][0], 0))
					value = "!VALUE!"
					prev = True
			elif (wordlist[i][1] > common_freq):#may need to #do an extra one here where the latter value can be not a common word (only checks for !VALUE! before
				
				latter_condition = False
				potential_matches = set()
				y = 0
				for _ in range(len(word_template)):
					try:
						potential_matches.add(word_template[word_template[y:].index(value)-1+y])
					except (IndexError, ValueError) as e:
						print(e)
						break
					y=y+(word_template[y:].index(value)-1+y)
					
				if (newwordlist[-1][0] in potential_matches):
					latter_condition = True
				if not((value_with_words[i+1] == word_template[word_template.index(value)+1]) and latter_condition):
					
					if prev:
						valueslist.append((wordlist[i][0], -1))
						continue
					else:
						valueslist.append((wordlist[i][0], 0))
						value = "!VALUE!"
						prev = True
			else:
				prev = False
			newwordlist.append((value, wordlist[i][1], wordlist[i][2], wordlist[i][3]))


		##ERROR##
		'''Currently does not work if a value is the last word in loop'''
		
		
	
		##Ending line to join each line with
		ending_line = temp[temp.index(word_template[-1])+len(word_template[-1]):temp[len(word_template[0]):].index(word_template[0])+len(word_template[0])]
		
		##because XSLT treats some special characters differently we need to replace
		ending_line = ending_line.replace(r"\n", r"&#10;")
		
		
		
		
		'''##This is achieved using word_template
		only_words = [i[0] for i in newwordlist]
		#print(only_words)
		#print(len(only_words))
		only_words = (only_words[:len(only_words)//common_freq])
		'''
		
		only_words = (" ".join(word_template))
		
		
		'''
		print(len(only_words))
		print(common_freq)
		print(len(only_words)//common_freq)
		
		
		#print(only_words)
		print(only_words[:len(only_words)//common_freq])
		only_words = only_words[:len(only_words)//common_freq]
		'''
		
		combined_valueslist = []
		collected = []
		for i in reversed(valueslist):
			if (i[1] == 0):
				collected.append(i)
				collected = [i[0] for i in collected]
				full_value = " ".join(list(reversed(collected)))
				combined_valueslist.append(full_value)
				collected = []
			else:
				collected.append(i)

		
		combined_valueslist = list(reversed(combined_valueslist))
		
		separated_values_list = []
		
		
		for i in range(0, len(combined_valueslist), len(combined_valueslist)//common_freq):
			temp = [combined_valueslist[j] for j in range(i, i+len(combined_valueslist)//common_freq)]
			separated_values_list.append(temp)
			
		
		punctuation = ["\"", ".", ",", "\\", "/", "'", ";", ":", "!"]
		bad_chars = []
		for i in range(len(separated_values_list[0])):
			word = separated_values_list[0][i]
			
			if word[-1] in punctuation:
				
				bad_char = word[-1]
				consistent = True
			
				for j in separated_values_list[1:]:
					new_word = j[i]
					if new_word[-1] != bad_char:
						
						consistent = False
						break
						
				if consistent:
					bad_chars.append(bad_char)
				else:
					bad_chars.append("")
			else:
				bad_chars.append("")

		final_values = []
		for word_list in separated_values_list:
			new_word_list = []
			for i in range(len(word_list)):
				word = word_list[i]
				try:
					new_word = word.strip(bad_chars[i])
					new_word_list.append(new_word)
				except IndexError as e:
					
					new_word_list.append(word)
			final_values.append(new_word_list)



		
		counter = 0
		for bad_char in bad_chars:
			print("counter %s" % counter)
			index = only_words[counter:].index("!VALUE!")
			print(only_words[counter:])
			print(index)
			
			only_words = only_words[:index+7+counter] + bad_char + only_words[counter+index+7:]
			counter = index + 7 + counter
			print(only_words)

		
		return(only_words, final_values, common_freq, ending_line)
		
		
	
			

	template_output = outputTxtTemplate
	word_template, values, frequency, ending_line = getTextTemplate(outputTxtTemplate)
	##Once out, it should be validated with the user that each of these variables are correct
	'''
	VALIDATION HERE
	'''
	xmlFile = inputXmlTemplate
	value_paths = getPathValues(xmlFile, values)



	##One of the limitations will be only a single loop point
	#However, due to the general simplicity of word docs this should be okay?
	##This function is what will need to be changed for multiple loop points (foreach loops)
	##Also in the function called here we haven't accounted for higher level tag calling
	g = open(xmlFile, "r")
	inputTemplateXml = g.read()
	g.close()
	looping_tag = getLoopingTag(inputTemplateXml, frequency, value_paths)


	##lets lay out all our values on the tables
	print("\n\n\n\n\n------------------\n\n")
	print("Frequency: %s\n" % frequency)
	print("Word template: %s\n" % word_template)
	print("Values: %s\n" % values)
	print("Value paths: %s\n" % value_paths)
	print("Looping tag: %s\n" % looping_tag)



	value_of, for_each_path = creatingCorrectPaths(value_paths, looping_tag)
	print(value_of)

	word_template = (word_template.split("!VALUE!"))

	f = open("current.xslt", "w+")
	f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
	f.write('<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">\n')
	f.write('\t<xsl:output method="text" omit-xml-declaration="yes" indent="yes"/>\n')
	f.write('<xsl:template match ="/">\n')
	f.write('<xsl:for-each select ="%s">\n' % for_each_path)
	for words in word_template:
		f.write('<xsl:text>%s</xsl:text>\n' % words)
		if value_of != []:
			f.write('<xsl:value-of select="%s"/>\n' % value_of[0])
			value_of.remove(value_of[0])
	f.write('<xsl:text>%s</xsl:text>\n' % ending_line)
	f.write('</xsl:for-each>\n')
	f.write('</xsl:template>\n')
	f.write('</xsl:stylesheet>')
	f.close()


	fileGenerated()

'''then we just do the saving process which can probably be copied from previous 
function'''