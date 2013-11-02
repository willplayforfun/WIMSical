import userlib

def login(cookies=None):
	urls = userlib.get_login_urls()
	dict={}
	dict['filename']='login.html'
	dict['vals']={'fbloginURL':urls['fb'],'googloginURL':urls['goog']}
	return dict
	