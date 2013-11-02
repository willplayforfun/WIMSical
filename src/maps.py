#!/usr/bin/env python

import webapp2
import entityList
from Crypto.Hash import MD5
from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import db

domain = "http://hack-tj.appspot.com"
fb_client_id = "404564209651865"
fb_client_secret = "038fbf3dd6e023ecc462dc772510fc47"
auth_page = "/auth"

def handle_login(request):
	code = request.get('	')
	if code:
		#facebook stuff
		validation = urlfetch.fetch("https://graph.facebook.com/oauth/access_token?client_id="+\
										fb_client_id+"&client_secret="\
										+fb_client_secret+"&redirect_uri="\
										+domain+auth_page+"&code="+code).content
		if 'access_token' in validation:
			try:
				token = validation[validation.find("="):validation.find("&expires")]
				return {"redirect":'/',"cookies":[('loginid',hash_userid(token)),('auth','fb')]}
			finally:
				#This should never happen
				pass
	goog = request.get('goog')
	if goog:
		if users.get_current_user():
			return {"redirect":'/',"cookies":[('loginid',hash_userid(users.get_current_user().user_id())),('auth','goog')]}
		else:
			#This should never happen
			pass
	logout = request.get('logout')
	if logout=='1':
		return {"redirect":'/',"cookies":[('loginid','')]}
	return {"redirect":'/'}
	