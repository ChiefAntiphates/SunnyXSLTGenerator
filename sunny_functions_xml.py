
import re
import os
from collections import deque
from lxml import etree
import tkinter as tk
from tkinter.filedialog import asksaveasfile as tksave
from tkinter import messagebox as tkalert
import sys
from functools import partial
from collections import OrderedDict
from sunny_misc import *
from threading import Thread
from playsound import playsound

'''
Write description of function here
'''
def getXmlMappingValues(sample_input_file, sample_output_file):

	
	def getInputPath(tree, string, tk_input_text, last_char_index):
		
		valid = False
		
		try:
			r = tree.xpath(".//%s" % string)
			
			list_of_possible_paths = 0
			
			if len(r) > 1:
			
				list_of_possible_paths = [tree.getpath(r[i]) for i in range(len(r))]
				
				#remove colons from list and convert to set
				temporary_list = []
				for path in list_of_possible_paths:
					temporary_list.append(re.sub('\[\d+?\]', '', path))
				
				list_of_possible_paths = list(set(temporary_list))
				print(list_of_possible_paths)
			
			else:
				input_path = tree.getpath(r[0]).replace("[1]", "")[1:]
			
			print(len(list_of_possible_paths))
			
			
			if len(list_of_possible_paths) > 1:
				max_path_number = 0
				for path in list_of_possible_paths:
					if len(path[1:].split("/")) > max_path_number:
						max_path_number = len(path[1:].split("/"))
				
				print(list_of_possible_paths)
				input = "BIG ERROR"
				final_path = None
				
				for i in range(2, max_path_number):
					nearest_parent = None
					found_difference = False
					nearest_path = None
					
					for full_path in list_of_possible_paths:
					
						path = full_path.split("/")[-i]
						
						backwards_parent_index = tk_input_text.search(path, last_char_index, backwards=True)
						print("Path: %s" % path)
						print("last_char_index: %s" % last_char_index)
						print("backwards_parent_index: %s" % backwards_parent_index)
						chars_away_from_parent = abs(float(last_char_index) - float(backwards_parent_index))
						print("full path: %s" % full_path)
						print("chars aways: %s" % chars_away_from_parent)
						if nearest_parent == None:
							nearest_parent = chars_away_from_parent
							nearest_path = full_path
					
						elif chars_away_from_parent < nearest_parent:
							found_difference = True
							nearest_parent = chars_away_from_parent
							nearest_path = full_path
						
						elif chars_away_from_parent > nearest_parent:	
							found_difference = True
							
						print(chars_away_from_parent)
					
					if found_difference:
						final_path = nearest_path
						break
				
				print("Final decided path is: %s" % final_path)
				
				input_path = final_path.replace("[1]", "")[1:]
			
			else:#only one match
				print(list_of_possible_paths)
				print(list_of_possible_paths[0])
				input_path = list_of_possible_paths[0].replace("[1]", "")[1:]
			
			valid = True
			
		except (etree.XPathEvalError, IndexError, TypeError) as e:
			input_path = "not valid"
		
		return input_path, valid
	
		#End of get input path
		
		
		
	def goToGenerate():
		print("NEST MAPPING BELOW")
		print(nestMapping)
		_, inputNestMapping = getOutputValues(sample_input_file)
		print(inputNestMapping)
		
		
		
		def showFileContext(file):
			context = tk.Toplevel(choose_nest)
			tk.Button(context, text="Close", command = lambda x= context: x.destroy()).pack()
			f = open(file, "r")
			text = f.read()
			f.close()
			tk_file_text = tk.Text(context)
			tk_file_text.pack()
			tk_file_text.insert(tk.END, text)
			tk_file_text.config(state=tk.DISABLED)
		
		def assignCorrectMap(i):
			global correct_map
			correct_map = i
			
			choose_nest.destroy()
		
		def helpSectionNestingTag():
			print("help section here")
			helpWindow = tk.Toplevel(root)
			helpWindow.title('Help')
			helpWindow.grid_columnconfigure(0, weight=1)
			help_text = tk.Text(helpWindow)
			help_text.grid(row=0, column=0, sticky="news")
			f = open("help_files/help_nesting.txt", "r")
			help_content = f.read()
			f.close()
			help_text.insert(tk.END, help_content)
			help_text.config(state=tk.DISABLED)
		
		
		
		
		
		def checkCorrectMapWithUser(match_var, user_select, last_char):
		
			def confirmValuesCorrectMap(user_select, last_char):
				global correct_map
				global nested_last_char_index
				confirm_window.destroy()
				nested_last_char_index = last_char ##Last char is index of last selected character
				correct_map = user_select
			
			def destroyConfirmWindow():
				confirm_window.destroy()
				
				
			
			try:
				user_select = re.search('<(.*?)[>| ]', user_select).group(1)
				print("passed first")
				if "/" in user_select:
					print("closing tag in")
					raise AttributeError("Closing tag")
				
				
			except AttributeError:
				print("ready attr")
				if user_select[0] == "<":
					user_select = user_select[1:]
				
				
				if user_select[0] =="/":
					user_select = user_select[1:]
			
				
			confirm_window = tk.Toplevel(choose_nest)
			confirm_window.title('Confirm Selection')
			tk.Label(confirm_window, text="Do you confirm that <%s> corresponds to <%s>?" % (user_select, match_var)).grid(row=0, column=0, columnspan=2)
			tk.Button(confirm_window, text="Yes", command=lambda: confirmValuesCorrectMap(user_select, last_char)).grid(row=1, column=0)
			tk.Button(confirm_window, text="No - Retry", command=destroyConfirmWindow).grid(row=1, column=1)
			
		
		root.withdraw()
			
		print("Nest mapping")
		print(nestMapping)
		for nest in nestMapping:
			same_len = [name for name in inputNestMapping if inputNestMapping[name] == nestMapping[nest]]

			global correct_map
			correct_map = ""
			
		
			nested_last_char_index = "1.1"####This is for initialise and is liable to change when more than one
				
			choose_nest = tk.Toplevel(root)
			choose_nest.title('Sunny XSLT Generator')
			choose_nest.grid_columnconfigure(0, weight=1)
			tk_input_text = tk.Text(choose_nest)
			tk_input_text.grid(row=4, column=0, sticky="ews")
			tk_input_text.insert(tk.END, sampleInput)
			tk_input_text.config(state=tk.DISABLED)
			
			menu_bar = tk.Menu(choose_nest)

			options_menu = tk.Menu(menu_bar, tearoff=0)
			options_menu.add_command(label="What am I supposed to do?", command=helpSectionNestingTag)
			menu_bar.add_cascade(label="Help", menu=options_menu)

			choose_nest.config(menu=menu_bar)
			
			
			print("input nest mapping: %s" % inputNestMapping)
			print("nest mapping: %s" % nestMapping)
			print("nest: %s" % nest)
			print("SAME LEN: %s" % same_len)
			if len(same_len) == 1:
				correct_map = same_len[0]
			
			
			else:
				
				tk.Label(choose_nest, text="For which of the input tags should <%s> loop according to?" % nest).grid(row=0, column=0)
				#Add a button like: confused? Click here!
				tk.Label(choose_nest, text="Highlight the correct tag and press \"Go!\"").grid(row=1, column=0)
				tk.Button(choose_nest, text="See Output File", command = lambda: showFileContext(sample_output_file)).grid(row=2, column=0)
				
				#Currently the user has to select the exact correct characters - validate for this
				tk.Button(choose_nest, text="Go!", command = lambda: checkCorrectMapWithUser(nest, tk_input_text.get(tk.SEL_FIRST, tk.SEL_LAST), tk_input_text.index(tk.SEL_LAST))).grid(row=3, column=0)
				while correct_map == "":
					choose_nest.update()
			
			##########################################################
			
			
			
			
			input_path, valid = getInputPath(tree, correct_map, tk_input_text, nested_last_char_index)
		
			
			nestMapping[nest] = [input_path, len(input_path.split("/"))]
		
			choose_nest.destroy()

		
		
		xmlToXmlTransform(sample_output_file, tagMapping, nestMapping)
		root.destroy()
		fileGenerated()
		
		###END of geenerate function
		
	
	
	def userSetValues(output_param):
		
	
		def findPath(string, output_param, last_char_index):
			valid = False
			is_attribute = 0
			input_path = "BIG ERROR"
			
			if tk_input_text.get(last_char_index) == "=":
				
				is_attribute = 1
				
				attribute_name = string.split(" ")[-1]
				
				print(attribute_name)
				
				pos = tk_input_text.search('<', last_char_index, stopindex="1.0", backwards=True)
				
				#this is the tag associated with the attribute
				attr_parent_tag = tk_input_text.get(pos, last_char_index).split(" ")[0][1:]
				
				if attr_parent_tag != top_input_tag:
					
					attr_parent_tag, valid = getInputPath(tree, attr_parent_tag, tk_input_text, last_char_index)
					
				input_path = attr_parent_tag + "/" + attribute_name
				
			
			elif ("=" in string) and ("<" not in string):
				is_attribute = 1
				pos1 = tk_input_text.search('=', last_char_index, stopindex="1.0", backwards=True)
				attribute_name = tk_input_text.get(tk.SEL_FIRST, pos1).split(" ")[-1]
				print(attribute_name)
				pos = tk_input_text.search('<', last_char_index, stopindex="1.0", backwards=True)
				attr_parent_tag = tk_input_text.get(pos, last_char_index).split(" ")[0][1:]
				
				if attr_parent_tag != top_input_tag:
					
					attr_parent_tag, valid = getInputPath(tree, attr_parent_tag, tk_input_text, last_char_index)
					
				input_path = attr_parent_tag + "/" + attribute_name
			
			
			elif ("=" in string) and ("<" in string):
				tkalert.showwarning("Multiple Tags Selected",
					"Please only select one tag.\nEach tag ends with either a > or a =")
			
				
			else:
				if string[0] == "<":#clean up the string for better usability
					
					try:
						end = string.index(">")
					except ValueError:
						end = len(string)
					string = string[1:end].split(" ")[0]
				
				
				
				if string == top_input_tag:
					input_path = string
					valid = True
				
				
				#Standard condition
				else:
				
					input_path, valid = getInputPath(tree, string, tk_input_text, last_char_index)

			
			
			if valid:
				
				tagMapping[output_param] = [input_path, len(input_path.split("/"))-1, is_attribute]##add attribute
				
				result = tk.Text(root, height = 1)
				result.grid(column = 2, row = list(tagMapping.keys()).index(output_param)+1)
				result.insert(tk.END, input_path)
				result.config(state=tk.DISABLED)
				
				tk.Label(root, text=output_param, bg="SeaGreen1", width=20).grid(column = 0, row = list(tagMapping.keys()).index(output_param)+1)
				
				
				new_win.destroy()
				
			return valid, input_path
		#END findPath FUNCTION
		
		
		
		def selectFromInput(output_param):
			print(output_param)
			valid = False
			
			print("\n\n\nBEFORE TRY EXCEPT\n\n\n")
			try:
				print("\nin teh try\n")
				user_selection = tk_input_text.get(tk.SEL_FIRST, tk.SEL_LAST)
				selection_index = tk_input_text.index(tk.SEL_LAST)
				print(selection_index)
				valid, input_path = findPath(user_selection, output_param, selection_index)
				print("past it all")
			except tk.TclError as e:
				print("Please select a tag")
				print(e)
			
			if valid:
				
				
				print(tagMapping)
				print(nestMapping)
				
			else:
				print("invalid try again")
		#END selectFromInput FUNCTION
		
		
		def showContext(output_param, output_param_label):
			print(output_param)
			
			#This is for if the value wanted is part of an attribute
			if len(output_param.split("/")) > 1:
				output_param = output_param.split("/")
				example_value = sampleOutput[sampleOutput.index(output_param[0])-1:sampleOutput.index("<", sampleOutput.index(output_param[0]))]
				print("example here: %s" %example_value)
				example_value = example_value[example_value.index(output_param[1]):]
				print("example here: %s" %example_value)
				example_value = example_value[example_value.index("\"")+1:]
				example_value = example_value[:example_value.index("\"")]
				print("example here: %s" %example_value)
				
		
			else:
				output_param = output_param.split("/")[0]
				example_value = sampleOutput[sampleOutput.index(output_param)-1:sampleOutput.index("<", sampleOutput.index(output_param))]
				
				example_value = example_value[example_value.index(">")+1:]
			
			output_param_label.insert(tk.END, "The value of the first instance of this tag is: ")
			output_param_label.insert(tk.END, example_value, ("pink"))
			
			
			return output_param_label
			
		def showFullOut():
			full_out_win = tk.Toplevel(new_win)
			tk.Button(full_out_win, text="Close", command = lambda x= full_out_win: x.destroy()).pack()
			tk_output_text = tk.Text(full_out_win)
			tk_output_text.pack()
			tk_output_text.insert(tk.END, sampleOutput)
			tk_output_text.config(state=tk.DISABLED)
			
		def helpSectionSelectTag():
			print("help section here")
			helpWindow = tk.Toplevel(root)
			helpWindow.title('Help')
			helpWindow.grid_columnconfigure(0, weight=1)
			help_text = tk.Text(helpWindow)
			help_text.grid(row=0, column=0, sticky="news")
			f = open("help_files/help_select_tag.txt", "r")
			help_content = f.read()
			f.close()
			help_text.insert(tk.END, help_content)
			help_text.config(state=tk.DISABLED)
		
		
		def readAloudTag():
			def playSound():
				playsound("sounds/output_mapping_tag.wav")
			Thread(target = playSound).start()
			
			
			
		new_win = tk.Toplevel(root)
		new_win.configure(bg="#ffe26e")
		
		output_param_label = tk.Text(new_win, height=5, font="Calibri 10", background="#ffe26e", relief="flat")
		output_param_label.grid(row=0, column=0)
		output_param_label.tag_configure("bold", font="Calibri 14 bold")
		output_param_label.tag_configure("small_bold", font="Calibri 10 bold")
		output_param_label.tag_configure("big", font="Calibri 14")
		output_param_label.tag_configure("pink", foreground="deep pink")
		output_param_label.insert(tk.END, "What does the output tag ", ("big"))
		output_param_label.insert(tk.END, output_param, ("bold","pink"))
		output_param_label.insert(tk.END, " map to in the input file below?\n", ("big"))
		output_param_label = showContext(output_param, output_param_label)
		output_param_label.insert(tk.END, "\nPlease highlight any instance of the correct mapping ")
		output_param_label.insert(tk.END, "tag", ("small_bold"))
		output_param_label.insert(tk.END, " below.")
		output_param_label.config(state=tk.DISABLED)
		
		
		
		
		tk.Button(new_win, text = "See Full Output File", command=showFullOut).grid(row=3, column=0)
		
		new_win.grid_columnconfigure(0, weight=1)
		tk_input_text = tk.Text(new_win)
		tk_input_text.grid(row=5, column=0, sticky="ews")
		tk_input_text.insert(tk.END, sampleInput)
		tk_input_text.config(state=tk.DISABLED)
		
		
		
		##Insert the user selection as a param here (put into a try except thing !! then get rid of select from input function
		button = tk.Button(new_win, text="Go!", command=partial(selectFromInput, output_param))
		button.grid(row=4, column=0)
		
		menu_bar = tk.Menu(new_win)

		options_menu = tk.Menu(menu_bar, tearoff=0)
		options_menu.add_command(label="What am I supposed to do?", command=helpSectionSelectTag)
		options_menu.add_command(label="Read Aloud", command=readAloudTag)
		menu_bar.add_cascade(label="Help", menu=options_menu)

		new_win.config(menu=menu_bar)

	#END userSetValues FUNCTION
		
	def returnToMain():
		root.destroy()
		import sunny_main
	
	def helpSectionValuesList():
		print("help section here")
		helpWindow = tk.Toplevel(root)
		helpWindow.title('Help')
		helpWindow.grid_columnconfigure(0, weight=1)
		help_text = tk.Text(helpWindow)
		help_text.grid(row=0, column=0, sticky="news")
		f = open("help_files/help_values_list.txt", "r")
		help_content = f.read()
		f.close()
		help_text.insert(tk.END, help_content)
		help_text.config(state=tk.DISABLED)
	
	def readAloudValuesList():
		def playSound():
			playsound("sounds/value_mappings.wav")
		Thread(target = playSound).start()
		
	##Big function code starts here
	
	tagMapping, nestMapping = getOutputValues(sample_output_file)

	f = open(sample_input_file, "r")
	sampleInput = f.read()
	f.close()
	
	f = open(sample_output_file, "r")
	sampleOutput = f.read()
	f.close()
	
	tree = etree.parse(sample_input_file)
	
	#Get the top xml tag in input to except in the path finding
	top_input_tag = tree.getroot().tag
	
	
	root = tk.Tk()
	root.configure(bg="#ffe26e")
	root.title('Sunny XSLT Generator')
	root.iconbitmap('sunny.ico')
	root.minsize(250, 300) 
	root.maxsize(1000, 1000)
	
	
	
	menu_bar = tk.Menu(root)

	options_menu = tk.Menu(menu_bar, tearoff=0)
	options_menu.add_command(label="What am I supposed to do?", command=helpSectionValuesList)
	options_menu.add_command(label="Read Aloud", command=readAloudValuesList)
	menu_bar.add_cascade(label="Help", menu=options_menu)

	root.config(menu=menu_bar)
	
	
	tk.Label(root, text = "Value Mappings:", bg="#ffe26e").grid(column = 0, row = 0)
	
	
	
	for output_tag in tagMapping:
		tk.Button(root, text="Select Mapping Value", command=partial(userSetValues, output_tag), width=20).grid(column = 1, row = list(tagMapping.keys()).index(output_tag)+1)	
		tk.Label(root, text=output_tag, bg="OrangeRed3", width=20).grid(column = 0, row = list(tagMapping.keys()).index(output_tag)+1)
	
	
	tk.Label(root, text="\n\nStep 2: Assign value mappings.\nSee the \"Help\" section for further guidance.", bg="#ffe26e").grid(column = 0, columnspan = 2, row = len(tagMapping) + len(nestMapping) + 5)
	
	all_done = False
	while(not all_done):
		all_done = True
		for output_tag in tagMapping:
			if tagMapping[output_tag] == "":
				all_done = False
		root.update()
	
	generate_button = tk.Button(root, text="Generate XSLT", command = goToGenerate)
	generate_button.grid(column = 0, row = len(tagMapping) + len(nestMapping) + 4)
	
	
	
	
	root.mainloop()
	
	print(tagMapping)
	print(nestMapping)
	



'''
Write description of function here
'''
def getOutputValues(sample_output_file):
	
	def addReqValues(n, close):
		
		has_attr = False
		attribute = ""
		try:
			n = sampleOutput.index("<", n+1, close)
			
		except ValueError:
			return close
			
		tag = re.search('<[^?](.*?)>', sampleOutput[n:]).group(0)
		orig_tag_len = len(tag)
		
	
		if ' ' in tag:
			has_attr = True
			tag, attribute = tag.split()[0] + ">", " ".join(tag.split()[1:])
			
		
			
		if tag in visited:
		
			miss = tag
			miss_close = tag[0] + "/" + tag[1:]
			while tag == miss or tag == miss_close:
				n+=1
				tag = re.search('<[^?](.*?)>', sampleOutput[n:]).group(0)
		
			if "/" in tag:
				tag = tag.replace("/", '')
			if ' ' in tag:
				tag = tag.split()[0] + ">"
			
			if (tag in visited):
				return close
			else:
				n = sampleOutput.index(tag, n+1, close)
			
				
		visited.append(tag)
		tag_value = tag[1:len(tag)-1]
		print("Tag here: %s" % tag)
		
		#'''
		print("Tag  value: %s" % tag_value)
		print(sampleOutput[n:n+orig_tag_len])
		
		#'''##HERE WE NEED TO FIX THAT CURRENTLY A TAG SUCH AS <length name="yes"/> (self closing tags) ARE NOT ALLOWED!!!###
		
		isValue = re.findall(r"([a-zA-Z0-9_]+)(?![^\<]*[\>|<\/])", sampleOutput[n+orig_tag_len:sampleOutput.index("</%s" % tag_value)])
		
		if len(isValue) > 0:
			print(tag)
			tagMapping[tag_value] = ""
		
		
		
	
		
		if len(re.findall(r"<\/?" + re.escape(tag[1:-1]) + r"( |>)", sampleOutput[n:close])) > 2:
			nestMapping[tag_value] = len(re.findall(r"<\/?" + re.escape(tag[1:-1]) + r"( |>)", sampleOutput))
			
		if has_attr:
			#Introduce loop for incase there are multiple attributes in one line
			first_one = True
			for individual_attr in attribute.split("="):
				print("individual_attr %s" % individual_attr)
				if first_one:
					first_one = False
				elif ">" in individual_attr:
					break
				else:
					individual_attr = individual_attr.split("\" ")[1]
					
				attribute_field = tag[1:-1] + "/" + individual_attr
				tagMapping[attribute_field] = ""
			#same attribute
			attribute_field = tag[1:-1] + "/" + attribute.split("=")[0]
			print(attribute_field)
			tagMapping[attribute_field] = ""
		
		
		close = sampleOutput.index((tag[0:1] + "/" + tag[1:]), n+1)
		
		while n < close:
			n = addReqValues(n, close)
		return close
	
	tagMapping = OrderedDict()
	nestMapping = OrderedDict()
	
	
	f = open(sample_output_file, "r")
	sampleOutput = f.read()
	f.close()
	
	visited = []
	firstTag = re.search('<[^?](.*?)>', sampleOutput).group(0)
	n = sampleOutput.index(firstTag)-1	
	close = len(sampleOutput)
	
	addReqValues(n, close)

	
	
	return tagMapping, nestMapping









'''
Function for returning what to write to XSLT file for the value of functions
'''
def writeValueOf(depth, tag_value, for_each, tagMapping):
	insert = ""
	attribute_status = tagMapping[tag_value][2]
	
	tag_write = ""
	tag_path = tagMapping[tag_value][0].split("/")
	print("\n---------------------------")
	
	if depth > tagMapping[tag_value][1]:
		iter = depth - tagMapping[tag_value][1]
		insert = iter*"../"
		if attribute_status == 1:
			tag_write = insert + "@" + tag_path[-1]
		elif iter == 1 and tag_path[-1] == for_each:
			tag_write = "."
		else:
			tag_write = insert + tag_path[-1]
		
			
	elif depth < tagMapping[tag_value][1]:
		diff = tagMapping[tag_value][1] - depth + 1
		while diff > 0:
			tag_write += tag_path[-diff]
			if diff >= 2:
				tag_write += "/"
			if diff == 2 and attribute_status == 1:
				tag_write += "@"
			
				
			diff -=1
			print("inside diff: %s" % diff)
			
		print("inside tag write: %s" % tag_write)
			
		
		#What is going on here? Someone please tell me!
		'''if attribute_status == 1:
			tag_write_temp = tag_write.split("/")[-1]
			tag_write = tag_write[:-len(tag_write_temp)] + "@" + tag_write_temp
		else:
			tag_write = tag_write[:-1]'''
	
	elif (attribute_status == 1) and (for_each != tag_path[-2]):
		print(tag_value)
		print(tag_path)
		tag_write = "../%s/@%s" % (tag_path[-2], tag_path[-1]) 
	
	else:
		print("if three")
		if attribute_status == 1: #Attribute
			tag_write = "@" + tag_path[-1]
		else:
			tag_write = tag_path[-1]
	
	
		
	return('<xsl:value-of select="%s"/>\n' % tag_write)
	
	
	
	
'''
Execute XML -> XML transform using the collected mappings
'''
def xmlToXmlTransform(sample_output_file, tagMapping, nestMapping):
	
	
	def parseXmlOut(n, close, depth):
		global last_for_each
		
		has_attr = False
		attribute = ""
		#Find the next tag in the output file
		try:
			n = sampleOutput.index("<", n+1, close)
			
		except ValueError:
			f.write(stack.pop() + "\n")
			return close
			
		
		tag = re.search('<[^?](.*?)>', sampleOutput[n:]).group(0)
		if ' ' in tag:
			has_attr = True
			tag, attribute = tag.split(" ")[0] + ">", " ".join(tag.split()[1:])

	
		if tag in visited:
			has_attr = False
			miss = tag
			miss_close = tag[0] + "/" + tag[1:]
			while tag == miss or tag == miss_close:
				n+=1
				tag = re.search('<[^?](.*?)>', sampleOutput[n:]).group(0)

			if "/" in tag:
				tag = tag.replace("/", '')
			
			if ' ' in tag:
				has_attr = True
				tag, attribute = tag.split(" ")[0] + ">", " ".join(tag.split()[1:])
			
			
			if (tag in visited):
				return close
			else:
				n = sampleOutput.index(tag, n+1, close)
				f.write(stack.pop() + "\n")
				
				
		visited.append(tag)
		
		print("Visted: %s" % visited)
		
		tag_value = tag[1:len(tag)-1]
		
		

		if len(re.findall(r"<\/?" + re.escape(tag[1:-1]) + r"( |>)", sampleOutput[n:close])) > 2:
			#here we need to go deeper until it's only one again so that we can get for each values
			for_each_path = nestMapping[tag_value][0].split("/")
			
			f.write('<xsl:for-each select ="%s">\n' % ("/".join(for_each_path[depth:])))
			stack.append("</xsl:for-each>")
			depth = nestMapping[tag_value][1]
			last_for_each = for_each_path[-1]
		
		
		f.write(tag + "\n")
		stack.append(tag[0:1] + "/" + tag[1:])
		
		
		
		if has_attr: 
			
			first_one = True
			for individual_attr in attribute.split("="):
				if first_one:
					first_one = False
				elif ">" in individual_attr:
					break
				else:
					individual_attr = individual_attr.split("\" ")[1]
				
				f.write('<xsl:attribute name="%s">' % individual_attr)
			
				temp_tag = (tag.split(" ")[0])[1:]
				if temp_tag[-1] == ">":
					temp_tag = temp_tag[:-1]
				
				f.write(writeValueOf(depth, temp_tag + "/" + individual_attr, last_for_each, tagMapping))
				f.write('</xsl:attribute>')
			
			
		if tag_value in tagMapping:
			
			f.write(writeValueOf(depth, tag_value, last_for_each, tagMapping))
		
		
		
		
		close = sampleOutput.index((tag[0:1] + "/" + tag[1:]), n+1)
		
		while n < close:
			n = parseXmlOut(n, close, depth)
		return close
		
	#END parseXmlOut
	
	
	
	
	###START###
	

	#Open the sample output file
	f = open(sample_output_file, "r")
	sampleOutput = f.read()
	f.close()

	#Declare parameters
	stack = deque()
	visited = []
	close = len(sampleOutput)
	global last_for_each
	last_for_each = ""
	depth = 0

	#Open XSL file and write standard file opener
	f = open("current.xslt", "w+")
	f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
	f.write('<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">\n')
	stack.append('</xsl:stylesheet>')
	f.write('\t<xsl:output omit-xml-declaration="yes" indent="yes"/>\n')
	f.write('<xsl:template match ="/">\n')
	stack.append('</xsl:template>')



	firstTag = re.search('<[^?](.*?)>', sampleOutput).group(0)
	n = sampleOutput.index(firstTag)-1
	
	
	parseXmlOut(n, close, depth)

	#Close all open tags by popping remainder of stack
	while len(stack) > 0:
		f.write(stack.pop() + "\n")
	f.close()
