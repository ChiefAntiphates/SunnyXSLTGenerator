from sunny_functions_xml import *
from sunny_functions_txt import *
from sunny_functions_csv import *
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename as tkfile
import lxml.etree
from playsound import playsound
from threading import Thread


'''Global vars:'''
process = "Generate" #<- determines if application is in state to generate new XSLT or execute old XSLT
inputFile = "" #<- user selected input file for both generate and execute
outputFile = "" #<- user selected output file for generate or XSLT file for execute




'''Function to open tk file dialogue and set the global input file variable, 
then updating the text widget in root'''
def selectInputFile():
	global inputFile
	filename = tkfile()
	inputFile = filename
	labelIn.config(text=inputFile.split("/")[-1], bg="SeaGreen1", fg="black")


'''Function to open tk file dialogue and set the global output file variable, 
then updating the text widget in root'''
def selectOutputFile():
	global outputFile
	filename = tkfile()
	outputFile = filename
	labelOut.config(text=outputFile.split("/")[-1], bg="SeaGreen1", fg="black")


def selectMostRecent():
	global outputFile
	outputFile = "most_recent.xslt"
	labelOut.config(text="most_recent.xslt", bg="SeaGreen1", fg="black")
	
	

'''Destroy the root windows and go to the XML output XSLT generator function'''	
def letsGoGenerate():
	if (inputFile == ""):
		messagebox.showwarning("Warning","You have not selected a template input file.")
	elif (outputFile == ""):
		messagebox.showwarning("Warning","You have not selected a template output file.")
	
	else:
		#Here validate the filenames and depending on output type trigger the correct function
		print(outputFile)
		output_extension = outputFile.split(".")[-1]
		if output_extension == "txt":
			root.destroy()
			transformToText(inputFile, outputFile)
		elif output_extension == "csv":
			root.destroy()
			transformToCsv(inputFile, outputFile)
		elif output_extension == "xml":
			root.destroy()
			getXmlMappingValues(inputFile, outputFile)
		else:
			print("ERROR")
			messagebox.showwarning("Warning - Incompatible File Type","The file type of output file is not compatible.\nPlease select a txt, csv, or xml file.")
		
	
	
'''Execute the selected XSLT file on the selected XML input file, 
then output the file in plaintext and give the option of saving the generated file'''	
def letsGoExecute():
	if (inputFile == ""):
		messagebox.showwarning("Warning","You have not selected an input file.")
	elif (outputFile == ""):
		messagebox.showwarning("Warning","You have not selected an XSLT file.")
	elif (outputFile.split(".")[-1] != "xsl" and outputFile.split(".")[-1] != "xslt"):
		print(outputFile.split(".")[-1])
		print(outputFile)
		messagebox.showwarning("Warning","The transform file you selected is not XSLT, please select an XSLT file.")
	else:
		transform_input = lxml.etree.parse(inputFile) #<- lxml parsed object of input XML file
		transform = lxml.etree.XSLT(lxml.etree.parse(outputFile)) #<- lxml object of XSLT file selected by user
		transform_output = transform(transform_input) #<- generated plaintext output of the user selected XSLT being executed on the user input
		print(transform_output)
		
		transform_window = tk.Toplevel(root)#New window for displaying and saving the generated output from the chosen XSLT
		tk.Label(transform_window, text="%s transformed with %s" % (inputFile.split("/")[-1], outputFile.split("/")[-1])).grid(row=0, column=0)#display input filename and XSLT filename
		tk.Button(transform_window, text="Save as", command = lambda: setFilePath(transform_output)).grid(row=0, column=1)
		tk.Button(transform_window, text="Close", command = lambda x= transform_window: x.destroy()).grid(row=0, column=2)
		transform_text = tk.Text(transform_window, width = 120)
		transform_text.grid(row=1, column=0, columnspan=3)
		transform_text.insert(tk.END, transform_output)
		transform_text.config(state=tk.DISABLED)
	
def setFilePath(write_to):
	f = tksave()
	print(f)
	
	if (f != None):
		file_path_selected = True
		f.write(str(write_to))
		tkalert.showinfo("Generated","All done! Your generated file is now in your chosen file location!")
	else:
		tkalert.showwarning("Warning","File not saved. Please try again.")
	f.close()
	
def clearVars():
	global inputFile
	global outputFile
	inputFile = ""
	outputFile = ""
	labelIn.config(text="--", fg="red", bg="white")
	labelOut.config(text="--", fg="red", bg="white")

def switch():
	clearVars()
	global process
	if process == "Generate":
		process = "Execute"
		button_in.config( text="Select Input File")
		button_out.config(text="Select XSLT File")
		button_recent.grid(row=4, column=2)
		button_go.config(text="Begin Execution!", command=letsGoExecute)
	else:
		process = "Generate"
		button_in.config( text="Select Template Input File")
		button_out.config(text="Select Template Output File")
		button_recent.grid_forget()
		button_go.config(text="Begin Transform!", command=letsGoGenerate)
	chosen_method.config(text="%s XSLT File" % process)
	chosen_method.config(text="%s XSLT File" % process)
	root.update()
	
def howToGenerateHelp():
	print("help section here")
	helpWindow = tk.Toplevel(root)
	helpWindow.title('Help')
	helpWindow.grid_columnconfigure(0, weight=1)
	help_text = tk.Text(helpWindow)
	help_text.grid(row=0, column=0, sticky="news")
	f = open("help_files/help_generate.txt", "r")
	help_content = f.read()
	f.close()
	help_text.insert(tk.END, help_content)
	help_text.config(state=tk.DISABLED)
	

	
def readAloudFunction():

	def generateSound():
		playsound("sounds/generate_xslt.wav")
		
	def executeSound():
		playsound("sounds/execute_xslt.wav")
		
	global process
	if process == "Generate":
		Thread(target = generateSound).start()
	else:
		Thread(target = executeSound).start()
		
		
	

root = tk.Tk()
root.minsize(600, 175) 
root.maxsize(600, 175) 
root.configure(bg="#ffe26e")

##Create a frame to center all widgets
frame = tk.Frame(root)
frame.pack()
frame.configure(bg="#ffe26e")
root.title('Sunny XSLT Generator')
root.iconbitmap('sunny.ico')
button_in = tk.Button(frame, text="Select Template Input File", command=selectInputFile)
#button_in.pack()
button_in.grid(row=2, column=0)

button_out = tk.Button(frame, text="Select Template Output File", command=selectOutputFile)
#button_out.pack()
button_out.grid(row=2, column=2)



button_recent = tk.Button(frame, text="Select Most Recent", command=selectMostRecent, bg="#50acde")




button_go = tk.Button(frame, text="Begin Transform!", command=letsGoGenerate)
button_go.grid(row=1, column=1, pady=(20,0), padx=20)

chosen_method = tk.Label(frame, text="%s XSLT File" % process, font='Calibri 18 bold', bg="#ffe26e")
chosen_method.grid(row=0, column=1)



labelIn = tk.Label(frame, text="--", fg="red", bg="white")
labelIn.grid(row=3, column=0)
labelOut = tk.Label(frame, text="--", fg="red", bg="white")
labelOut.grid(row=3, column=2)

menu_bar = tk.Menu(root)

options_menu = tk.Menu(menu_bar, tearoff=0)
options_menu.add_command(label="Switch to Generate/Execute XSLT File", command=switch)
menu_bar.add_cascade(label="Select Mode", menu=options_menu)

options_menu2 = tk.Menu(menu_bar, tearoff=0)
options_menu2.add_command(label="How do I generate an XSLT file?", command=howToGenerateHelp)
options_menu2.add_command(label="Read Aloud", command=readAloudFunction)
menu_bar.add_cascade(label="Help", menu=options_menu2)


root.config(menu=menu_bar)
root.mainloop()