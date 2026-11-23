from django.shortcuts import render, get_object_or_404
from .models import Course, StudyGroup


def course_list(request):
    courses = Course.objects.all()
    return render(
        request, "courses/list.html",
        {"courses": courses}
    )


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    groups = course.groups.select_related("teacher")
    return render(
        request, "courses/detail.html",
        {"course": course, "groups": groups}
    )


def group_list(request):
    level = request.GET.get("level", "")
    groups = StudyGroup.objects.select_related(
        "course", "teacher"
    )

    if level:
        groups = groups.filter(course__level=level)

    return render(
        request, "courses/groups.html",
        {"groups": groups}
    )