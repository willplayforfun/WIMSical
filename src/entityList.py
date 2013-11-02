from google.appengine.ext import db

class Account(db.Model):
	fb_id=db.StringProperty()
	my_id=db.StringProperty()
	goog_id=db.StringProperty()
	email=db.StringProperty()
	nickname=db.StringProperty()
	phone=db.StringProperty()
	loc=db.StringProperty()
	
class Device(db.Model):
	serial_number=db.StringProperty(required=True)
	description=db.StringProperty(required=False)
	date_lost = db.DateTimeProperty(required=False)
	ismissing = db.BooleanProperty(required=True)
	owner = db.ReferenceProperty(Account)
	price = db.IntegerProperty(required=False)
	finder = db.IntegerProperty()