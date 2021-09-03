from django.core import serializers
from PHMSystem.HttpResonseMy import *
import numpy as np
import random,os,sys,json
from PHMSystem.HttpCode import *

from .models import *
from .SelfQueue import SelfQueue

sys.path.append("G:\data_sun\project\DD\hanjia\motorProgram")
import gru_train_onlyfault

#dataa = '[{"paras":"几方战步专。","value":%d,"row_index":0,"index":0},{"paras":"问千专声社将联。","value":56,"row_index":1,"index":1},{"paras":"低集平任去加三率。","value":102,"row_index":2,"index":2},{"paras":"都速该越还。","value":56,"row_index":3,"index":3},{"paras":"持江被公连温验。","value":123,"row_index":4,"index":4},{"paras":"石给别农说始。","value":58,"row_index":5,"index":5},{"paras":"量节说时住话。","value":79,"row_index":6,"index":6},{"paras":"同表名力部。","value":59,"row_index":7,"index":7},{"paras":"片路济正专则了报。","value":115,"row_index":8,"index":8},{"paras":"特老后花作儿。","value":55,"row_index":9,"index":9}]'%random.randint(100,10000)
motor1 = "0"
motor2 = "0"
dataQueueX = SelfQueue(512)
dataQueueY = SelfQueue(512)
dataQueueZ = SelfQueue(512)
nowData = ""

def get_ip(request):
    '''
    获取请求者的IP信息
    :param request: 
    :return: 请求者的ip
    '''
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    return "请求IP地址为："+ ip

def getStatus(dataQueueX:SelfQueue,dataQueueY:SelfQueue,dataQueueZ:SelfQueue) -> str:
    """
    将队列转换成数组，同时进行故障诊断
    :param dataQueueX:X相的数据 
    :param dataQueueY: Y相的数据 
    :param dataQueueZ: Z相的数据 
    :return: 故障与否的代号
    """
    data = np.array([dataQueueX.data, dataQueueY.data, dataQueueZ.data])
    data = data.reshape((1, 3, 4, 128))
    faultType = gru_train_onlyfault.preData(data)
    print("get Status")
    return faultType


def upData(request):
    '''
    客户端软件上传数据并进行检测
    :param request: 
    :return: 返回状态码
    '''
    global nowData
    global dataQueueX,dataQueueY,dataQueueZ
    print(dataQueueX)
    print(get_ip(request))
    if request.method == 'POST':
        print("POST Data ---",request.body.decode("utf-8"))
        getNowData = eval(request.body.decode('utf-8'))
        status = '0'
        #print(dataa['data'])
        date = getNowData['time']
        x = getNowData['X']
        y = getNowData['Y']
        z = getNowData['Z']
        getNowData['status'] = '0'
        data = request.body.decode('utf-8')
        #print(date,x,y,z,data)
        dataQueueX.put(x)
        dataQueueY.put(y)
        dataQueueZ.put(z)
        print(dataQueueX.length,dataQueueY.length,dataQueueZ.length)
        if dataQueueX.full() and dataQueueY.full() and dataQueueZ.full():
            status = getStatus(dataQueueX, dataQueueY, dataQueueZ)
        nowData = eval(data)
        nowData['status'] = str(status)
        RunData.objects.create(mod_date = date,data =data,x_current = x,y_current = y,z_current = z,status = status)
    else:
        return errorResponse(REQUEST_TYPE_ERROR)
    return normalResponse('status',"ok")

def getDataByTime(request):
    '''
    通过时间段获取，当前满足条件的数据
    :param request: 
    :return: 
    '''
    if request.method == "POST":
        try:
            data = {}
            postData = eval(request.body.decode('utf-8'))
            startTime = postData['startTime']
            endTime = postData['endTime']
            getRunData = RunData.objects.filter(mod_date__gt=startTime, mod_date__lt=endTime)
            data['data'] = json.loads(serializers.serialize("json", getRunData))
            return JsonResponse(data)
        except:
            return errorResponse(REQUEST_TYPE_ERROR)
    else:
        try:
            data = {}
            startTime = request.GET['startTime']
            endTime = request.GET['endTime']
            getRunData = RunData.objects.filter(mod_date__gt = startTime,mod_date__lt =endTime)
            print(len(getRunData))
            print(type(getRunData))
            print(getRunData)
            data['data'] = json.loads(serializers.serialize("json", getRunData))
            return JsonResponse(data)
        except:
            return errorResponse(REQUEST_TYPE_ERROR)
    return errorResponse(REQUEST_TYPE_ERROR)

def getNowData(request):
    '''
    浏览器获取当前软件上传的数据 
    :param request: 
    :return: 当前透传的数据加上一个故障检查状态
    '''
    global nowData
    if request.method == "GET":
        print("nowData",nowData)
        if nowData !="":
            return normalResponse("data",nowData)
        else:
            return errorResponse(SOFTWARE_CLIENT_ERROE)

def getFile(request):
    with open(os.path.join(os.getcwd(), "static\\model\\emazongzhuang2.STL"), 'rb') as f:
        ret_img_data = f.read()
        # content_type为img图片类型
    return HttpResponse(ret_img_data, content_type='application/vnd.ms-pkistl')

def faultDiagnosis(request):
    '''
    可以完成单组数据的故障诊断，目前是写死的状态
    :param request: 
    :return: 
    '''
    if request.method == 'POST':
        print("------faultDiagnosis-----")
        print(request.POST)
        #try:
        requestData = eval(request.body.decode('utf-8'))
        x = [float(i) for i in requestData['X'].split(',')]
        y = [float(i) for i in requestData['Y'].split(',')]
        z = [float(i) for i in requestData['Z'].split(',')]
        data = np.array([x, y, z])
        data = data.reshape((1, 3, 4, 128))
        # t1 = np.random.randint(-30, 50, size=(1, 3, 4, 128))  # 三个（1,4,128）输入即可
        faultType = gru_train_onlyfault.preData(data)
        return HttpResponse(faultType)
        #except:
            #return errorResponse(DATA_ERROR)
    elif request.method == "GET":
        print("------faultDiagnosis-----")
        x = [random.randint(-30, 50) for i in range(512)]
        y = [random.randint(-30, 50) for i in range(512)]
        z = [random.randint(-30, 50) for i in range(512)]
        data = np.array([x, y, z])
        data = data.reshape((1, 3, 4, 128))
        # t1 = np.random.randint(-30, 50, size=(1, 3, 4, 128))  # 三个（1,4,128）输入即可
        faultType = gru_train_onlyfault.preData(data)
        return HttpResponse(faultType)
def test(request):
    RunData.objects.create(data = "12345",status = "2")
    return HttpResponse("OK")