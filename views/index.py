import sys
sys.path.append('..')
import tornado.web
import application
import random
import base64
import os
import config
import threading
import tornado.ioloop
import win32api
import win32print
import time
BASE_DIR=os.path.join(config.BASE_DIRS,'media')
def my_gencoroutine(func):
    def wrapper(*args,**kwargs):
        gen_func=func(*args,**kwargs)
        def run(gen):
            res=next(gen)
            try:
                gen_func.send(res)
            except StopIteration as e:
                pass
        threading.Thread(target=run,args=(gen_func,)).start()
    return wrapper
@my_gencoroutine
def uploadfile(file_metas):
    def run(file_metas):
        for meta in file_metas:
            file_name = meta['filename']
            file_name=check_file_name(file_name)
            file_path = os.path.join(BASE_DIR, file_name)
            with open(file_path, 'wb') as f:
                f.write(meta['body'])
            default_printers = "FF K570h for DocuPrint CP105 b"  #获取默认打印机
            print(default_printers)                             #print
            print(file_path)
            open(file_path, "r")
            win32api.ShellExecute (
            0, #父窗口的句柄，如果没有父窗口，则为0
            "print",#要进行的操作，为“open”、“print”或者为空  printto为指定打印机,需要设置第4行参数
            file_path,#要打印的文件
            default_printers,
            ".",#程序初始化的目录
            0 #是否显示窗口
            )
    yield run(file_metas)
def check_file_name(file_name):
    global n
    n=0
    def check_name(filename):
        global n
        file_new_name = filename
        if os.path.isfile(os.path.join(BASE_DIR, filename)):
            file_new_name = filename[:filename.rfind('.')]+ '_'+str(n) + filename[filename.rfind('.'):]
            n+= 1
        if os.path.isfile(os.path.join(BASE_DIR, file_new_name)):
            file_new_name = check_name(file_new_name)
        return file_new_name
    res=check_name(file_name)
    return res
class MainHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user=self.get_secure_cookie('user')
        return user
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.write('hello，正在跳转')
        self.redirect('/user-uploadfile')
class UserRegisterHanlder(tornado.web.RequestHandler):
    def post(self, *args, **kwargs):
        context={}
        email=self.get_argument('email',default=None)
        password=self.get_argument('password')
        password_again=self.get_argument('password_again')
        if len(password)<8:
            context['password_length_error']='密码至少8个字符'
        if password_again!=password:
            context['password_input error']='两次密码输入不一致'
        else:
            db = application.Application().db
            password=base64.b64decode(password.encode('utf-8'))
            sql='insert into user (password) values (%s)'
            db.insert(sql,password)
            account=random.randint(10000000,99999999)
            sql=' insert into user_info (account,email) values (%s,%s)'
            db.insert(sql,account,email)
            context['status']='200'
        self.write(context)
class UserLoginHandler(tornado.web.RequestHandler):
    def get(self, *args, **kwargs):
        return self.render('login.html')
    def post(self, *args, **kwargs):
        db = application.Application().db
        context={}
        email=self.get_argument('email',default=None)
        input_password=self.get_argument('password',default=None)
        sql="select password from user where id = (select id from user_info where email = %s)"
        cursor = db.cursor()
        cursor.execute(sql,email)
        password=cursor.fetchone()
        if input_password.encode('utf-8') == password[0].encode('utf-8'):
            self.set_secure_cookie('user',email)
            #context['authenticated']='200'
            self.redirect('/user-uploadfile')
        else:
            context['authenticated']='500'
            context['password'] = password
            self.write(context)
class UserUploadFileHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        self.user=self.get_secure_cookie('user')
        return self.user
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('uploadfile.html')
    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        context={'status':'500'}
        file_metas=self.request.files.get('file',None)
        try:
            uploadfile(file_metas)
            for file_meta in file_metas:
                file_name=file_meta['filename']
                file_name=check_file_name(file_name)
                context['status']='200'
        except Exception as e:
            print(e)
        self.write(context)
        self.finish()