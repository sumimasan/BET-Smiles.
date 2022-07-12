import tornado.web
from concurrent.futures import ThreadPoolExecutor
from app.common.ip2Addr import ip2addr
import  datetime
import json
class CommHandeler(tornado.web.RequestHandler):
    executor = ThreadPoolExecutor(1000)
    @property
    def md(self):
        return self.application.md

    # prefix address
    @property
    def site_url(self):
        return 'http://127.0.0.1:8003'

    @property
    def param(self):
        # minprogram provide json information
        data={
            k:v for k,v in json.load(self.request.body.decode('utf-8')).items()
        }
        return data
    @property
    def dt(self):
        return datetime.datetime.now().strftime("%Y-%M-%D %H:%M:%S")

    @property
    def common_param(self):
        data=dict(
            createAt=self.dt,
            ip=self.request.remote_ip,
            addr = ip2addr(self.request.remote_ip)['region'].decode('utf-8'),
            headers = dict(self.request.headers)
        )
        return data
