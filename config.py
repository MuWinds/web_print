import os
import base64
BASE_DIRS=os.path.dirname(__file__)
options={
    'port':8000,
}
settings={
    'static_path':os.path.join('static',BASE_DIRS),
    'cookie_secret':base64.b64encode('printer'.encode('utf-8')),
    'template_path':os.path.join(BASE_DIRS,'templates'),
    'debug':True,
    'login_url':'/user-login',
}