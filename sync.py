import os
from smugmug import Smugmug

DATADIR = './data'
smugmug = Smugmug()
albums = smugmug.get_albums()

def process_subfolder(year):
	print("Processing %s..." % year.name)
	# todo: get a list of files in the gallery from smugmug
	# todo: if gallery with the year name does not exist, create it

	# ...for performance reasons it might be better to just save a text file in the directory
	# of which files were already uploaded lol
	with os.scandir(year) as i:
		for filename in i:
			# if filename was already uploaded, skip
			print(filename)

with os.scandir(DATADIR) as i:
	for filename in i:
		if filename.is_dir():
			process_subfolder(filename)
