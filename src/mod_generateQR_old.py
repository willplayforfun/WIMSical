#!/usr/bin/env python
#
#	Function: Generates QR
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageColor, ImageChops, ImageEnhance
import StringIO
import logging
from google.appengine.api import urlfetch

homeURL='http%3A%2F%2Fhack-tj.appspot.com%2Ffound%3Fid%3D'

def overlay( qrImage, dim ):

	#	### TEXT OVERLAYS ###
	textDim = (int(dim * .9), int(dim * .1))

	#	### FONT COPYING ###
	fontSize = {150:12, 250:20, 1000:80}[dim]

	ifFoundTextWrapper = Image.new('L', textDim);
	ImageDraw.Draw(ifFoundTextWrapper).text((0, 0), "Scan if found.", font=ImageFont.truetype('./fonts/Purisa.ttf', fontSize), fill='white')
	ifFoundTextWrapper = ImageOps.colorize(ifFoundTextWrapper, (255, 255, 255), (0, 0, 0))

	websiteTextWrapper = Image.new('L', textDim);
	ImageDraw.Draw(websiteTextWrapper).text((0, 0), "hack-tj@appspot", font=ImageFont.truetype('./fonts/Purisa.ttf', fontSize - 5), fill='white')
	websiteTextWrapper = ImageOps.colorize(websiteTextWrapper, (255, 255, 255), (0, 0, 0))

	#	### LOGO OVERLAY ###

	#logoURL = urlfetch.fetch('http://hack-tj.appspot.com/static/images/logo.png')
	#logoWrapper = Image.open( StringIO.StringIO( logoURL.content ) ).resize((int(dim * .15), int(dim * .15)), Image.ANTIALIAS)

	qrImage.paste(ifFoundTextWrapper, (int((dim - textDim[0]) / 2.), 5));
	qrImage.paste(websiteTextWrapper, (int((dim - textDim[0]) / 2.), dim - 5 - textDim[1]));

	#qrImage.paste(logoWrapper, (int(dim * .85), int(dim * .85)))

	return qrImage

def content_qr( deviceID, doOverlay=False, dim=250):

	qrGeneratorURL = 'https://chart.googleapis.com/chart?chs=' + str(dim) + 'x' + str(dim) + '&cht=qr&chl='

	urlContent = urlfetch.fetch(qrGeneratorURL + homeURL + str(deviceID) + '%0A')

	deviceQR = Image.open( StringIO.StringIO( urlContent.content ) )

	if (doOverlay):
		deviceQR = overlay( deviceQR, dim )

	#	### LOGO OVERLAY ###

	logoURL = urlfetch.fetch('http://hack-tj.appspot.com/static/images/logo.png')
	logoWrapper = Image.open( StringIO.StringIO( logoURL.content ) ).resize((int(dim * .15), int(dim * .15)), Image.ANTIALIAS)
	deviceQR.paste(logoWrapper, (int(dim * .85), int(dim * .85)))

	#	### SAVING TO PNG ###
	output = StringIO.StringIO()
	deviceQR.save( output, 'PNG' )
	contents = output.getvalue()
	output.close()

	return {'content-type': 'image/png', 'image': contents}

def jinja_qr ( deviceID ):

	return {'filename': 'qr.html',	'vals': {'did': deviceID, 'url': homeURL + str(deviceID)}}