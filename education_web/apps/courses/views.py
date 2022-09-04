from django.shortcuts import render
from django.views.generic import View
from apps.courses.models import Course, CourseTag, CourseResourse, Video
from pure_pagination import Paginator, PageNotAnInteger
from apps.operations.models import UserFavorite, UserCourse, CourseComments
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


class CourseListView(View):
    def get(self, request, *args, **kwargs):
        all_courses = Course.objects.order_by('-add_time')
        hot_courses = Course.objects.order_by("-click_nums")[:3]

        keywords = request.GET.get('keywords', '')
        if keywords:
            all_courses = all_courses.filter(
                Q(name__icontains=keywords) | Q(desc__icontains=keywords) | Q(detail__icontains=keywords))
        s_type = "course"
        # 课程排序
        sort = request.GET.get('sort', '')
        if sort == 'students':
            all_courses = all_courses.order_by('-students')
        elif sort == "hot":
            all_courses = all_courses.order_by('-click_nums')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'sort': sort,
            "keywords": keywords,
            "hot_courses": hot_courses,
            "s_type": s_type
        })


class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        # tag = Course.tag
        # related_courses = []
        # if tag:
        #     related_courses = Course.objects.filter(tag=tag)
        tags = course.coursetag_set.all()
        # 列表生成式
        tag_list = [tag.tag for tag in tags]
        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course_id=course.id)
        related_courses = set()
        for course_tag in course_tags:
            related_courses.add(course_tag.course)

        return render(request, 'course-detail.html', {
            'course': course,
            'has_fav_course': has_fav_course,
            'has_fav_org': has_fav_org,
            'related_courses': related_courses,
        })


class CourseLessonView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by('course__click_nums')
        related_courses = [user_course.course for user_course in all_courses if user_course.course.id != course.id]

        course_resources = CourseResourse.objects.filter(course=course)

        return render(request, 'course-video.html', {
            'course': course,
            'course_resources': course_resources,
            'related_courses': related_courses,

        })


class CourseCommentView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request, course_id, *args, **kwargs):
        """
               获取课程章节信息
               """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        comments = CourseComments.objects.filter(course=course)
        # 1. 查询用户是否关联该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()
        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
        # related_courses = [user_course.course  for user_course in all_courses if user_course.course.id!=course.id]
        related_courses = []
        for item in all_courses:
            if item.course_id != course.id:
                related_courses.append(item.course)
        course_resource = CourseResourse.objects.filter(course=course)

        # 3. 其他课程
        print(comments)
        return render(request, "course-comment.html", {
            "course": course,
            "course_resource": course_resource,
            "related_courses": related_courses,
            "comments": comments

        })


class VideoView(View):
    login_url = "/login/"

    def get(self, request, course_id, video_id, *args, **kwargs):
        """
        获取课程章节信息
        """
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()

        video = Video.objects.get(id=int(video_id))
        # 1. 查询用户是否关联该课程
        user_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()
            course.students += 1
            course.save()
        # 学习过该课程的所有同学
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourse.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:5]
        # related_courses = [user_course.course  for user_course in all_courses if user_course.course.id!=course.id]
        related_courses = []
        for item in all_courses:
            if item.course_id != course.id:
                related_courses.append(item.course)
        course_resource = CourseResourse.objects.filter(course=course)

        # 3. 其他课程

        return render(request, "course-play.html", {
            "course": course,
            "course_resource": course_resource,
            "related_courses": related_courses,
            "video": video,
        })
