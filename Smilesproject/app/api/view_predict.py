from app.api.view_common import CommHandeler
import  tornado.concurrent
import  tornado.gen
import os
import  datetime
import uuid
from app.models.Smiles_BRD4 import BRD4
from bson.objectid import ObjectId
import numpy as np
import pandas as pd
import xlrd
import numpy as np
import pandas as pd
import keras
from keras.layers import Input, Add, Dense, Activation, ZeroPadding2D, LayerNormalization, Flatten, AveragePooling2D, MaxPooling2D, GlobalMaxPooling2D
from keras.models import Model, load_model
from keras.layers import Dense, Dropout
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from sklearn.utils import shuffle
from keras.models import Sequential, Model
from keras.layers import Conv2D, MaxPooling2D, Input, GlobalMaxPooling2D
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.optimizers import Adam
from keras.callbacks import ReduceLROnPlateau
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from sklearn.model_selection import KFold
from copy import deepcopy
from keras import backend as K #转换为张量
from keras import optimizers
import os
from app.models.Model_gui import main
from app.models.read_image import show_image



# 测试
# print("res:",BRD4().predict)

class PredictHandler(CommHandeler):
    @tornado.gen.coroutine
    def post(self):
        yield self.post_response()

    @tornado.concurrent.run_on_executor
    def post_response(self):
        self.write(self.save_image())

    def make_upload_dir(self):
        upload_path =os.path.join(
            os.path.dirname(
            os.path.dirname(__file__)
            ),
            r'static\uploads'
        )
        if not os.path.exists(upload_path):
            os.mkdir(upload_path)
        return upload_path

    @property
    def dt(self):
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    @property
    def image_name(self):
        """date + unique id  composed the name of the picture """
        prefix1 = self.dt
        prefix2 = uuid.uuid4().hex
        return prefix1+prefix2

    def upload_image(self):
        # acquire image from client
        files=self.request.files['img']
        imgs_http,imgs_name=[],[]
        upload_path = self.make_upload_dir()
        imgs_http, imgs_name=self.save_upload_image(files,upload_path,imgs_http,imgs_name)
        return imgs_http, imgs_name,upload_path

    def save_upload_image(self,files,upload_path,imgs_http,imgs_name):
        for file in files:
            newname=self.image_name+os.path.splitext(file['filename'])[-1] # get the format of the image
            imgs_name.append(newname)
            img_path = os.path.join(upload_path,newname)
            with open(img_path,'wb') as up:
                up.write(file['body'])
            imgs_http.append(self.site_url+'/static/uploads/{}'.format(newname))
        return imgs_http,imgs_name


    def save_image(self):
        res ={'code':0}
        imgs_http, imgs_name, upload_path =self.upload_image()
        cate_type =self.get_argument('cate',None)
        cate_type =int(cate_type)
        model = BRD4()
        # show_image()
        # main()
        if cate_type==1:
                known =model.predict()
                print(known)
                name = 'BD1活性预测'
        elif cate_type ==2:
                known = model.predict()
                name ='BD2活性预测'
        db = self.md.Smiles_project
        record =db.image.insert_one(
            dict(
                image = imgs_http,
                # known = list (
                #     # map(
                #     #     lambda v : self.site_url+"/static/uploads/{}".format(v),
                #     #     known
                #     # ),
                #
                # ),
                predict_val = known,
                name = name,
                cate=cate_type,
                status = 0,
                # **self.common_param
            )
        )
        last_id = record.inserted_id
        if last_id:
            res={
                'code':1,
                'cate':cate_type,
                'uuid':str(last_id)
            }
        return res

    def get_image(self,uid):
        image_data=dict()
        db=self.md.Smiles_project
        record =db.image.find_one({'_id':ObjectId(uid)}) # the function of uid is searching
        image_data['cate']=record['cate']
        image_data['image'] = record['image']
        image_data['name']=record['name']
        image_data['predict_val']=record['predict_val']
        return image_data

    @tornado.gen.coroutine
    def get(self,*args,**kwargs):
        yield self.get_response()

    def get_response(self):
        # question ?
        uid =self.get_argument('uuid',None)
        # call the get_image to execute the prediction
        if uid:
            self.write(self.get_image(uid))
        else:
            cate = self.get_argument('cate',1)
            data ={
                1:{
                    'cate':1,
                    'name':'BD1 预测示例',
                    'image':[self.site_url+"/static/images/structure.png"],
                    'url':'/pages/BD1/BD1?cate=1&uuid=',
                    'predict_val':'NS(=O)(=O)C1=CC=C(NC2=NC3=C(C=CC=C3)C(C3=CC=C(Cl)C=C3)=N2)C=C1 : 3.37 um/L'
                },
                2: {
                    'cate': 2,
                    'name': 'BD2 预测示例',
                    'image': [self.site_url + "/static/images/structure.png"],
                    'url':'/pages/BD1/BD1?cate=2&uuid='
                }
            }
            self.write(data[int(cate)])
