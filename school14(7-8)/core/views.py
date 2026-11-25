from django.views.decorators.cache import cache_page
from django.views.decorators.cache import cache_control
from django.shortcuts import render
from django.db.models import Avg
from courses.models import Course, Teacher, StudyGroup
from students.models import Student, Enrollment

@cache_page(60)
def home(request):
    return render(request, "home.html")

@cache_control(no_cache=True, no_store=True, must_revalidate=True)
def stats(request):
    context = {
        "course_count": Course.objects.count(),
        "teacher_count": Teacher.objects.count(),
        "student_count": Student.objects.count(),
        "group_count": StudyGroup.objects.count(),
        "enrollment_count": Enrollment.objects.count(),
        "average_price": Course.objects.aggregate(
            avg=Avg("price")
        )["avg"] or 0,
    }

    return render(request, "stats.html", context)