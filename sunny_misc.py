import os
import sys
import re
from lxml import etree
import tkinter as tk
from tkinter.filedialog import asksaveasfile as tksave
from tkinter import messagebox as tkalert
from tkinter import Entry
from collections import Counter, deque
import smtplib, ssl, email
from email.mime.text import MIMEText
from functools import partial
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.mime.base import MIMEBase

def getPathValues(filename, values):
	tree = etree.parse(filename)
	value_paths = []
	for i in range(len(values[0])):
		print(values[0][i])
		for tag in tree.iter():
			tag_match = False
			path = tree.getpath(tag)
			rem_path = re.sub(r'\[\d+\]', '', path)
			if (tag.text == values[0][i]):
				possible_paths = [i for i in tree.xpath(rem_path)]
				tick_box = [item[i] for item in values]
				for path in possible_paths:
					if path.text in tick_box:
						tick_box.remove(path.text)
				if tick_box == []:
					tag_match = True
				if tag_match:
					value_paths.append(rem_path)
					break
			else:
				if tag.attrib != {}:
					attr_tags = dict(tag.attrib)
					for attr in attr_tags:
						if attr_tags.get(attr) == values[0][i]:
							##This is giving all the values of this path
							if (set([item[i] for item in values]) == set(tree.xpath("%s/@%s" % (rem_path, attr)))):
								value_paths.append("%s/@%s" % (rem_path, attr))
								tag_match = True
								break
					if tag_match:
						break
	return value_paths
###########################


def getLoopingTag(inputTemplateXml, frequency, value_paths):
		
		all_tags = Counter(re.findall('<(/.*?)[>| ]', inputTemplateXml))
		
		potential_loops = [i[1:] for i in all_tags if all_tags.get(i) == frequency]
		
		further_potentials = []
		
		for tag_name in potential_loops:
			
			valid = False
			for path in value_paths:
				
				if tag_name in path:
					
					valid = True
					break
			if valid:
				further_potentials.append(tag_name)
				
		if len(further_potentials) == 1:
			return further_potentials[0]
		else:
			winner = ""
			left_count = 9999
			for potential in further_potentials:
				for path in value_paths:
					if potential in path:
						path = path.split("/")
						left_index = path.index(potential)
						if left_index < left_count:
							winner = potential
							left_count = left_index
						break
			return winner
	############################	


def creatingCorrectPaths(value_paths, looping_tag):
	for_each_path = "ERROR"
	for i in range(len(value_paths)):
		print("VALUEPATHSi")
		print(value_paths[i])
		if looping_tag in value_paths[i]:
			for_each_path = (value_paths[i][:value_paths[i].index(looping_tag)] + looping_tag)[1:]
			break
	print(for_each_path)

	value_of = []
			
	for path in value_paths:
		if for_each_path in path:
			value_of.append(path.replace("/"+for_each_path+"/", ""))
		else:
			print("here")
			print(path[1:].split("/"))
			path_split = path[1:].split("/")
			print(for_each_path.split("/")[::-1])
			traversable_for_each = (for_each_path.split("/")[::-1])
			up_ticks = 0
			keyword = ""
			for split_bit in traversable_for_each:
				if split_bit in path_split:
					break
				else:
					up_ticks = up_ticks + 1
			values_to_add = []
			for split_bit in path_split:
				if split_bit in traversable_for_each:
					pass
				else:
					values_to_add.append(split_bit)
			up_factor = "../" * up_ticks
			value_of.append(up_factor +  "/".join(values_to_add))
			print(up_factor + "/".join(values_to_add))
			print("here")
			
	return(value_of, for_each_path)



def fileGenerated():
	def setFilePath():
		f = tksave(defaultextension=".xslt")
		print(f)
		if (f != None):
			file_path_selected = True
			f.write(generated_file)
			tkalert.showinfo("Generated","All done! Your generated XSLT file is now in your chosen file location!")
			
			
		else:
			tkalert.showwarning("Warning","File not saved. Please try again.")
		f.close()

	def returnToMain():
		done_window.destroy()
		
		try:
			del sys.modules["sunny_main"]
		except KeyError:
			pass
		import sunny_main
		
	def emailTo():
	
		def submitEmail(receiver_email):
			
			port = 465
			password = "hw00441sunny" ##do something to encrypt or hide this
			sender_email = "sunnyxsltgenerator@gmail.com"
			print("reciever")
			print(receiver_email)##insert error handling here?
			print("reciever")
			
			context = ssl.create_default_context()
			
			filename = "most_recent.xslt"
			
			with open(filename, "rb") as attachment:
				part = MIMEBase("application", "octet-stream")
				part.set_payload(attachment.read())
			
			encoders.encode_base64(part)
			
			part.add_header(
				"Content-Disposition",
				f"attachment; filename= {filename}",
			)
			
			message = MIMEMultipart("alternative")
			message["Subject"] = "Generated XSLT Stylesheet [timestamp]"
			message["From"] = sender_email
			message["To"] = receiver_email
			text = """\
Hi,
			
Please find the new XSLT stylesheet that has been generated attached.
			
Happy transforming!
			
- Sunny XSLT Generator"""
			
			message.attach(MIMEText(text, "plain"))
			message.attach(part)
			
			with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
				server.login(sender_email, password)
				server.sendmail(
					sender_email, receiver_email, message.as_string()
				)
				
			inputwin.destroy()
			tkalert.showinfo("Sent","An email has been sent with the new XSLT file attached!")
			
		inputwin = tk.Toplevel(done_window)
		inputwin.configure(bg="#ffe26e")
		inputwin.title("Send as Email")
		
		inputwin.minsize(300, 100) 
		inputwin.maxsize(300, 100)
		
		tk.Label(inputwin, text="Enter email to send to:", bg="#ffe26e", width=200).pack()
		
		
		enter_box = tk.Entry(inputwin, width=200)
		enter_box.pack()
	
		
		
		
		
		
		tk.Button(inputwin, text="Go", command=lambda : submitEmail(enter_box.get()), fg="blue2").pack()
		
		
		inputwin.mainloop()
		
			
			
			
	#end email function
			

	done_window = tk.Tk()
	done_window.configure(bg="#ffe26e")
	done_window.title("All Generated!")
			
	##title the window and have a button so that you can cancel file dialogue
			
	
	g = open("current.xslt", "r")
	generated_file = g.read()
	g.close()
	os.remove("current.xslt")
	
	h = open("most_recent.xslt", "w")
	h.write(generated_file)
	h.close()
	

	tk.Button(done_window, text="Save as", command=setFilePath, fg="blue2").pack()

	tk.Button(done_window, text="Main Menu", command=returnToMain, fg="blue2").pack()
	
	tk.Button(done_window, text="Send as Email", command=emailTo, fg="blue2").pack()

	generated_text = tk.Text(done_window)
	generated_text.pack()
	generated_text.insert(tk.END, generated_file)
	generated_text.config(state=tk.DISABLED)

			
	done_window.mainloop()