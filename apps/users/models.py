from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    # 用user替换auth_user表，即拓展表
    nick_name = models.CharField(max_length=50,verbose_name=u"昵称",default="")
    birday = models.DateField(verbose_name=u"生日",null=True,blank=True)
    gender = models.CharField(max_length=6,choices=(("male",u"男"),("female",u"女")),default="female")
    address = models.CharField(max_length=100,default=u"")
    mobile = models.CharField(max_length=11,null=True,blank=True)
    image = models.ImageField(upload_to="image/%Y/%m",default=u"image/default.png")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    # 重载__unicode__，用于打印自定义的字符串
    def __str__(self):
        return self.username

    def unread_nums(self):
        # 获取用户未读消息的数量
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id,has_read=False).count()


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name=u"验证码")
    email = models.EmailField(max_length=50,verbose_name=u"邮箱")
    send_type = models.CharField(verbose_name=u"验证码类型",choices=(("register",u"注册"),("forget",u"找回密码"),("update_email",u"修改邮箱")),max_length=20)
    send_time = models.DateTimeField(verbose_name=u"发送时间",default=datetime.now)#datetime.now是class实例化的时间,datetime.now()是model编译的时间

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    # 重载__unicode__，用于打印自定义的字符串，比如新增验证码时，成功后会显示验证码+邮箱，如果不加则会显示	EmailVerifyRecord object
    def __str__(self):
        return '{0}({1})'.format(self.code,self.email)


class Banner(models.Model):
    title = models.CharField(max_length=100,verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y/%m",verbose_name=u"轮播图",max_length=100)
    url = models.URLField(max_length=200,verbose_name=u"访问地址")
    index = models.IntegerField(default=100,verbose_name=u"顺序")#比如想把某张图片放在前面，只需要把index设置小一点就可以了
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"轮播图"
        verbose_name_plural = verbose_name