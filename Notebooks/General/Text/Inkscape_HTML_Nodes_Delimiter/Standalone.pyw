"""Script delimiting Inkscape's HTML node points
Can be used as both CLI and GUI"""
from sys import *; del path
from os import *; del open
from subprocess import call
from tkinter import Tk, messagebox as msgbox, filedialog as fd
chdir(path.abspath(path.dirname(__file__)))

#---#

__author__	= "kubinka0505"
__credits__	= __author__
__version__	= "1.0"
__date__	= "02.08.2021"

#---#

root = Tk()
root.withdraw()

#---#

def Folder_Size():
	"""Calculates folder size recursively"""
	Size = 0
	for Root, Dirs, Files in walk("."):
		for File in Files:
			Path = path.join(Root, File)
			if not path.islink(Path):
				Size += path.getsize(Path)
	return Size

def File_Size(Bytes: float) -> str:
	"""Returns human-readable file size"""
	for Unit in ["B", "KB", "MB", "GB"]:
		if Bytes < 1024.: break
		Bytes /= 1024.
	return "{0} {1}".format(round(Bytes, 2), Unit)

#---#

try:
	try:
		File = argv[1]
	except IndexError:
		File = fd.askopenfilename(
			initialdir = getcwd(),
			filetypes = [
				("Hypertext Markup Language Files", "*.html *htm"),
				("All Files", "*.*")
			]
		)
	if File:
		File = open(path.abspath(File), encoding = "U8")
	else:
		raise IndexError
except IndexError:
	exit("No file given!")

Folder_Name = File.name.split(".")[0] + "_Nodes"

#---#

Content	= File.read()
Content	= Content.replace("\t", "")
Begin	= Content.find("ctx.moveTo(")
Content	= Content[Begin:].split("ctx.fill(")[0].strip().split("\n")

#---#

Formats = ("HTM", "HTML")
if not File.name.upper().endswith(Formats):
	try:
		raise OSError("Only single simple webpages format files are supported ({0})".format(
			", ".join(Formats).strip()
			)
		)
	except Exception as Error:
		msgbox.showerror(
			title = Error.__class__.__name__,
			message = Error
			)
		exit("{0}: {1}".format(Error.__class__.__name__, Error))

for Line in Content:
	if "ctx.bezier" in Line:
		try:
			raise AttributeError("SVG file contains bezier curves")
		except Exception as Error:
			msgbox.showerror(
				title = Error.__class__.__name__,
				message = Error
				)
			exit("{0}: {1}".format(Error.__class__.__name__, Error))

try:
	mkdir(Folder_Name)
except FileExistsError:
	pass
chdir(Folder_Name)

#---#

X = "\n".join([Line.split(", ")[1].split(");")[0] for Line in Content])
X += "{0}{1}{0}".format("\n", X.split("\n")[0])

Y = "\n".join([Line.split("(")[1].split(",")[0] for Line in Content])
Y += "{0}{1}{0}".format("\n", Y.split("\n")[0])

open("X.txt", "w", encoding = "U8").write(X)
open("Y.txt", "w", encoding = "U8").write(Y)

#---#

Message = "Successfully {0} nodes ({1})\n\nDo You want to open containing folder?".format(
	len([Line for Line in Content]),
	File_Size(Folder_Size())
	)

print(Message.split("\n")[0] + "\a")
Message = msgbox.showinfo(
	title = "Success",
	message = Message
)

#---#

Command = "nautilus"
if platform.startswith("win"):
	Command = "start /max"

if Message == "ok":
	call(Command + " .", shell = True)
