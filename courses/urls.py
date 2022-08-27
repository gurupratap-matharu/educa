from django.urls import path

from . import views

app_name = "courses"

urlpatterns = [
    # instructor facing CRUD views
    path("mine/", views.ManageCourseListView.as_view(), name="manage_course_list"),
    path("create/", views.CourseCreateView.as_view(), name="course_create"),
    path("<int:pk>/update/", views.CourseUpdateView.as_view(), name="course_update"),
    path("<int:pk>/delete/", views.CourseDeleteView.as_view(), name="course_delete"),
    # public facing views
    path("<int:pk>/", views.CourseDetailView.as_view(), name="course_detail"),
    path("", views.CourseListView.as_view(), name="course_list"),
]
