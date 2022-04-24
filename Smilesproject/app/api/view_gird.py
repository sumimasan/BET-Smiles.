from app.api.view_common import CommHandeler
import  tornado.concurrent
import  tornado.gen


class GridHandler(CommHandeler):
    @tornado.gen.coroutine
    def get(self):
        yield  self.get_response()

    @tornado.concurrent.run_on_executor
    def get_response(self):
        grid={
            'style': 'width:50%',
            'data':[
                {
                  'cate': 1,
                  'name': 'BD1预测示例',
                  'image': self.site_url + "/static/images/BD1.jfif",
                  'url': '/pages/BD1/BD1?cate=1&uuid='
                  },
                {
                'cate': 2,
                'name': 'BD2预测示例',
                'image': self.site_url + "/static/images/BD2.jfif",
                'url': '/pages/BD1/BD1?cate=2&uuid='
                }
            ]
        }
        self.write(grid)