# -*- coding: utf-8 -*-
from os import listdir
import jinja2
from PIL import Image
from tqdm import tqdm # fancy progress bar 😍

# set up templating engine
templateLoader = jinja2.FileSystemLoader( 'templates/' )
templateEnv = jinja2.Environment( loader=templateLoader )

importFolder = 'import';
exportFolder = 'cloud';

thumbnail_sizes = [ (100, 100), (250, 250), (500, 500) ]

clouds = []
print( "Processing new clouds..." )
for file in tqdm( listdir( importFolder ) ):
	img = Image.open( importFolder + '/' + file )
	size = 50, 50
	img.thumbnail( size )
	thumbnail_path = exportFolder + '/' + file + '.thumbnail'
	img.save( thumbnail_path, "JPEG" )
	url = importFolder + '/' + file
	clouds.append( { 'url': url, 'thumbnail': thumbnail_path } )

# clouds = [ {
# 	'url': file,
# 	'thumbnail': importFolder + '/' + file
# } for file in listdir( importFolder ) ]

# output folder structure = by date?

# write a top-level page with an index
template = templateEnv.get_template( 'index.html.j2' )

with open( 'index.html', 'w' ) as index_html:
	index_html.write( template.render( clouds=clouds ) )

print( "All done!" )