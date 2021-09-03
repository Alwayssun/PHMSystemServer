from django.db import models

# Create your models here.
class RunData(models.Model):  # 记录用户信息
    mod_date = models.DateTimeField(verbose_name = '最后修改日期', auto_now=True)
    data = models.CharField(max_length=30, verbose_name="数据",default="")
    x_current = models.CharField(max_length=30,verbose_name="X相电流",default="0")
    y_current = models.CharField(max_length=30, verbose_name="Y相电流",default="0")
    z_current = models.CharField(max_length=30, verbose_name="Z相电流",default="0")
    status = models.CharField(max_length=5,verbose_name="故障状态",default="0")


    def __str__(self):
        return str(self.mod_date) + self.data + self.status

    class Meta:
        verbose_name = verbose_name_plural = "数据"


