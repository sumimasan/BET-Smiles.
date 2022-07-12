import tornado.concurrent
from app.api.view_common import CommHandeler

class UserHandler(CommHandeler):

    def check_xsrf_cookie(self):
        return  True

    @tornado.gen.coroutine
    def  post(self,*args,**kwargs):
        yield self.post_response

    @tornado.concurrent.run_on_executor
    def post_response(self):
        result = dict(
            code =0,
            msg ="request fail"
        )
        data = dict(
            self.param
            **self.common_param
        )
        db = self.md.Smiles_project
        record = db.loginlog.insert_one(data)
        last_id = record.inserted_id
        if last_id:
            result=dict(
                code =1,
                msg="success",
                last_id=str(last_id)
            )
        self.write(result)