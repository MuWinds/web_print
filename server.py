import tornado.ioloop
import tornado.httpserver
import config
from application import Application
if __name__ == '__main__':
    app=Application()
    httpserver=tornado.httpserver.HTTPServer(app)
    httpserver.listen(config.options['port'])
    tornado.ioloop.IOLoop.current().start()