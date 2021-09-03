from django.shortcuts import render, redirect
from django.http import HttpResponse, FileResponse,JsonResponse
from .models import *
import random
from PHMSystem.sendMail import sendVerifCode
from PHMSystem.HttpResonseMy import *
from PHMSystem.HttpCode import *
import time,os

emailVerifyDict = {}

def checkLogin(name, token):
    """
    检查是否已经登录
    :param name: 邮箱地址
    :param token: token值
    :return: 0表示已经登录 且存在，否则返回错误代码
    """
    try:  # 检测是否有该用户
        user = User.objects.filter(name=name)[0]
    except:
        return USER_NO_SIGNUP,1
    try:  # 检查是否登录
        user = User.objects.filter(name=name, token=token)[0]
    except:
        return TOKEN_ERROR,1
    return 0,user

#获取token
def getToken():
    randomNum = random.randint(100000000,1000000000)
    return str(randomNum)

#邮件验证码
# password为0是注册，1是修改密码
def emailVerify(request):
    if request.method == 'GET':
        print("emailVerify get 请求")
        email = request.GET['email']
        flag = request.GET['password']
        print(email)
    elif request.method == "POST":
        print("emailVerify post 请求",request.POST)
        email = request.POST['email']
        flag = request.POST['password']
        print(email,flag)
    else:
        return errorResponse(REQUEST_TYPE_ERROR)
    if User.objects.filter(name = email) and flag != '1':# 注册时候
        return errorResponse(EMAIL_EXIST)
    try:
        verifyCode = sendVerifCode(email)
        if flag == '0':# 注册的时候需要将验证码写入到临时的字典里
            emailVerifyDict[email] = {}
            emailVerifyDict[email]['code'] = verifyCode
            emailVerifyDict[email]['status'] = '0'
            print(emailVerifyDict)
        else:# 修改密码直接写入到数据库
            user = User.objects.filter(name = email)[0]
            user.emailVerify = verifyCode
            user.save()
    except:
        return errorResponse(EMAIL_OR_SERVER_ERROR)
    return normalResponse( 'status', "OK")


# 邮件验证码 验证
# password为0是注册，1是修改密码
def emailVerifyVerify(request):
    if request.method == 'GET':
        print("emailVerifyVerify get 请求")
        email = request.GET['email']
        flag = request.GET['password']
        verifyCode = request.GET['verifyCode']
    elif request.method == "POST":
        print("emailVerifyVerify post 请求")
        email = request.POST['email']
        flag = request.POST['password']
        verifyCode = request.POST['verifyCode']
    else:
        return errorResponse(REQUEST_TYPE_ERROR)
    if flag == '0':
        if verifyCode == emailVerifyDict[email]['code']:
            emailVerifyDict[email]['status'] = '1'
            return normalResponse("status","OK")
        else:
            return errorResponse(EMAIL_VERFIFY_CODE_FAILED)# 邮件验证码错误
    else:
        user = User.objects.filter(name=email)[0]
        if verifyCode == user.emailVerify:
            return normalResponse("status", "OK")
        else:
            return errorResponse(EMAIL_VERFIFY_CODE_FAILED)  # 邮件验证码错误


def signUp(request):
#用户注册处理函数,注册成功后向用户发送注册成功的消息
#检查用户所发送的表格,将用户名,密码明文存入相应表格
#若用户名已存在,则返回用户以存在的消息
    if request.method == 'POST':
        try:
            data = eval(request.body.decode('utf-8'))
            nickname = data['nickname']
            name = data['email']
            password = data['password']
            phone = data['phone']
            gender = data['gender']
            info = data['info']
        except:
            return errorResponse(FORM_ERROR)
        if User.objects.filter(name = name):
            return errorResponse(EMAIL_EXIST)
        #if User.objects.filter(phone = phone):
            #return errorResponse(PHONE_EXIST)
        else:
            if emailVerifyDict[name]['status'] == '1':
                User.objects.create(nickname = nickname,name = name,pass_word = password,phone = phone,gender = gender,info = info)
            print(emailVerifyDict)
            emailVerifyDict.pop(name)
            print(emailVerifyDict)
            return normalResponse( 'status', "OK")
    else:
        return errorResponse(REQUEST_TYPE_ERROR)
#退出登录
def logout(request):
    if request.method == 'GET':
        print("Logout get 请求")
        #return HttpResponse(a[0].name)
        return errorResponse(REQUEST_TYPE_ERROR,"请求类型错误")
    elif request.method == 'POST':
        print("POST")
        try:
            data = eval(request.body.decode('utf-8'))
            name = data['username']
            token = data['token']
        except:
            return  errorResponse(FORM_ERROR)
        try:
            user = User.objects.filter(name = name)[0]
        except:
            return errorResponse(USER_NO_SIGNUP)# 用户未注册
        try:
            user = User.objects.filter(name = name,token = token)[0]
        except:
            return errorResponse(TOKEN_ERROR)
        print(user.name,user.isLogin)
        if user.isLogin:#用户已经登陆了
            try:
                user.isLogin = False
                user.token = "phm"
                user.cookie = "phm"
                print("User 存在")
                user.save()
            except:
                return errorResponse(SAVE_ERROR)
            # return HttpResponse("OK")
            return normalResponse( 'status', "logout")
        else:
            return errorResponse(USER_NO_LOGIN)
    return errorResponse(REQUEST_TYPE_ERROR)


def login(request):
    """
    用户登录
    :param request: 
    :return: 
    """
    if request.method == 'GET':
        return errorResponse(REQUEST_TYPE_ERROR)
    elif request.method == 'POST':
        try:
            data = eval(request.body.decode('utf-8'))
            user = data['username']
            password = data['password']
            print(user,password)
        except:
            return errorResponse(FORM_ERROR)
        try:
            user = User.objects.filter(name=user)[0]
        except:
            return errorResponse(USER_NO_SIGNUP)
        try:
            user = User.objects.filter(name=user, pass_word=password)[0]
        except:
            return errorResponse(PASSWORD_ERROR)
        if not user.isLogin:  # 用户未登录
            print("用户还未登录，现登录成功")
        else:
            print("用户已经登录，再次重复登录")
        try:
            #设置登录状态
            user.isLogin = True
            userToken = getToken()
            user.token = userToken
            user.cookie = userToken
            nickname = user.nickname
            user.save()
        except:
            return errorResponse(SAVE_ERROR)
        return loginResponse('token',userToken,nickname)
    return errorResponse(REQUEST_TYPE_ERROR)

def getInfo(request):
    """
    获取目前的个人信息 
    个人简介、性别、手机号、qq、微信
    :param request: 
    :return: 
    """
    if request.method == 'GET':
        print("获取个人信息请求")
        try:
            token = request.GET['token']
            email = request.GET['username']
        except:
            return errorResponse(FORM_ERROR)
        print(email,token)
        loginStatus, user = checkLogin(email, token)  # 检查是否已经登录
        if loginStatus == 0:
            print("用户已经登录")
        else:
            return errorResponse(loginStatus)
        if user.isLogin:  # 用户已经登录 可以修改
            email = user.name
            nickname = user.nickname
            info = user.info
            gender = user.gender
            phone = user.phone
            qq = user.qq
            wechat = user.wechat
            return userInfoResponse(email, nickname, info, gender, phone, qq, wechat)
        else:
            return errorResponse(USER_NO_LOGIN)
    elif request.method == 'POST':
        data = eval(request.body.decode('utf-8'))
        email = data['email']
        print(email)
        if User.objects.filter(name=email):
            return errorResponse(EMAIL_EXIST)
        try:
            verifyCode = sendVerifCode(email)
        except:
            return errorResponse(EMAIL_OR_SERVER_ERROR)
        return normalResponse('emailCode', verifyCode)


def changeInfo(request):
    """
    修改个人信息  主要是之前注册没有填的信息
    个人简介、性别、手机号、qq、微信
    :param request: 
    :return: 
    """
    if request.method == 'POST':
        try:# 获取表单
            data = eval(request.body.decode('utf-8'))
            name = data['username']
            token = data['token']
            nickname = data['nickname']
            info = data['info']
            gender = data['gender']
            phone = data['phone']
            qq = data['qq']
            wechat = data['wechat']
        except:# 表单内容不对
            return errorResponse(FORM_ERROR)

        loginStatus,user = checkLogin(name, token)  # 检查是否已经登录
        if loginStatus == 0:
            print("用户已经登录")
        else:
            return errorResponse(loginStatus)
        if user.isLogin:#用户已经登录 可以修改
            try:
                user.nickname = nickname
                user.info = info
                user.gender = gender
                user.phone = phone
                user.qq = qq
                user.wechat = wechat
                user.save()
            except:#更新数据失败
                return errorResponse(SAVE_ERROR)
        else:
            return errorResponse(USER_NO_LOGIN)
        return normalResponse("status", "OK")
    else:
        return errorResponse(REQUEST_TYPE_ERROR)

def changePassage(request):
    """
    修改密码
    :param request: 
    :return: 
    """
    if request.method == 'POST':
        try:# 获取表单
            data = eval(request.body.decode('utf-8'))
            name = data['username']
            token = data['token']
            newPassword = data['newPassword']
        except:
            return errorResponse(FORM_ERROR)
        loginStatus, user = checkLogin(name, token)  # 检查是否已经登录
        if loginStatus == 0:
            print("用户已经登录")
        else:
            return errorResponse(loginStatus)
        try:#修改密码
            user.pass_word = newPassword
            user.save()
        except:
            return errorResponse(SAVE_ERROR)
        return normalResponse("status","OK")
    else:
        return errorResponse(REQUEST_TYPE_ERROR)


# 上传头像
def uploadIcon(request):
    if request.method == 'POST':
        try:  # 获取表单
            print()
            name = request.POST.get("username")
            token = request.POST.get("token")
        except:
            return errorResponse(FORM_ERROR)
        loginStatus, user = checkLogin(name, token)  # 检查是否已经登录
        if loginStatus == 0:
            print("用户已经登录")
        else:
            return errorResponse(loginStatus)
        try:
            file = request.FILES.get('upload_icon_file')
            print(file,file.name)
            t = str(time.time())
            path = 'static\\head\\' + t + '.' + file.name.split('.')[-1]
            f = open(path, 'wb')
            f.write(file.read())
            f.close()
        except:
            return errorResponse(ICON_UPLOAD_FAILED)
        finally:
            user.headIcon = path  # 更新头像信息
            user.save()
        return normalResponse("status","OK")
    else:
        return errorResponse(FORM_ERROR)

# 获取头像
def getIcon(request):
    if request.method == 'GET':
        print("获取个人信息请求")
        try:
            token = request.GET['token']
            email = request.GET['username']
        except:
            return errorResponse(FORM_ERROR)
        print(email,token)
        loginStatus, user = checkLogin(email, token)  # 检查是否已经登录
        if loginStatus == 0:
            print("用户已经登录")
        else:
            return errorResponse(loginStatus)
        print(os.getcwd(),user.headIcon)
        with open(os.path.join(os.getcwd(),user.headIcon), 'rb') as f:
            ret_img_data = f.read()
         # content_type为img图片类型
        return HttpResponse(ret_img_data, content_type='image/jpg')
