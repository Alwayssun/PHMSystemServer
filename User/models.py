from django.db import models

# Create your models here.
class User(models.Model):  # 记录用户信息
    SEX_ITEMS = [
        (0, '男'),
        (1, '女')
    ]
    name = models.CharField(max_length=30, verbose_name="邮箱")
    nickname = models.CharField(max_length=30,null=True, verbose_name="昵称")
    #icon = models.CharField(max_length=200, verbose_name="头像")
    pass_word = models.CharField(max_length=20, verbose_name="密码")
    isLogin = models.BooleanField(default=False,verbose_name="is_login")
    cookie = models.CharField(max_length=30, default='phm',verbose_name="cookie")
    token = models.CharField(max_length=30, default='phm', verbose_name="token")
    headIcon = models.CharField(max_length=200,default="static//head//1627106680.92.jpg", verbose_name="头像")
    info = models.CharField(max_length=500,null=True, verbose_name="个人简介")
    gender = models.IntegerField(choices=SEX_ITEMS, null=True, verbose_name="性别")
    phone = models.CharField(max_length=20, null=True, verbose_name="手机号")
    qq = models.CharField(max_length=20, null=True, verbose_name="qq")
    wechat = models.CharField(max_length=20, null=True, verbose_name="wechat")
    emailVerify = models.CharField(max_length=6, null=True, verbose_name="目前的验证码")


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "用户"


