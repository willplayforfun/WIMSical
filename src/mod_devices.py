#!/usr/bin/env python

from google.appengine.ext import db
import userlib

def lookup_devices( key ):

	deviceList = list(db.GqlQuery('SELECT * FROM Device WHERE owner=:1', key))

	retval = {'filename': 'devices.html',
			'vals': {'devices': deviceList,
			'deviceCount': len(deviceList),
			'userName': ""}}
	for device in range(len(deviceList)):
		retval['vals']['devices'][device] = {'obj':retval['vals']['devices'][device],'id':retval['vals']['devices'][device].key().id(),'date_lost':(retval['vals']['devices'][device].date_lost.strftime('%B %d, %Y') if retval['vals']['devices'][device].date_lost else '')}
	return retval
