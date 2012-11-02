import os
import re
import filecmp
import time
import sys


currentPath = "" + os.getcwd()
JheadPath = currentPath + "/./Jhead"
def getMonth(month):
	months = ["01 - Jan", "02 - Feb", "03 - Mar", "04 - Apr",
	"05 - May", "06 - Jun", "07 - July", "08 - Aug", "09 - Sept",
	 "10 - Oct", "11 - Nov", "12 - Dec"]
	month = int(month)
	return months[month - 1]
def getSortedPath(name):
	return currentPath + "/" + name[0:4] + "/" + getMonth(name[4:6]) + "/" + name

def checkIfFile(name,originalName):
	path = getSortedPath(name)
	if (os.path.isfile(path) or os.path.isdir(path)):
		print("Found files with the same name")
		if(filecmp.cmp(currentPath + "/" + originalName, path)):
			print("Duplicate File, Overwriting")
			return False
		print("Renaming new file and sorting")
		return True
	return False

def recursiveMoveToSortedPath(name, originalName):
	if checkIfFile(name,originalName):
		print(name + " " + originalName)
		endOfOldName = name[15:name.__len__()]
		newName = name[0:15] + '-' + endOfOldName
		recursiveMoveToSortedPath(newName,originalName)
		return
	os.renames(originalName,getSortedPath(name))

def moveToSortedPath(name):
	recursiveMoveToSortedPath(name,name)
	
def renameImagesWithMetaData():
	print("Renameing Images:")
	os.system(currentPath + "/./Jhead -nf%Y%m%d-%H%M%S *")
	print("Finished Renaming")
	print("")

def sortImages():
	files = os.listdir(os.getcwd())
	stuffToRemove = []
	for stuff in files:
		if not (re.search('.jpg',stuff)):
			stuffToRemove.append(stuff)
	for stuff in stuffToRemove:
		files.remove(stuff)
	print("Files to sort:")
	print(files)
	print(" ")
	print("Sorting files")
	for picture in files:
		moveToSortedPath(picture)
	print("Finish Sorting")

def fixMetaData():
	print("")
	print("Fixing MetaData")
	#Get the System output
	allPictures = os.popen(currentPath + "/./Jhead *").read()

	allPicturesBrokenApart = allPictures.split("\n")

	fileInfoList= []

	lastValue = 0
	for i in range(len(allPicturesBrokenApart)):
		if allPicturesBrokenApart[i] == "":
			fileInfoList.append(allPicturesBrokenApart[lastValue:i])
			lastValue = i

	fileInfoList.remove([""])
	#For each file we want to get its name, fix it's metadata (the YYYY:MM:DD format seems to be broken sometimes and is YYYY:MMDD:DD)
	#I take the :MMDD: (which is at index 11) and only take the first two values which is MM and replace the meta data with a new YYYY:DD
	for files in fileInfoList:
		name = ""
		date = ""
		for items in files:
			isFileName = items.find("File name    :")
			isDateTime = items.find("Date/Time    :")
			if not isFileName == -1:
				name = items.split(":")[1]
				name = name[1:name.__len__()]
			if not isDateTime == -1:
				date = items.split(":")[1] + ":" + items.split(":")[2]
				date = date[1:8]
		print(name)
		print(date)
		fixMetaDataCommand = currentPath + "/./Jhead -ds" + date + " " + name
		os.system(fixMetaDataCommand)
		os.system(fixMetaDataCommand)
		os.system(fixMetaDataCommand)
		print("")

	print("Finished fixing MetaData")
	print("")

def main():
	if len(sys.argv) > 1:
		if not sys.argv[1] == '0':
			JheadPath = sys.argv[1]
	
	if len(sys.argv) > 2:
		if sys.argv[2] == '0':
			fixMetaData()

	renameImagesWithMetaData()
	sortImages()
	print(" ")

if __name__ == '__main__':
	main()
	