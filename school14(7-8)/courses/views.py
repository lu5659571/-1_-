from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from .models import Course, StudyGroup
from .forms import CourseForm


def course_list(request):
    q = request.GET.get("q", "").strip()
    level = request.GET.get("level", "")

    courses = Course.objects.all().order_by("id")

    if q:
        courses = courses.filter(name__icontains=q)

    if level in dict(Course.LEVELS):
        courses = courses.filter(level=level)

    context = {
        "courses": courses,
        "q": q,
        "level": level,
        "levels": Course.LEVELS,
    }

    return render(request, "courses/list.html", context)


def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)

    groups = course.groups.select_related("teacher")

    return render(
        request,
        "courses/detail.html",
        {"course": course, "groups": groups}
    )


def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                course = form.save()

            return redirect(
                "courses:course_detail",
                pk=course.pk
            )

        return render(
            request,
            "courses/form.html",
            {"form": form},
            status=400
        )

    form = CourseForm()

    return render(
        request,
        "courses/form.html",
        {"form": form}
    )


def group_list(request):
    level = request.GET.get("level", "")

    groups = StudyGroup.objects.select_related(
        "course", "teacher"
    )

    if level in dict(Course.LEVELS):
        groups = groups.filter(course__level=level)

    return render(
        request,
        "courses/groups.html",
        {
            "groups": groups,
            "levels": Course.LEVELS,
            "level": level,
        }
    )