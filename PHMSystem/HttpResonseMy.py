from django.http import HttpResponse, FileResponse,JsonResponse

#返回错误的类
class HttpResponseError():
    def __init__(self, code, message):
        self.code = code
        self.errorMessage = message

#错误返回
def errorResponse(responseError:HttpResponseError):
    print("error:",responseError.errorMessage)
    return JsonResponse({
                'code': responseError.code,
                'status': responseError.errorMessage
            },json_dumps_params={'ensure_ascii':False})
#正常返回
def normalResponse(messageKey, message):
    print("noraml",message,":",message)
    return JsonResponse({
        'code': 200,
        messageKey: message
    },json_dumps_params={'ensure_ascii':False})

#登录返回
def loginResponse(messageKey, message, nickname):
    print("noraml",message,":",message)
    return JsonResponse({
        'code': 200,
        messageKey: message,
        "nickname" : nickname
    },json_dumps_params={'ensure_ascii':False})


#查询用户个人信息
def userInfoResponse(email, nickname, info, gender, phone, qq, wechat):

    return JsonResponse({
        'code': 200,
        "email": email,
        "nickname":nickname,
        "info":info,
        "gender":gender,
        "phone":phone,
        "qq":qq,
        "wechat":wechat,
    },json_dumps_params={'ensure_ascii':False})