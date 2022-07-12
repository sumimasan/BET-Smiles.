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


class BRD4:
    # def read_test(self):
    def read_train(self):
        train_file_path ='../models/train_check.csv'
        train_df = pd.read_csv(train_file_path)
        self.X_train_smiles = np.array(list(train_df["SMILES"]))
        assay1 = "BRD4-BD1"
        Y_train = train_df[assay1].values
        self.Y_train = np.array(Y_train)
        dic_df = pd.read_csv('../models/train_check.csv')
        self.charset = set("".join(list(dic_df.SMILES)) + "!E")
        """为字符构建索引"""
        self.char_to_int = dict((c, i) for i, c in enumerate(self.charset))
        self.int_to_char = dict((i, c) for i, c in enumerate(self.charset))
        self.embed = max([len(smile) for smile in dic_df.SMILES]) + 5  # 最长的len(smiles)
        self.vocab_size =len(self.charset)
        return self.embed,self.charset

    def vectorize(self, smiles, embed, charset, char_to_int,flag=0):
        if flag:
            print("one simple")
            one_hot =np.zeros((embed-1),dtype =np.int8)
            one_hot[0] =char_to_int["!"]
            for j, c in enumerate(smiles):
                one_hot[j+1]=char_to_int[c]
            for i in range(j+1,embed-1):
                one_hot[i]= char_to_int["E"]
            return one_hot

        else:
            one_hot = np.zeros((smiles.shape[0], embed, len(charset)), dtype=np.int8)
            # 为所有数据生成形状为（embed，len(charset))的onehot编码,
            for i, smile in enumerate(smiles):
                # encode the start char 开始编码为！
                one_hot[i, 0, char_to_int["!"]] = 1
                # encode the rest of the chars
                for j, c in enumerate(smile):
                    one_hot[i, j + 1, char_to_int[c]] = 1
                # Encode endchar 结束编码为 E
                one_hot[i, len(smile) + 1:, char_to_int["E"]] = 1
            # Return two, one for input and the other for output
            return one_hot[:, 0:-1, :], one_hot[:, 1:, :]

    def model(self):
        model = Sequential()
        model.add(Embedding(self.vocab_size, 100, input_length=self.embed - 1))  # embeding
        model.add(keras.layers.Conv1D(512, 10, activation='relu'))  # Conv1D
        model.add(LayerNormalization())
        model.add(keras.layers.Conv1D(256, 5, activation='relu'))
        model.add(keras.layers.Conv1D(128, 3, activation='relu'))
        model.add(Flatten())
        model.add(Dense(1024, activation='relu'))  # Dense 输出256维度
        model.add(Dropout(0.1))
        model.add(Dense(64, activation='relu'))  # Dense 输出64维度
        model.add(Dropout(0.1))
        model.add(Dense(1, activation='linear'))
        model.compile(loss="mse", optimizer=Adam(lr=0.0001))
        return model

    def train(self):
        embed ,charcset = self.read_train()
        X_train,_=self.vectorize(smiles=self.X_train_smiles,embed=embed,charset=charcset,char_to_int=self.char_to_int)
        # Y_train,_= self.vectorize(smiles=self.Y_train,embed= self.embed,charset=self.charset,char_to_int=self.char_to_int)
        X_train = K.cast_to_floatx(X_train)
        Y_train = K.cast_to_floatx(self.Y_train)
        callbacks_list = [
            EarlyStopping(monitor="loss", patience=10),
            ReduceLROnPlateau(monitor='loss', factor=0.5, patience=5, min_lr=1e-15, verbose=1, mode='auto',
                              cooldown=0),
            ModelCheckpoint(filepath="weights.best.hdf5", monitor='loss', save_best_only=True, verbose=1,
                            mode='auto')
        ]
        model = self.model()
        history = model.fit(x=np.argmax(X_train, axis=2), y=Y_train,
                                batch_size=32,
                                epochs=100,
                               callbacks=callbacks_list)

    @property
    def read_smiles_predict(self):
        filename = r"D:\Working\Python\Smilesproject\app\models\picture_to_smiles.xls"
        wb = xlrd.open_workbook(filename=filename)
        # 通过索引获取表格sheet页
        sheet1 = wb.sheet_by_index(0)
        smiles = sheet1.row(sheet1.nrows - 1)[0].value
        print(smiles)
        print("read success")
        return smiles

    def predict(self):
        charaset ={'=', 'C', 'E', 'O', 'r', '2', 'g', 'N', '3', 'H', '4', 'S', '5', ')', 'F', '!', '(', '#', '+', '-', '1', '@', '*', 'M', 'l', ']', '[', 'B'}
        char_to_int = {'=': 0, 'C': 1, 'E': 2, 'O': 3, 'r': 4, '2': 5, 'g': 6, 'N': 7, '3': 8, 'H': 9, '4': 10, 'S': 11, '5': 12, ')': 13, 'F': 14, '!': 15, '(': 16, '#': 17, '+': 18, '-': 19, '1': 20, '@': 21, '*': 22, 'M': 23, 'l': 24, ']': 25, '[': 26, 'B': 27}
        model_path = r"D:\Working\Python\Smilesproject\app\models\weights.best.hdf5"
        local_model = load_model(model_path)
        X_test_smiles=self.read_smiles_predict
        X_test=np.array(list(X_test_smiles))  # change to list that can be iterable
        X_test =[self.vectorize(X_test,embed=97 ,charset=charaset,char_to_int=char_to_int,flag=1).tolist()]
        # print(X_test)  形状
        result = local_model.predict(X_test)
        result = str(result[0][0]) + ' um/L'
        print(result)
        return X_test_smiles+": "+ result

BRD4().predict
