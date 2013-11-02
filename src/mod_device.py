from google.appengine.ext import db
import entityList
def getID(deviceID, cookies=None):
	obj = entityList.Device.get_by_id(int(deviceID))
	if not obj:
		return {'redirect':'/devices/'}
	finder_obj = None
	if obj.finder:
		finder_obj = entityList.Account.get_by_id(int(obj.finder))
	dict={}
	dict['filename']= 'device.html'
	dict['vals']={'did':deviceID, 'device':obj if obj else {}, 'finder_email':finder_obj.email if finder_obj else "", 'finder_phone':finder_obj.phone if finder_obj else ""}
	return dict