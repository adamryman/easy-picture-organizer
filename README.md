Easy Picture Sorter
========

Thank you Jhead for being awesome! Author: Matthias Wandel Site: http://www.sentex.net/~mwandel/jhead/

Results
------- 
Takes this:
fdasfdas.jpg
img_4.jpg
somethingsomething2012.jpg

And does this!:
(Folder System)
2010
	->02 - Feb
		->20100223-145430.jpg
2011
	->05 - May
		->20110515-174144.jpg
	->09 - Sept
		->20110902-035119.jpg

Useage
------- 

Place jpg images with metadata into the same directory as the script and Jhead.

I had a lot of images with broken metadata, they were in a YYYY:MMDD:DD format. I wrote something to fix that too.

python sortImages.py arg1 arg2

Where arg1 is the path to the executable version of Jhead (0 for default) (not sure if this works on windows) and arg2 is 0 if you want to fix metadata.

By default, the Jhead path is currentDirectory + "/./Jhead" and metadata will not be fixed.

The script will rename images in YYYYMMDD-HHMMSS format without overwriting images taken at the same time.

It will then sort them into folders by year and then month.

Have fun!