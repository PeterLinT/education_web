from datetime import datetime

from django.db import models

from apps.users.models import BaseModel
from apps.organizations.models import Teacher, CourseOrg

"""
实体1<关系>实体2
课程 章节 视频 课程资源
"""


class Course(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name='讲师')
    course_org = models.ForeignKey(CourseOrg, blank=True, null=True, on_delete=models.CASCADE, verbose_name='课程机构')
    name = models.CharField(max_length=50, verbose_name='课程名')
    desc = models.CharField(max_length=300, verbose_name='课程描述')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    degree = models.CharField(verbose_name='难度', choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')), max_length=2)
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    notice = models.CharField(max_length=300, verbose_name='课程公告',default='')
    category = models.CharField(default='后端开发', max_length=20, verbose_name='课程类别')
    tag = models.CharField(default='', max_length=10, verbose_name='课程标签')
    youneed_know = models.CharField(default='', max_length=300, verbose_name='课程须知')
    teacher_tell = models.CharField(default='', max_length=300, verbose_name='老师告诉你')
    detail = models.TextField(verbose_name='课程详情')
    is_banner = models.BooleanField(default=False, verbose_name='是否广告位')
    image = models.ImageField(upload_to='course/%Y/%m', verbose_name='封面图', max_length=100)
    is_classics = models.BooleanField(default=False,verbose_name='是否经典')
    class Meta:
        verbose_name = '课程信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def lesson_nums(self):
        return self.lesson_set.all().count()

class CourseTag(BaseModel):
        course = models.ForeignKey(Course,on_delete=models.CASCADE, verbose_name='课程')
        tag = models.CharField(max_length=100, verbose_name='标签')

        class Meta:
            verbose_name = '课程标签'
            verbose_name_plural = verbose_name
        def __str__(self):
            return self.tag



class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # on_delete表示对应的外键数据呗删除后，当前的数据怎么办。
    name = models.CharField(max_length=100, verbose_name='章节名')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')

    class Meta:
        verbose_name = '课程章节'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Video(BaseModel):
    lesson = models.ForeignKey(Lesson, verbose_name='章节', on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name='章节名')
    learn_times = models.IntegerField(default=0, verbose_name='学习时长(分钟数)')
    url = models.CharField(max_length=200, verbose_name='访问地址')

    class Meta:
        verbose_name = '视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResourse(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='课程')
    name = models.CharField(max_length=100, verbose_name='名称')
    file = models.FileField(upload_to='course/resourse/%Y/%m', verbose_name='下载地址', max_length=200)

    class Meta:
        verbose_name = '课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
