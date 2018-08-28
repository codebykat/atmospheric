# -*- coding: utf-8 -*-
import glob
import jinja2
import os
from PIL import Image
from tqdm import tqdm # fancy progress bar 😍

# set up templating engine
templateLoader = jinja2.FileSystemLoader( 'templates/' )
templateEnv = jinja2.Environment( loader=templateLoader )

importFolder = 'import/';
exportRoot = 'docs/'
exportFolder = 'cloud/';

thumbnail_sizes = [ (100, 100), (250, 250), (500, 500) ]

def get_image_folder( uid, relative=True ):
	if relative:
		return exportFolder + uid + '/'
	return exportRoot + exportFolder + uid + '/'

def get_image_filename( uid, size='full' ):
	return uid + '-' + size + '.jpg'

def get_image_path( uid, size='full', relative=True ):
	return get_image_folder( uid, relative ) + get_image_filename( uid, size )

clouds = []
print( "Processing new clouds..." )
for file in tqdm( glob.glob( importFolder + '*.jpg' ) ):
	uid = os.path.splitext( os.path.basename ( file ) )[0]

	image_folder = get_image_folder( uid, False )
	if not os.path.exists( image_folder ):
		os.makedirs( image_folder )

	img = Image.open( file )

	# copy full-sized image into export folder
	img.save( get_image_path( uid, 'full', False ), "JPEG" )

	# generate and save thumbnail
	size = 50, 50
	img.thumbnail( size )

	img.save( get_image_path( uid, 'thumb', False ), "JPEG" )

	clouds.append( {
		'url': get_image_path( uid ),
		'thumbnail': get_image_path( uid, 'thumb' )
	} )

# clouds = [ {
# 	'url': file,
# 	'thumbnail': importFolder + '/' + file
# } for file in listdir( importFolder ) ]

# output folder structure = by date?

# write a top-level page with an index
print ( "Writing index page..." )
template = templateEnv.get_template( 'index.html.j2' )

with open( exportRoot + '/index.html', 'w' ) as index_html:
	index_html.write( template.render( clouds=clouds ) )

print( "All done!" )