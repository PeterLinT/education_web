from django.db import models
from apps.users.models import BaseModel

class City(BaseModel):
    name = models.CharField(max_length=20, verbose_name='城市')
    desc = models.CharField(max_length=200, verbose_name='描述')


    class Mate:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CourseOrg(BaseModel):
    name = models.CharField(max_length=50, verbose_name='机构名称')
    desc = models.TextField(verbose_name='描述')
    tag = models.CharField(default='全国知名', max_length=10, verbose_name='机构标签')
    category = models.CharField(default='jxpg', max_length=4, verbose_name='机构类别'
                                , choices=(('pxjg', '培训机构'), ('gr', '个人'), ('gx', '高校')))
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(upload_to='org/%Y/%m', verbose_name='logo', max_length=100)
    address = models.CharField(max_length=150, verbose_name='机构地址')
    students = models.IntegerField(default=0, verbose_name='学习人数')
    course_nums = models.IntegerField(default=0, verbose_name='课程数')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='所在城市')

    is_auth = models.BooleanField(default=False, verbose_name='是否认证')
    is_gold = models.BooleanField(default=False, verbose_name='是否金牌')

    def courses(self):
        courses = self.course_set.filter(is_classics=True)[:3  ]
        return courses

    class Meta:
        verbose_name = '课程机构'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Teacher(BaseModel):
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name='所属机构')
    name = models.CharField(max_length=50, verbose_name='教师名')
    work_years = models.IntegerField(default=0, verbose_name='工作年限')
    work_position = models.CharField(max_length=50, verbose_name='公司职位')
    work_company = models.CharField(max_length=50, verbose_name='就职公司')
    points = models.CharField(max_length=50, verbose_name='教学特点')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    age = models.IntegerField(default=18, verbose_name='年龄')
    image = models.ImageField(upload_to='teacher/%Y/%m', verbose_name='头像')

    class Meta:
        verbose_name = '教师'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
    def course_nums(self):
        return self.course_set.all().count()