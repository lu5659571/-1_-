from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("courses/", views.course_list, name="course_list"),
    path("courses/new/", views.course_create, name="course_create"),
    path("courses/<int:pk>/", views.course_detail, name="course_detail"),
    path("groups/", views.group_list, name="group_list"),
]