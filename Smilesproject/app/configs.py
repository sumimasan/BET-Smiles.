import  os

root_path =os.path.dirname(__file__)

configs=dict(
    static_path = os.path.join(root_path,'static'),
    debug=True
)

#mongodb 配置
mongodb_configs=dict(
    db_host="127.0.0.1",
    db_port= 27017
)