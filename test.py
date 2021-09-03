# -*- coding: utf-8 -*-

"""
Author  :   AlwaysSun
Time    :   2021/9/2 10:03
"""
# import sys
# sys.path.append("G:\data_sun\project\DD\hanjia\motorProgram")
#
# import testDiao
#
# testDiao.diaoMain()
import numpy as np
import random


# x = [random.randint(-30,50) for i in range(512)]
# y = [random.randint(-30,50) for i in range(512)]
# z = [random.randint(-30,50) for i in range(512)]
#
# def getTestData(x:List,y:List,z:List):
#     data = np.array([x, y, z])
#     data = data.reshape((1,3,4,128))
#     return data
#
#
# t1 = np.random.randint(-30, 50, size=(1, 3, 4, 128))  # 三个（1,4,128）输入即可
# print(t1.shape)

import queue

q=queue.Queue(5)    #如果不设置长度,默认为无限长
print(q.maxsize)    #注意没有括号
q.put(123)
q.put(456)
q.put(789)
q.put(100)
q.put(202)
print(q.full())
print(q.get())
print(q.get())

print(q.qsize())




