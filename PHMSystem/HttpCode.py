
from .HttpResonseMy import HttpResponseError

OK_CODE = 200

REQUEST_TYPE_ERROR = HttpResponseError(800,"请求类型错误")

EMAIL_EXIST = HttpResponseError(801,"该邮箱已经注册，请直接登录")
PHONE_EXIST = HttpResponseError(802,"手机已经被注册")
EMAIL_OR_SERVER_ERROR = HttpResponseError(803,"邮箱地址错误或服务器错误")

TOKEN_ERROR = HttpResponseError(804,"token错误")
PASSWORD_ERROR = HttpResponseError(805,"账号或密码错误")

USER_NO_SIGNUP = HttpResponseError(806,"用户未注册")
USER_NO_LOGIN = HttpResponseError(807,"用户还没有登录")

FORM_ERROR = HttpResponseError(808,"表单错误")
SAVE_ERROR = HttpResponseError(809,"信息更新失败")

ICON_UPLOAD_FAILED = HttpResponseError(810,"头像上传失败")

EMAIL_VERFIFY_CODE_FAILED = HttpResponseError(811,"邮件验证码错误")

DATA_ERROR = HttpResponseError(812,"数据错误")
SOFTWARE_CLIENT_ERROE = HttpResponseError(813,"数据上传软件未开启")