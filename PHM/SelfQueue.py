# -*- coding: utf-8 -*-

"""
Author  :   AlwaysSun
Time    :   2021/9/2 19:32
"""

'''
    用列表实现一个可以不断增加的队列，可以完成添加和取数据等操作
    以长度为3的列表为例
    最开始[0,0,0]    leftIndex(0)  rightIndex(0)
    put(1):[1,0,0]   0          1
    put(2):[2,1,0]   0          2
    put(3):[3,2,1]   0          3
    get():[0,3,2]->1
    get():[0,0,3]->2
    get():[0,0,0]->3
    
    put(4):[]
'''
class SelfQueue:
    def __init__(self,qSize):
        self.qSize = qSize
        self.data = [0 for i in range(qSize)]
        self.length = 0
        self.rightIndex = 0 # 右边的索引
        self.leftIndex = 0 # 左边的索引

    def put(self,x):
        for i in range(self.qSize - 1 ,0,-1):
            self.data[i] = self.data[i-1]
        self.data[self.leftIndex] = x
        #self.leftIndex+=1
        if self.rightIndex < self.qSize - 1:
            self.rightIndex += 1
        if self.length < self.qSize:
            self.length += 1

    def toList(self):
        return self.data

    def full(self):
        if self.length < self.qSize:
            return False
        else:
            return True
    
    # def get(self):
    #     if self.rightIndex < self.qSize:
    #         for i in range(self.qSize-1 ,0,-1):
    #             self.data[i] = self.data[i - 1]
    #         self.data[0] = 0
    #         self.leftIndex += 1
    #         return self.data[self.rightIndex]
    #     self.length -=1



if __name__ == '__main__':
    que = SelfQueue(3)
    que.put(1)
    print(que.length, que.full())
    que.put(2)
    print(que.length, que.full())
    que.put(3)
    print(que.length, que.full())
    que.put(2)
    print(que.data)
    print(que.length,que.full())

