import os
import re
import filecmp
import time


currentPath = "" + os.getcwd()

def getMonth(month):
	months = ["01 - Jan", "01 - Feb", "03 - Mar", "04 - Apr",
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
	#Break it into sections based on collens, it is easy to get the date that way
	allPicturesBrokenApart = allPictures.split(":")
	#Remove the last value to make it even
	allPicturesBrokenApart.remove(allPicturesBrokenApart[len(allPicturesBrokenApart) - 1])
	fileInfoList= []
	i = 0
	nextNumber = 0
	#Break the huge list into lists for each file, each one has 15 fields and that is why we break at 15
	while( i < len(allPicturesBrokenApart)/15):
		fileInfoList.append(allPicturesBrokenApart[nextNumber:nextNumber + 15])
		nextNumber = nextNumber + 15
		i = i + 1
	#For each file we want to get its name, fix it's metadata (the YYYY:MM:DD format seems to be broken sometimes and is YYYY:MMDD:DD)
	#I take the :MMDD: (which is at index 11) and only take the first two values which is MM and replace the meta data with a new YYYY:DD
	for files in fileInfoList:
		#The name is at index 1, just getting rid of the stuff around it
		name = files[1].split("\n")
		name = name[0][1:name[0].__len__()]
		fixMetaDataCommand = currentPath + "/./Jhead -ds" + files[10][1:5] + ":" + files[11][0:2] + " " + name
		#For some reason it only works if I do it twice
		os.system(fixMetaDataCommand)
		os.system(fixMetaDataCommand)
	print("Finished fixing MetaData")
	print("")

if __name__ == '__main__':
	fixMetaData()
	renameImagesWithMetaData()
	sortImages()
	print(" ")