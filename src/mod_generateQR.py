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
from google.appengine.api import urlfetch

homeURL='http%3A%2F%2Fhack-tj.appspot.com%2Ffound%3Fid%3D'

def content_qr( deviceID, doOverlay=False, dim=250):

	qrGeneratorURL = 'https://chart.googleapis.com/chart?chs=' + str(dim) + 'x' + str(dim) + '&cht=qr&chl='
	urlContent = urlfetch.fetch(qrGeneratorURL + homeURL + str(deviceID) + '%0A')
	deviceQR = Image.open( StringIO.StringIO( urlContent.content ) )

	#	### LOGO OVERLAY ###
	
	# overlayURL = None
	# if int(entityList.Device.get_by_id(int(deviceID)).price) > 0:
	overlayURL = urlfetch.fetch('http://hack-tj.appspot.com/static/images/qrcodeoverlay_yesreward.bmp', 'RGB')
	# else:
		# overlayURL = urlfetch.fetch('http://hack-tj.appspot.com/static/images/qrcodeoverlay_noreward.bmp', 'RGB')
	overlayWrapper = Image.open( StringIO.StringIO( overlayURL.content ) )

	deviceQR = ImageChops.darker(deviceQR, overlayWrapper)

	#	### SAVING TO PNG ###
	output = StringIO.StringIO()
	deviceQR.save( output, 'PNG' )
	contents = output.getvalue()
	output.close()

	return {'content-type': 'image/png', 'image': contents}
#	### SAVING TO PNG ###
	output = StringIO.StringIO()
	deviceQR.save( output, 'PNG' )
	contents = output.getvalue()
	output.close()
	return {'content-type': 'image/png', 'image': contents}

def jinja_qr ( deviceID ):

	return {'filename': 'qr.html',	'vals': {'did': deviceID, 'url': homeURL + str(deviceID)}}