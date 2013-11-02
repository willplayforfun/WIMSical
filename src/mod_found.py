from google.appengine.ext import db
import userlib
import entityList

def found(deviceID, user_obj, findername=None,finderemail=None,finderphone=None,finderloc=None,get=True):
	validDID = False
	try:
		temp = int(deviceID)
		validDID = True
	except: pass
	
	if not deviceID or not validDID:
		return {'filename': 'found.html',
				'vals': {'noid': True}}
	else:
		device = entityList.Device.get_by_id(int(deviceID))
		if not device:
			return {'redirect':'/found/'}
		if user_obj and device.owner.key().id() == user_obj.key().id():
			return {'redirect':'/device/?id=%s' % deviceID}
		
		if device.ismissing == False:
			return {'filename': 'found.html',
					'vals': {'ismissing':False,
							 'finder': user_obj}}
			
		if user_obj:	#Someone is logged in currently
			if user_obj.email or user_obj.phone:
				device.finder = user_obj.key().id()
				device.put()
				return {'filename': 'found.html',
						'vals': {'thanks': True,
								'ismissing':True,
								 'finder': user_obj}}
			
			else:
				return {'filename': 'found.html',
						'vals': {'missingfield': True,
								 'reward': device.price if device.price else '0',
								 'ismissing':True,
								 'did':deviceID,
								 'finder': user_obj}}
								 
		elif finderemail or finderphone:	#Nobody logged in currently, but form from found.html is filled out correctly
		
			user_obj = entityList.Account(my_id=deviceID, nickname=findername, email=finderemail, phone=finderphone, loc=finderloc)
			user_obj.put()
			device.finder = user_obj.key().id()
			device.put()
			return {'filename': 'found.html',
					'vals': {'thanks': True,
							'ismissing':True,
							 'finder': user_obj}}
			
		else:	#Nobody logged in currently, form not filled out
			return {'filename': 'found.html',
						'vals': {'missingfield': True,
								 'reward': device.price if device.price else '0',
								 'ismissing':True,
								 'did':deviceID,
								 'finder': user_obj}}

#EOF
