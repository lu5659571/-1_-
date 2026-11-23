
from django.db import models


class Teacher(models.Model):
    full_name = models.CharField("ФИО", max_length=150)
    subject = models.CharField("Предмет", max_length=100)
    phone = models.CharField("Телефон", max_length=20)

    class Meta:
        verbose_name = "Преподаватель"
        verbose_name_plural = "Преподаватели"

    def __str__(self):
        return self.full_name


class Course(models.Model):
    LEVELS = [
        ("beginner", "Начальный"),
        ("intermediate", "Средний"),
        ("advanced", "Продвинутый"),
    ]

    name = models.CharField("Название", max_length=150)
    level = models.CharField(
        "Уровень", max_length=20, choices=LEVELS
    )
    duration = models.PositiveIntegerField(
        "Длительность, часов"
    )
    price = models.DecimalField(
        "Цена", max_digits=10, decimal_places=2
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.name


class StudyGroup(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="groups",
        verbose_name="Курс",
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.PROTECT,
        related_name="groups",
        verbose_name="Преподаватель",
    )
    start_date = models.DateField("Дата начала")
    schedule = models.CharField(
        "Расписание", max_length=200
    )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return f"{self.course.name} — группа №{self.pk}"