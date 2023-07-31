import tornado.web
from views import index
from config import settings
import pymysql
class Application(tornado.web.Application):
    def __init__(self):
        handlers=[
            (r'/',index.MainHandler),
            (r'/user-login',index.UserLoginHandler),
            (r'/user-uploadfile',index.UserUploadFileHandler),
        ]
        super(Application,self).__init__(handlers,**settings)
        self.db=pymysql.Connection(host='127.0.0.1',user='printer',password='printerpassword',database='printer')
