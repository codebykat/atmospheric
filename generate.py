# -*- coding: utf-8 -*-
import glob
import jinja2
from os import path
from PIL import Image
from tqdm import tqdm # fancy progress bar 😍

# set up templating engine
templateLoader = jinja2.FileSystemLoader( 'templates/' )
templateEnv = jinja2.Environment( loader=templateLoader )

importFolder = 'import/';
exportRoot = 'docs/'
exportFolder = 'cloud/';

thumbnail_sizes = [ (100, 100), (250, 250), (500, 500) ]

clouds = []
print( "Processing new clouds..." )
for file in tqdm( glob.glob( importFolder + '*.jpg' ) ):
	size = 50, 50
	img = Image.open( file )
	img.thumbnail( size )

	filename = path.basename( file )
	file_url = exportFolder + filename

	thumbnail_path = exportRoot + file_url + '.thumbnail'
	img.save( thumbnail_path, "JPEG" )

	thumbnail_url = file_url + '.thumbnail'
	clouds.append( { 'url': file_url, 'thumbnail': thumbnail_url } )

# clouds = [ {
# 	'url': file,
# 	'thumbnail': importFolder + '/' + file
# } for file in listdir( importFolder ) ]

# output folder structure = by date?

# write a top-level page with an index
template = templateEnv.get_template( 'index.html.j2' )

with open( exportRoot + '/index.html', 'w' ) as index_html:
	index_html.write( template.render( clouds=clouds ) )

print( "All done!" )