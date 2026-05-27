from django.db import models
from django.conf import settings

# Create your models here.
class Welcome(models.Model):
    # upload_to 图片上传后，放到 media文件夹下的welcome文件夹下
    # 必须安装pillow      pip3 install pillow
    # 如果用CharField--》图片需要自己保存，然后把地址放在CharField这个字段上
    img = models.ImageField(upload_to='welcome', default='/welcome/slash.png')
    order = models.IntegerField()
    # 这个字段以后不用传，会自动把上传图片的时间存到数据库
    create_time = models.DateTimeField(auto_now=True)
    is_delete = models.BooleanField(default=False)

    class Meta:
        # 在admin中，表名是中文
        verbose_name_plural = '欢迎表'

class Banner(models.Model):
    img = models.ImageField(upload_to='banner', default='banner1.png', verbose_name='图片')
    order = models.IntegerField(verbose_name='顺序')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    is_delete = models.BooleanField(default=False, verbose_name='是否删除')

    class Meta:
        verbose_name_plural = '轮播图'

    def __str__(self):
        return str(self.img)

class Notice(models.Model):
    title = models.CharField(max_length=64, verbose_name='公告标题')
    content = models.TextField(verbose_name='公告内容')
    img = models.ImageField(upload_to='notice', default='notice.png', verbose_name='公告图片')
    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')

    class Meta:
        verbose_name_plural = '公告表'

    def __str__(self):
        return self.title

class Collection(models.Model):
    name = models.CharField(max_length=32, verbose_name='采集人员姓名')
    # 做为人脸识别的id号
    name_pinyin=models.CharField(max_length=32, verbose_name='姓名拼音',null=True)
    avatar = models.ImageField(upload_to='collection/%Y/%m/%d/', default='default.png', verbose_name='头像')
    create_time = models.DateTimeField(auto_now=True, verbose_name='采集时间')
    # face_token---->人脸识别的token唯一码
    face_token = models.CharField(max_length=64, verbose_name='百度Token', null=True)
    area = models.ForeignKey(to='Area', null=True, verbose_name='网格区域', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '采集表'

    def __str__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=32, verbose_name='网格区域名')
    desc = models.CharField(max_length=32, verbose_name='网格简称')
    # 跟用户一对多---》一个网格员，可以采集多个网格
    user = models.ForeignKey(to='UserInfo', on_delete=models.CASCADE, null=True, verbose_name="负责用户")

    class Meta:
        verbose_name_plural = '区域表'
    def __str__(self):
        return self.name

class UserInfo(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=32)
    avatar = models.FileField(verbose_name="头像", max_length=128, upload_to='avatar')
    create_date = models.DateField(verbose_name="日期", auto_now_add=True)
    score = models.IntegerField(verbose_name="积分", default=0)
    # 用户需要手机号登录--》手机号字段
    mobile = models.CharField(verbose_name="手机号", max_length=11, null=True)

    class Meta:
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.name


### 活动表
class Activity(models.Model):
    title = models.CharField(verbose_name="活动标题", max_length=128)
    text = models.TextField(verbose_name="活动描述", null=True, blank=True)
    date = models.DateField(verbose_name="举办活动日期")
    count = models.IntegerField(verbose_name='报名人数', default=0)
    total_count = models.IntegerField(verbose_name='总人数', default=0)
    score = models.IntegerField(verbose_name="积分", default=0)
    # 一个用户可以报名多个活动
    join_record = models.ManyToManyField(
        to='UserInfo',
        verbose_name="参与者",
        through="JoinRecord",
        through_fields=("activity", "user"),
    )

    class Meta:
        verbose_name_plural = '活动表'

    def __str__(self):
        return self.title


## 活动报名记录表--》跟用户多对多关系--》一个用户可以报名多个活动
class JoinRecord(models.Model):
    # 原来可能是 ForeignKey(settings.AUTH_USER_MODEL, ...)
    user = models.ForeignKey('UserInfo', on_delete=models.CASCADE)   # 改为直接关联 UserInfo
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'activity')