from app.api.view_common import CommHandeler
import tornado.gen
import  tornado.concurrent
class IndexHandler(CommHandeler):
    @tornado.gen.coroutine
    def get(self,*arg,**kwargs):
        yield self.get_response()

    @tornado.concurrent.run_on_executor # thread pool
    def get_response(self,*args,**kwargs):
        self.write("<h1 style=‘color:blue’>这是API接口</h1>")
        self.write("<h1 style=‘color:red’>{}</h1>".format(str(self.md)))