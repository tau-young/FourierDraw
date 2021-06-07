from Tkinter import *
import tkFileDialog
import os

# Building GUI
console = Tk()
console.title("FourierDraw - Console")
guiFileLabel = Label(console, text="SVG File Address:")
guiFileLabel.grid(row=0, column=0, sticky=E)
guiFileEntry = Entry(console)
guiFileEntry.grid(row=0, column=1, columnspan=3, sticky=W)
guiNumbLabel = Label(console, text="Pair of epicycloids:")
guiNumbLabel.grid(row=1, column=0, sticky=E)
guiNumbEntry = Entry(console)
guiNumbEntry.grid(row=1, column=1, sticky=W)
guiTolLabel = Label(console, text="Tolerance:")
guiTolLabel.grid(row=1, column=2, sticky=E)
guiTolEntry = Entry(console)
guiTolEntry.grid(row=1, column=3, sticky=W)
guiAnyMessage = Label(console, text="")
guiAnyMessage.grid(row=2, column=0, columnspan=4, sticky=W)

# Initializing
<<<<<<< Updated upstream
filename = '/Users/tauyoung/Documents/GitHub/fourier/assets/peace.svg'
=======
# filename = '/Users/tauyoung/Documents/GitHub/fourier/assets/peace.svg'
>>>>>>> Stashed changes
numberOfEpicycloids = 128
tol = 1e-3

# Checking argv
from sys import argv
if len(argv) >= 2:
	filename = argv[1]
if len(argv) >= 3:
	numberOfEpicycloids = int(argv[2])
if len(argv) >= 4:
	tol = float(argv[3])
# guiFileEntry.insert(0, filename)
guiNumbEntry.insert(0, numberOfEpicycloids)
guiTolEntry.insert(0, tol)

# Processing anything
def process(filename, numberOfEpicycloids, tol):
	# Reading SVG
	from svgpathtools import svg2paths
	paths, attributes = svg2paths(filename)

	# Creating Canvas
	c = Canvas(console, width=540, height=540)
	c.grid(row=3, column=0, columnspan=5)

	# Calculating coefficients
	import cmath
	nsum = int(round(1/tol))
	points = [0] * (nsum + 1)
	coeff = [0] * (numberOfEpicycloids * 2 + 1)
	for thisPath in paths:
		for t in range(nsum + 1):
			points[t] = thisPath.point(t * tol)
		for n in range(-numberOfEpicycloids, numberOfEpicycloids + 1):
			csum = 0
			for t in range(nsum):
				csum += cmath.exp(-n * 2 * cmath.pi * 1j * t * tol) * points[t]
			coeff[n] = csum * tol
		
		# Clearing tags for this path
		try:
			for i in range(-numberOfEpicycloids, numberOfEpicycloids + 1):
				c.delete(arrows[i], epicys[i])
		except:
			"Skip"
		
		# Calculating coordinates
		coord = [0] * (numberOfEpicycloids * 2 + 1)
		coord[0] = coeff[0]
		for i in range(1, numberOfEpicycloids + 1):
			coord[-i] = coord[i-1] + coeff[-i]
			coord[i] = coord[-i] + coeff[i]

		# Draw fourier series
		epicys = [0] * (numberOfEpicycloids * 2 + 1)
		arrows = [0] * (numberOfEpicycloids * 2 + 1)
		for i in range(1, numberOfEpicycloids + 1):
			arrows[-i] = c.create_line(coord[i-1].real, coord[i-1].imag, coord[-i].real, coord[-i].imag, arrow=LAST)
			epicys[-i] = c.create_oval(coord[i-1].real - abs(coeff[-i]), coord[i-1].imag - abs(coeff[-i]), coord[i-1].real + abs(coeff[-i]), coord[i-1].imag + abs(coeff[-i]))
			arrows[i] = c.create_line(coord[-i].real, coord[-i].imag, coord[i].real, coord[i].imag, arrow=LAST)
			epicys[i] = c.create_oval(coord[-i].real - abs(coeff[-i]), coord[-i].imag - abs(coeff[i]), coord[-i].real + abs(coeff[i]), coord[-i].imag + abs(coeff[i]))
		c.create_rectangle(int(coord[i].real), int(coord[i].imag), int(coord[i].real) + 1, int(coord[i].imag) + 1)
		c.update()

		# Animation
		for t in range(1, nsum + 1):
			for i in range(1, numberOfEpicycloids + 1):
				coord[-i] = coord[i-1] + coeff[-i] * cmath.exp(-i * 2 * cmath.pi * 1j * t * tol)
				coord[i] = coord[-i] + coeff[i] * cmath.exp(i * 2 * cmath.pi * 1j * t * tol)
			for i in range(1, numberOfEpicycloids + 1):
				c.coords(arrows[-i], coord[i-1].real, coord[i-1].imag, coord[-i].real, coord[-i].imag)
				c.coords(epicys[-i], coord[i-1].real - abs(coeff[-i]), coord[i-1].imag - abs(coeff[-i]), coord[i-1].real + abs(coeff[-i]), coord[i-1].imag + abs(coeff[-i]))
				c.coords(arrows[i], coord[-i].real, coord[-i].imag, coord[i].real, coord[i].imag)
				c.coords(epicys[i], coord[-i].real - abs(coeff[i]), coord[-i].imag - abs(coeff[i]), coord[-i].real + abs(coeff[i]), coord[-i].imag + abs(coeff[i]))
			c.create_rectangle(int(coord[i].real), int(coord[i].imag), int(coord[i].real) + 1, int(coord[i].imag) + 1)
			c.update()

# Listening for changes
from threading import Thread
threadChange = Thread(target=process)

# Interface binded functions
def fileSelector(nul):
	guiFileEntry.insert(0, tkFileDialog.askopenfilename(initialdir=os.getcwd(), title="Select file", filetypes=(("Scalable Vector Graphics", "*.svg"),)))

def checkAndRun(nul):
	""" global filename
	global numberOfEpicycloids
	global tol
	if (filename, numberOfEpicycloids, tol) == (guiFileEntry.get(), int(guiNumbEntry.get()), float(guiTolEntry.get())) and drawn:
		return """
	(filename, numberOfEpicycloids, tol) = (guiFileEntry.get(), int(guiNumbEntry.get()), float(guiTolEntry.get()))
	try:
		filePointer = open(filename, 'r')
		filePointer.close()
		guiAnyMessage.config(text="Drawing " + filename + " with " + str(numberOfEpicycloids * 2) + " epicycloids...")
	except Exception as err:
		# guiAnyMessage.config(text="Error: File not found " + filename)
		guiAnyMessage.config(text=err)
		return
	process(filename, numberOfEpicycloids, tol)

# Binding Events
guiFileEntry.bind('<FocusIn>', fileSelector)
guiFileEntry.bind('<FocusOut>', checkAndRun)
guiNumbEntry.bind('<FocusOut>', checkAndRun)
guiTolEntry.bind('<FocusOut>', checkAndRun)
console.bind_all('<Return>', checkAndRun)
console.mainloop()

# TODO: Create Canvas based on the saize of the SVG file
# TODO: Scale too large or too small image to the proper size
# TODO: Draw multiple paths