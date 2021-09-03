#coding:utf-8
# Author:AlwaysSun
# Time:2021-04

from keras.layers import Dense, LSTM, Dropout, Input, GRU
from keras.utils import to_categorical
from keras.models import Sequential
import numpy as np
from matplotlib import pyplot as plt
import os, keras
from keras.models import Model
import datetime, time
from threading import Thread
from keras.layers.core import Lambda
from typing import *

# parameters for LSTM
# nb_lstm_outputs = 128  #神经元个数
# nb_time_steps = 160  #时间序列长度
# nb_input_vector = 128 #输入序列
'''
目前负载的识别不好 0.2665 0.3333333333333333
output_fault_accuracy, output_loadVal_accuracy

[0.055917358365778484, 0.9666666388511658]
'''


sample_fre = 10000  # 采样频率10000 40960
# data_len=int(sample_fre // 10)#数据长度为0.5s，即为采样频率除以2个点 0.1s   /10
# data_len = int(sample_fre * 0.8)  # 0.8s的数据
data_len = 512#数据长度为0.05s
dataset_len=1000  #保存数据集的个数

now_time_all = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
class NumberLstm():
    count = 0


class MyLstm():
    def __init__(self, data_len,channel=5, nb_lstm_outputs=128, nb_time_steps=data_len // 128,nb_input_vector=128, epoch=100):
        self.data_len = data_len
        self.channel = channel
        self.npy_dir = ['0','1','2','3','4']
        self.channel_str = ['A','B','C']
        #self.loadStr = ['0','500','1000']
        self.loadList = [[1,0,0],[0,1,0],[0,0,1]]
        self.loadSet = set()
        self.x_train = []
        self.y_train = []
        self.x_test = []
        self.y_test = []
        self.x_eval = []
        self.y_eval = []
        #self.mul = mul
        self.model = None
        #self.data_thousand = thousand
        self.nb_lstm_outputs = nb_lstm_outputs
        self.nb_time_steps = nb_time_steps
        self.nb_input_vector = nb_input_vector
        self.epoch = epoch
        #self.y_train_flag = False #标志使得  在getData中self.y_train只添加一次

    def get_now_time(self):
        now_time = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
        return now_time + ".h5"
    def getLoadStr(self,str):
        #print(str)
        a = str.split('_')[1]
        for strIndex in range(len(self.loadStr)):
            if a == self.loadStr[strIndex]:
                return self.loadList[strIndex]
    def getExceptStart(self,str):
        a = str.split('_')
        returnStr = ''
        for i in range(1,len(a)):
            returnStr += ('_' + a[i])
        #print(returnStr)
        return returnStr
    def getData(self,str):#['0','1','2','3','4']
        x_trainA = []
        x_testA = []
        m = [0, 0, 0, 0, 0]
        if str == '0':
            m = [1, 0, 0, 0, 0]
        elif str == '1':
            m = [0, 1, 0, 0, 0]
        elif str == '2':
            m = [0, 0, 1, 0, 0]
        elif str == '3':
            m = [0, 0, 0, 1, 0]
        elif str == '4':
            m = [0, 0, 0, 0, 1]

        npy_file = os.path.join(os.getcwd(),str,'newgenerate')
        for root, dirs,files in os.walk(npy_file):
            for j in files:#每一个文件
                startStr = self.getExceptStart(j)
                if j.startswith('A') and startStr not in self.loadSet:
                    self.loadSet.add(startStr)
                    a = np.load(os.path.join(npy_file,'A'+startStr))
                    b = np.load(os.path.join(npy_file,'B'+startStr))
                    c = np.load(os.path.join(npy_file, 'C' + startStr))
                    for i in range(a.shape[0] * 8 // 10):
                        x_trainA.append(a[i])
                        x_trainA.append(b[i])
                        x_trainA.append(c[i])
                        self.x_train.append(x_trainA)
                        x_trainA = []
                        self.y_train.append(m)
                    for i in range(a.shape[0] * 1 // 10):
                        x_testA.append(a[a.shape[0] * 8 // 10 + i])
                        x_testA.append(b[b.shape[0] * 8 // 10 + i])
                        x_testA.append(c[c.shape[0] * 8 // 10 + i])
                        self.x_test.append(x_testA)
                        x_testA = []
                        self.y_test.append(m)

    def train(self):
        self.y_train_flag = False
        for i in self.npy_dir:
            self.getData(i)
        self.x_train = np.array(self.x_train)
        self.y_train = np.array(self.y_train)
        self.x_test = np.array(self.x_test)
        self.y_test = np.array(self.y_test)
        #print(self.x_train)
        #self.x_eval = np.array(self.x_eval)
        #self.y_eval = np.array(self.y_eval)
        print(self.data_len / 128)
        print(self.x_train.shape)#(4000, 512) (3, 4000, 512)  (14400,4096)->(14400,32,128)  (16000, 3, 512)->(16000, 3, 4, 128)
        print(self.y_train.shape)#(4000, 5) (16000, 5)
        #print(self.y_train)
        self.x_train = self.x_train.reshape(self.x_train.shape[0],self.x_train.shape[1], self.data_len // 128, 128)
        self.x_test = self.x_test.reshape(self.x_test.shape[0],self.x_test.shape[1],self.data_len // 128, 128)
        print(self.x_train.shape)# (16000, 3, 4, 128)
        print(self.y_train.shape)# (16000, 5)
        input_1 = Input((self.data_len // 128, 128), name='input1')
        x_1 = input_1
        x_1 = Dense(64, activation='relu')(x_1)
        x_1 = GRU(units=self.nb_lstm_outputs, input_shape=(self.nb_time_steps, self.nb_input_vector),
                return_sequences=False)(x_1)
        #x_1 = Dense(128, activation='relu')(x_1)
        #x1_1 = Dense(64, activation='relu')(x_1)
        #output_fault_1 = Dense(5, activation='softmax', name='output_fault')(x1_1)

        input_2 = Input((self.data_len // 128, 128), name='input2')
        x_2 = input_2
        x_2 = Dense(64, activation='relu')(x_2)
        x_2 = GRU(units=self.nb_lstm_outputs, input_shape=(self.nb_time_steps, self.nb_input_vector),
                  return_sequences=False)(x_2)
        #x_2 = Dense(128, activation='relu')(x_2)
        #x2_2 = Dense(64, activation='relu')(x_2)
        #output_fault_2 = Dense(5, activation='softmax', name='output_fault')(x2_2)

        input_3 = Input((self.data_len // 128, 128), name='input3')
        x_3 = input_3
        x_3 = Dense(64, activation='relu')(x_3)
        x_3 = GRU(units=self.nb_lstm_outputs, input_shape=(self.nb_time_steps, self.nb_input_vector),
                  return_sequences=False)(x_3)
        #x_3 = Dense(128, activation='relu')(x_3)
        #x3_3 = Dense(64, activation='relu')(x_3)
        #output_fault_3 = Dense(5, activation='softmax', name='output_fault')(x3_3)

        weight_1 = Lambda(lambda x: x * 0.3)
        weight_2 = Lambda(lambda x: x * 0.3)
        weight_3 = Lambda(lambda x: x * 0.4)
        weight_gru1 = weight_1(x_1)
        weight_gru2 = weight_2(x_2)
        weight_gru3 = weight_3(x_3)
        last = keras.layers.Add()([weight_gru1, weight_gru2, weight_gru3])

        last = Dense(128, activation='relu')(last)
        x_11 = Dense(64, activation='relu')(last)
        x_12 = Dense(64, activation='relu')(last)
        output_fault = Dense(5, activation='softmax', name='output_fault')(x_11)
        #load_val = Dense(3, activation='softmax', name='output_loadVal')(x_12)#负载值

        self.model = Model(inputs=[input_1,input_2,input_3], outputs= output_fault)
        self.model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.model.summary()
        print(self.x_train[:,0,:,:].shape)
        self.H = self.model.fit(x={'input1': self.x_train[:,0,:,:],'input2': self.x_train[:,1,:,:],'input3': self.x_train[:,2,:,:]},
                                y={'output_fault': self.y_train}, epochs=self.epoch,
                                batch_size=128, verbose=1, shuffle=True)

        score = self.model.evaluate(x={'input1': self.x_test[:,0,:,:],'input2': self.x_test[:,1,:,:],'input3': self.x_test[:,2,:,:]},
                                    y={'output_fault': self.y_test}, batch_size=128, verbose=1)
        print("score is:")
        print(score)
        y_pre_fault = self.model.predict([self.x_test[:,0,:,:],self.x_test[:,1,:,:],self.x_test[:,2,:,:]], batch_size=1)
        np.argmax(y_pre_fault)
        #np.argmax(y_pre_loadVal)
        result1 = np.argmax(y_pre_fault, -1) == np.argmax(self.y_test, -1)
        result1 = result1.astype('int')
        # resultLoad = np.argmax(y_pre_loadVal, -1) == np.argmax(self.y_test[:, len(self.npy_dir):len(self.npy_dir) + len(self.loadStr)], -1)
        # resultLoad = resultLoad.astype('int')
        #self.acc_fault = np.sum(result1) / (dataset_len / 10 * self.channel)
        self.acc_fault = np.sum(result1) / len(result1)
        #self.acc_loadVal = np.sum(resultLoad) / (dataset_len / 10 * len(self.loadStr))
        #self.acc_loadVal = np.sum(resultLoad) / len(resultLoad)
        print("acc:",self.acc_fault)
        self.model_eveluate()
        self.model.save(os.path.join(os.getcwd(), 'model','1_epoch_'+str(self.epoch)+'_acc_'+str(self.acc_fault)+'_'+str(self.acc_eval_fault)+'_time_'+now_time_all + ".h5"))
        self.plt_pic()

    def plt_pic(self):
        N = self.epoch
        plt.style.use("ggplot")
        plt.figure()
        print(self.H.history.keys())
        plt.semilogy(np.arange(0, N), self.H.history["loss"], label="loss")
        plt.semilogy(np.arange(0, N), self.H.history["loss"], label="fault_loss")
        #plt.semilogy(np.arange(0, N), self.H.history["output_loadVal_loss"], label="loadVal_loss")
        plt.semilogy(np.arange(0, N), self.H.history["accuracy"], label="fault_acc")
        #plt.semilogy(np.arange(0, N), self.H.history["output_loadVal_accuracy"], label="loadVal_acc")

        plt.title("Training Loss and Accuracy on Dataset")
        plt.xlabel("Epoch #")
        plt.ylabel("Loss/Accuracy")
        plt.legend(loc="lower left")
        plt.savefig(os.path.join(os.getcwd(),'pic', '1_epoch_'+str(self.epoch)+'_acc_'+str(self.acc_fault)+'_'+str(self.acc_eval_fault)+'_time_'+now_time_all+".png"))
        print('Finish')

    def load_model(self, name):
        self.model = keras.models.load_model(name)
        self.model_eveluate()

    def getEvalData(self,str):#ABC
        x_evalA = []
        m = [0, 0, 0, 0, 0]
        if str == '0':
            m = [1, 0, 0, 0, 0]
        elif str == '1':
            m = [0, 1, 0, 0, 0]
        elif str == '2':
            m = [0, 0, 1, 0, 0]
        elif str == '3':
            m = [0, 0, 0, 1, 0]
        elif str == '4':
            m = [0, 0, 0, 0, 1]
        npy_file = os.path.join(os.getcwd(), str, 'newgenerate')
        for root, dirs, files in os.walk(npy_file):
            for j in files:  # 每一个文件
                startStr = self.getExceptStart(j)
                if j.startswith('A') and startStr not in self.loadSet:
                    self.loadSet.add(startStr)
                    a = np.load(os.path.join(npy_file, 'A' + startStr))
                    b = np.load(os.path.join(npy_file, 'B' + startStr))
                    c = np.load(os.path.join(npy_file, 'C' + startStr))

                    for i in range(a.shape[0] * 1 // 10):
                        x_evalA.append(a[a.shape[0] * 8 // 10 + i])
                        x_evalA.append(b[b.shape[0] * 8 // 10 + i])
                        x_evalA.append(c[c.shape[0] * 8 // 10 + i])
                        self.x_eval.append(x_evalA)
                        x_evalA = []
                        self.y_eval.append(m)


    def model_eveluate(self):
        self.loadSet = set()
        self.y_train_flag = False
        print("Start Eval")
        for i in self.npy_dir:# 01234
            self.getEvalData(i)
        self.x_eval = np.array(self.x_eval)
        self.y_eval = np.array(self.y_eval)
        #print(self.x_eval.shape)
        self.x_eval = self.x_eval.reshape(self.x_eval.shape[0],self.x_eval.shape[1], self.data_len // 128, 128)
        score = self.model.evaluate(x={'input1': self.x_eval[:,0,:,:],'input2': self.x_eval[:,1,:,:],'input3': self.x_eval[:,2,:,:]},
                                    y={'output_fault': self.y_eval}, batch_size=128,
                                    verbose=1)
        print("eval score is:")
        print(score)
        y_pre_fault= self.model.predict([self.x_eval[:,0,:,:],self.x_eval[:,1,:,:],self.x_eval[:,2,:,:]], batch_size=1)
        np.argmax(y_pre_fault)
        result1 = np.argmax(y_pre_fault, -1) == np.argmax(self.y_eval, -1)
        result1 = result1.astype('int')
        # resultLoad = np.argmax(y_pre_loadVal, -1) == np.argmax(self.y_eval[:,len(self.npy_dir):len(self.npy_dir) + len(self.loadStr)], -1)
        # resultLoad = resultLoad.astype('int')
        print(dataset_len/10*self.channel,self.y_eval[:, 0:len(self.npy_dir)].shape,len(result1),np.sum(result1))
        print(result1)
        #self.acc_eval_fault = np.sum(result1) / (dataset_len / 10*self.channel)
        self.acc_eval_fault = np.sum(result1) / len(result1)
        #self.acc_eval_loadVal = np.sum(resultLoad) / len(resultLoad)
        print("val_acc:",self.acc_eval_fault)

    def predict_data(self,data_pre:List) -> str:
        #self.model = keras.models.load_model(name)
        y_test = self.model.predict([data_pre[:, 0, :, :], data_pre[:, 1, :, :], data_pre[:, 2, :, :]], batch_size=1)
        return np.argmax(y_test)



def myThread():
    start = time.clock()
    myLstm = MyLstm(data_len)
    #myLstm.train()
    #myLstm.load_model(os.path.join(os.getcwd(),'model','epoch_1_acc_0.88_time_2021_04_08_11_22.h5'))
    t1 = np.random.randint(-30, 50, size=(1, 3, 4, 128))  # 三个（1,4,128）输入即可
    myLstm.predict_data(os.path.join(os.getcwd(), 'model', 'epoch_100_acc_0.998_evalacc_0.996_time_2021_04_08_16_43.h5'),t1)
    end = time.clock()
    t = end - start
    print("Runtime is ：%s s" % t)  # 1164


def preData(data:List) -> str:
    myLstm = MyLstm(data_len)
    myLstm.model = keras.models.load_model(
        os.path.join(os.getcwd(), 'model', 'epoch_100_acc_0.998_evalacc_0.996_time_2021_04_08_16_43.h5'))
    start = time.clock()
    faultType = myLstm.predict_data(data)
    end = time.clock()
    t = end - start
    print("preData runtime is ：%s s" % t)  # 1164
    print(faultType)
    return faultType

if __name__ == "__main__":
    #myThread()
    t1 = np.random.randint(-30, 50, size=(1, 3, 4, 128))  # 三个（1,4,128）输入即可
    print(preData(t1))
