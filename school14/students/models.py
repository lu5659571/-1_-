from django.db import models
from courses.models import StudyGroup


class Student(models.Model):
    full_name = models.CharField("ФИО", max_length=150)
    birth_date = models.DateField("Дата рождения")
    phone = models.CharField("Телефон", max_length=20)
    email = models.EmailField("Email")

    groups = models.ManyToManyField(
        StudyGroup,
        through="Enrollment",
        related_name="students",
        blank=True,
    )

    class Meta:
        verbose_name = "Ученик"
        verbose_name_plural = "Ученики"

    def __str__(self):
        return self.full_name


class Enrollment(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="Ученик",
    )
    group = models.ForeignKey(
        StudyGroup,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="Группа",
    )
    enrolled_at = models.DateTimeField(
        "Дата записи", auto_now_add=True
    )

    class Meta:
        verbose_name = "Запись"
        verbose_name_plural = "Записи"
        constraints = [
            models.UniqueConstraint(
                fields=["student", "group"],
                name="unique_student_group",
            )
        ]

    def __str__(self):
        return f"{self.student} — {self.group}"