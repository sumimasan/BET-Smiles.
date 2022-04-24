from app.admin.view_index import IndexHandler as admin_index
from app.api.view_index import IndexHandler as api_index
from app.api.view_user import UserHandler as api_user
from app.api.view_gird import GridHandler as api_grid
from app.api.view_predict import PredictHandler as api_predict
# API接口
api_urls =[
    (r'/',api_index),
    (r'/user/',api_user),
    (r'/predict/',api_predict),
    (r'/grid/',api_grid)
]

# 后台系统
admin_urls =[
    (r'/admin/',admin_index)
]
urls =api_urls+admin_urls