from django.urls import path, re_path

from courses.views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddCommentsView, VideoPlayView


app_name = "course"
urlpatterns = [
    # 课程列表url
    path('list/', CourseListView.as_view(), name="list"),
    # 课程详情页
    re_path('detail/(?P<course_id>\d+)/', CourseDetailView.as_view(), name="course_detail"),
    # 课程章节信息页
    re_path('info/(?P<course_id>\d+)/', CourseInfoView.as_view(), name="course_info"),

    # 课程章节信息页
    re_path('comments/(?P<course_id>\d+)/', CommentsView.as_view(), name="course_comments"),

    # 添加课程评论,已经把参数放到post当中了
    path('add_comment/', AddCommentsView.as_view(), name="add_comment"),

    # 课程视频播放页
    re_path('video/(?P<video_id>\d+)/', VideoPlayView.as_view(), name="video_play"),
]
