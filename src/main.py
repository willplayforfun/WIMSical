#!/usr/bin/env python

import webapp2
import jinja2
import os
from google.appengine.ext import db
import datetime
import logging
import time

import mod_generateQR
import mod_device
import mod_devices
import userlib
import mod_login
import mod_found
import mod_account

import entityList

import Cookie

root_dir = os.path.dirname(__file__)

template_dir = os.path.join(root_dir, "templates")
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
							   autoescape = False)
							   
class MainHandler(webapp2.RequestHandler):
	
	@webapp2.cached_property
	def jinja2(self):
		return jinja2.get_jinja2(app=self.app)
	
	def get(self, *params):
		
		logging.info("\n\n GET \n")
		
		mobile = False
		agent = self.request.headers.get('user_agent')
		if "Mobile" in agent:
			mobile = True
		
		url = []
		if params[0]:
			# logging.info( "\n\n URL: %s \n" % str(params) )
			url = params[0].split('/')
			if url[-1]=='': url.pop()
			# logging.info( "\n\n URL: %s \n" % str(url) )
		
		logging.info( "\n\n URL: %s \n" % str(url) )
		# self.response.write( str(url) )
		
		AJAX = self.request.get('ajax')
		user_name = None
		if self.request.cookies.get('loginid'):
			user_name = userlib.get_user(self.request.cookies)
		
		if AJAX:
			logging.info( "\n\n AJAX \n")
		
		title = "Error"
		template_dict = {'filename':'notfound.html', 'vals':{} }
		
		if not user_name:
			title = "WIMSical"
			template_dict = mod_login.login(self.request.cookies)
		
		if len(url)>0:
			
			#BASIC HTML PAGES
			
			if url[0]=='about':
				title = "About WIMSical"
				logging.info("\n\n ABOUT \n")
				template_dict = {'filename':'about.html', 'vals':{} }
			
			elif url[0]=='howto':
				title = "How to WIMSical"
				logging.info("\n\n HOWTO \n")
				template_dict = {'filename':'howto.html', 'vals':{} }
			
			elif url[0]=='serialhelp':
				title = "Serial Number Help"
				logging.info("\n\n SERIALHELP \n")
				template_dict = {'filename':'serialhelp.html', 'vals':{} }
			
			elif url[0]=='qrtips':
				title = "QR Code Tips"
				logging.info("\n\n QRTIPS \n")
				template_dict = {'filename':'qrtips.html', 'vals':{} }
				
			#UNLOCKED PAGES
			
			elif url[0]=='auth': #Authentication
				title = "Authenticate"
				logging.info("\n\n AUTH \n")
				template_dict = userlib.handle_login(self.request)
			
			elif url[0]=='login': #Login Screen
				if not user_name:
					title = "Login"
					logging.info("\n\n LOGIN \n")
					template_dict = mod_login.login(self.request.cookies)
				else:
					title = "Your Device List"
					user_obj = userlib.get_user(self.request.cookies)
					user_id = None if not user_obj else user_obj.key()
					logging.info("\n\n DEVICES (%s) \n" % user_id)
					template_dict = mod_devices.lookup_devices(user_id)
					
			elif url[0]=='found': #Found device page
				title = "Found a Device"
				email = self.request.get('email')
				nickname = self.request.get('nickname')
				phone = self.request.get('phone')
				location = self.request.get('loc')
				device_id = self.request.get('id')
				logging.info("\n\n FOUND (%s) \n" % device_id)
				if not email and not nickname and not phone and not location:
					template_dict = mod_found.found(device_id, user_name)
				else:
					template_dict = mod_found.found(device_id, user_name, nickname, email, phone, location, get=False)
					
			elif url[0]=='qrcode':
				device_id = self.request.get('id')
				logging.info("\n\n QR CODE IMAGE (%s) \n" % device_id)
				template_dict = mod_generateQR.content_qr(device_id)
			
			elif url[0]=='logout': #Logout utility page
				logging.info("\n\n LOGOUT \n")
				self.redirect('/auth?logout=1')
				
			#LOCKED PAGES
			
			elif url[0]=='device' and user_name: #Single device page
				title = "Device Page"
				device_id = self.request.get('id')
				logging.info("\n\n DEVICE (%s) \n" % device_id)
				template_dict = mod_device.getID(device_id, self.request.cookies)
				
			elif url[0]=='remove' and user_name: #Device deletion utility page
				device_id = self.request.get('id')
				logging.info("\n\n DELETE (%s) \n" % device_id)
				device = entityList.Device.get_by_id(int(device_id))
				if device.owner.key().id() == user_name.key().id():
					db.delete(device)
				template_dict = {'redirect':'/devices/'}
				
			elif url[0]=='missing' and user_name: #Device missing utility page
				device_id = self.request.get('id')
				logging.info("\n\n MISSING (%s) \n" % device_id)
				device = entityList.Device.get_by_id(int(device_id))
				if device.owner.key().id() == user_name.key().id():
					device.ismissing = True
					device.date_lost = datetime.datetime.now()
					device.put()
				template_dict = {'redirect':'/devices/'}
				
			elif url[0]=='unmissing' and user_name: #Device unmissing utility page
				device_id = self.request.get('id')
				logging.info("\n\n UNMISSING (%s) \n" % device_id)
				device = entityList.Device.get_by_id(int(device_id))
				if device.owner.key().id() == user_name.key().id():
					device.ismissing = False
					device.finder = None
					device.date_lost = None
					device.put()
				template_dict = {'redirect':'/devices/'}
			
			elif url[0]=='devices' and user_name:
				title = "Your Device List"
				user_obj = userlib.get_user(self.request.cookies)
				user_id = None if not user_obj else user_obj.key()
				logging.info("\n\n DEVICES (%s) \n" % user_id)
				template_dict = mod_devices.lookup_devices(user_id)
				
			elif url[0]=='add' and user_name:
				title = "Add a Device"
				logging.info("\n\n ADD \n")
				template_dict = {'filename':'add.html', 'vals':{'description':'', 'name':'', 'price':''} }
				
			elif url[0]=='account' and user_name:
				title = "Your Account"
				logging.info("\n\n ACCOUNT \n")
				template_dict = mod_account.account(user_name)
			
		else:
			if not user_name:
				title = "Login"
				logging.info("\n\n LOGIN \n")
				template_dict = mod_login.login(self.request.cookies)
			else:
				title = "Your Device List"
				user_obj = userlib.get_user(self.request.cookies)
				user_id = None if not user_obj else user_obj.key()
				logging.info("\n\n DEVICES (%s) \n" % user_id)
				template_dict = mod_devices.lookup_devices(user_id)
		
		# title=params[0]
		page_class = None
		self.mainFunc(template_dict, params[0], user_name, page_class, mobile, title, AJAX)
	
	def post(self, *params):
		logging.info("\n\n POST \n")
		
		mobile = False
		agent = self.request.headers.get('user_agent')
		if "Mobile" in agent:
			mobile = True
		
		url = []
		if params[0]:
			url = params[0].split('/')
			if url[-1]=='': url.pop()
		
		logging.info( "\n\n URL: %s \n" % str(url) )
		
		page_class = None
		title = ""
		
		user_name = None
		if self.request.cookies.get('loginid'):
			user_name = userlib.get_user(self.request.cookies)
		
		template_dict = {'filename':'notfound.html', 'vals':{} }
		if user_name:
			if len(url)>0:
				if url[0]=='add' and user_name:
					title = "Add a Device"
					#verify input
					name = self.request.get('name')
					description = self.request.get('description')
					price = self.request.get('price')
					if name:
						price_num = 0
						try: price_num = float(price)
						except: logging.info( "\n\n Bad Price Value: %s \n" % str(price) )
						new_device = entityList.Device(serial_number = name, owner = user_name, ismissing=False, price = int(price_num), description=description)
						new_device.put()
						device_id = new_device.key().id()
						self.redirect('/device?id=%s' % device_id)
						return
					else:
						# page_class
						template_dict = {'filename':'add.html', 'vals':{'description':description, 'name':'', 'price':price} }
				elif url[0]=='found':
					title = "Found a Device"
					email = self.request.get('email')
					nickname = self.request.get('nickname')
					phone = self.request.get('phone')
					location = self.request.get('loc')
					device_id = self.request.get('id')
					template_dict = mod_found.found(device_id, user_name, nickname, email, phone, location, get=False)
				elif url[0]=='account' and user_name:
					email = self.request.get('email')
					phone = self.request.get('phone')
					location = self.request.get('address')
					title = "Your Account"
					logging.info("\n\n ACCOUNT \n")
					template_dict = mod_account.account(user_name, email, location, phone)
				
		self.mainFunc(template_dict, params[0], user_name, page_class, mobile, title, False)
	
	def mainFunc(self, template_dict, url, user, page, mobile, title, ajax):
		#set cookies
		if 'cookies' in template_dict:
			logging.info("\n\n Setting cookies, %s \n" % str(template_dict['cookies']))
			for cookie in template_dict['cookies']:
				c = Cookie.SimpleCookie()
				c[cookie[0]] = cookie[1]
				st = c.output()
				self.response.headers.add_header('Set-Cookie',cookie[0]+'='+cookie[1]+';')
		
		if 'redirect' in template_dict:
			logging.info("\n\n Redirecting to %s \n" % str(template_dict['redirect']))
			self.redirect(template_dict['redirect'])
			return
			
		if 'image' in template_dict:
			self.response.headers['Content-Type'] = template_dict['content-type']
			self.response.out.write(template_dict['image'])
			return
		
		
		"""
		#should we redirect
		if 'REDIRECT' in template_dict:
			logging.info("\n\n Redirecting to %s \n" % str(template_dict['REDIRECT']))
			self.redirect(template_dict['REDIRECT'])
		elif 'IMG' in template_dict:
			self.redirect(template_dict['IMG'])
		else:
		"""
		if template_dict:
			#render appropriate template
			page = ''
			if 'filename' in template_dict:
				logging.info("\n\n RENDERING (%s) \n" % template_dict['filename'])
				page_template = jinja_env.get_template(template_dict['filename'])
				page = page_template.render(template_dict['vals'])
			
			# if ajax:
				# self.response.out.write(page)
				# return
			
			framework_template = jinja_env.get_template("header.html")
			
			framework_template_dict = {}
			framework_template_dict['vals'] = { 'title': title,
												'titleHTML': title,
												'image': '',
												'url': url,
												'description': '',
												'loggedIn': (user!=None),
												'name': user,
												'element': page,
												'mobile': mobile}
			framework_template_dict['vals']['content'] = page
			
			framework_page = framework_template.render(framework_template_dict['vals'])
			
			#send reponse
			self.response.out.write(framework_page)
			return
		else:
			logging.info("\n\n OMG HOLY SHIT NO TEMPLATE DICT \n")
# URLs that satisfy the below regex
dir_list = [('/?([A-Za-z0-9/]+)?/?', MainHandler)]
app = webapp2.WSGIApplication(dir_list, debug=True)
