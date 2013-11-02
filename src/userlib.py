#!/usr/bin/env python

import webapp2
import entityList
import json
from Crypto.Hash import MD5
from google.appengine.api import urlfetch
from google.appengine.api import users
from google.appengine.ext import db

domain = "http://hack-tj.appspot.com"
fb_client_id = "404564209651865"
fb_client_secret = "038fbf3dd6e023ecc462dc772510fc47"
auth_page = "/auth"

def handle_login(request):
	code = request.get('code')
	if code:
		#facebook stuff
		validation = urlfetch.fetch("https://graph.facebook.com/oauth/access_token?client_id="+\
										fb_client_id+"&client_secret="\
										+fb_client_secret+"&redirect_uri="\
										+domain+auth_page+"&code="+code).content
		if 'access_token' in validation:
			try:
				token = validation[validation.find("=")+1:validation.find("&expires")]
				content = urlfetch.fetch("https://graph.facebook.com/me?access_token="+token).content
				data = json.loads(content)
				id = data['id']
				return {"redirect":'/',"cookies":[('loginid',hash_userid(id)),('auth','fb'),('fbtoken',token)]}
			finally:
				#This should never happen
				pass
	goog = request.get('goog')
	if goog:
		if users.get_current_user():
			return {"redirect":'/',"cookies":[('loginid',hash_userid(users.get_current_user().user_id())),('auth','goog')]}
		else:
			#This should never happen
			logging.error("BURP: USERLIB LINE 40 GOOGLE AUTH FAILURE")
			pass
	logout = request.get('logout')
	if logout=='1':
		return {"redirect":'/',"cookies":[('loginid','')]}
	return {"redirect":'/'}
	
def get_login_urls():
	urls = {}
	urls['fb'] = "https://www.facebook.com/dialog/oauth?client_id="+fb_client_id+"&redirect_uri="+domain+auth_page
	urls['goog'] = users.create_login_url(dest_url=domain+auth_page+"?goog=1")
	return urls

def get_logout_url(cookies):
	if 'auth' in cookies and cookies['auth']=='goog':
		return users.create_logout_url(dest_url=domain+auth_page+"?logout=1")
	return domain+auth_page+"?logout=1"

def get_user(cookies):
	if 'loginid' in cookies:
		loginid = cookies['loginid']
		resp = db.GqlQuery("SELECT * "
						   "FROM Account "
						   "WHERE my_id=:1",loginid)
		usr = resp.get()
		if not usr:
			if 'auth' in cookies and cookies['auth']=='fb':
				data = json.loads(urlfetch.fetch("https://graph.facebook.com/me?access_token="+cookies['fbtoken']).content)
				users_name = str(data['first_name'])
			elif 'auth' in cookies and cookies['auth']=='goog':
				users_name = str(users.get_current_user().nickname())
			else:
				users_name = 'Good Sire'
			entityList.Account(my_id=loginid,key_name=loginid,nickname=users_name).put()
		return usr
	else:
		return None
	
def hash_userid(userid):
	h = MD5.new()
	h.update(userid)
	return str(h.hexdigest())