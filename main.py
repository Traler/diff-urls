#!/usr/bin/python3

import PySimpleGUI as sg
import re
import pyperclip

sg.theme('SandyBeach')

regex = r"[^&?]*?=[^&?]*"

def getData(link1, link2):
	parsedLink1 = re.finditer(regex, link1, re.MULTILINE)
	parsedLink2 = re.finditer(regex, link2, re.MULTILINE)

	dic = {}

	for match in parsedLink1:
		keyValue = match.group().split("=")
		key = keyValue[0]
		value = keyValue[1]

		dic[key] = [value, ""]

	for match2 in parsedLink2:
		keyValue = match2.group().split("=")
		key = keyValue[0]
		value = keyValue[1]

		if key in dic:
			dic[key][1] = value;
		else:
			dic[key] = ["", value];

	return dic

def createTable(data):
	layout = []

	layout.append([
			sg.Text("", size=(15, 1), font='Lucida',justification='right'),
			sg.Text("Url1", size=(15, 1), font='Lucida',justification='right'),
			sg.Text("", size=(15, 1), font='Lucida',justification='right'),
			sg.Text("Url2", size=(15, 1), font='Lucida',justification='right')
	])

	col = []

	for key in data:
		params = data[key]
		color = "white"
		if params[0] == params[1]:
			color = "#63a947"
		col.append([
			sg.Text(key, size=(15, 1), font='Lucida',justification='right'),
			sg.Input(params[0], background_color=color),
			sg.Input(params[1], background_color=color),
		])

	layout.append([sg.Column(col, size=(900,1000), scrollable="True")])
	layout.append([sg.Cancel()])

	window = sg.Window('py-diff compare urls', layout)

	while True:
	   event, values = window.read()
	   if event == sg.WIN_CLOSED or event == 'Cancel':
	      break
	window.close()

def createWindow():
	windowLayout = [
	    [sg.Text('Enter urls')],
	    [
			sg.Text('Url1', size =(15, 1)), 
			sg.Multiline(key="inputURL1", size=(60, 20), expand_y="True", expand_x="True"),
 			sg.Button("Copy", key="copyURL1"), 
 			sg.Button("Clear", key="clearURL1")
 		],
	    [
	    	sg.Text('Url2', size =(15, 1)), 
	    	sg.Multiline(key="inputURL2", size=(60, 20), expand_y="True", expand_x="True"),
	    	sg.Button("Copy", key="copyURL2"), 
	    	sg.Button("Clear", key="clearURL2")
	    ],
	    [sg.Button("Compare")],
	    [sg.Cancel()]
	]

	window = sg.Window('py-diff compare urls', windowLayout)

	while True:
		event, values = window.read()
		if event == sg.WIN_CLOSED or event == 'Cancel':
			window.close()	
			break
		if event == sg.WIN_CLOSED or event == 'Compare':
			createTable(getData(values["inputURL1"], values["inputURL2"]))

		if event == "copyURL1":
			pyperclip.copy(values["inputURL1"])
		if event == "copyURL2":
			pyperclip.copy(values["inputURL2"])

		if event == "clearURL1":
			window['inputURL1'].update('')
		if event == "clearURL2":
			window['inputURL2'].update('')
	window.close()
createWindow()
