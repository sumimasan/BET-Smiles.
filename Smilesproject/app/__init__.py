import tornado.web
import  tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.options import  options,define

from app.configs import  configs,mongodb_configs
from app.urls import urls

from pymongo import MongoClient
define('port',default=8003,help="运行端口")

class CustomApp(tornado.web.Application):
    def __init__(self,urls,configs):
        settings = configs
        handlers =urls
        self.md =MongoClient(host=mongodb_configs['db_host'],
                             port=mongodb_configs['db_port'])
        super(CustomApp,self).__init__(handlers=handlers,**settings)
"""create server"""
def create_server():
    tornado.options.parse_command_line()
    http_sever =tornado.httpserver.HTTPServer(
        CustomApp(urls,configs),xheaders = True
    )
    http_sever.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()