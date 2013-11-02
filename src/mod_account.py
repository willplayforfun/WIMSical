def account(user_obj, email=None, address=None, phone=None):
	if email:
		user_obj.email=email
	else:
		email=user_obj.email
	if address:
		user_obj.loc=address
	else:
		address=user_obj.loc
	if phone:
		user_obj.phone=phone
	else:
		phone=user_obj.phone
	user_obj.put()
	return {'filename':'account.html', 
		    'vals':{'email':user_obj.email if user_obj.email else "", 'address': user_obj.loc if user_obj.loc else "", 'phone':user_obj.phone if user_obj.phone else ""}}
	