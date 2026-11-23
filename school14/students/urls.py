from django.urls import path
from . import views

urlpatterns = [
    path(
        "students/create/",
        views.student_create,
        name="student_create",
    ),
]