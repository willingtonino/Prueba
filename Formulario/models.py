from django.db import models
from Inicio_sesion.models import CustomUser, Company


class Section(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Question(models.Model):
    description = models.CharField(max_length=255)
    section = models.ForeignKey(Section, related_name='questions', on_delete=models.CASCADE)

    def __str__(self):
        return self.description


class Form(models.Model):
    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    sections = models.ManyToManyField(Section, through='FormSection', related_name='forms')
    authorized_employees = models.ManyToManyField(CustomUser, related_name='authorized_forms')

    def __str__(self):
        return self.title


class FormSection(models.Model):
    form = models.ForeignKey(Form, related_name='form_sections', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, related_name='sections_form', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.form.title} - {self.section.name}"


class Response(models.Model):
    SCALE_CHOICES = [
        (1, 'No lo describe nada'),
        (2, 'No le describe bien'),
        (3, 'Lo describe de cierta manera'),
        (4, 'Lo describe bien'),
        (5, 'Lo describe muy bien'),
    ]

    employee = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='responses')
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name='responses')
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='responses')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='responses')
    answer = models.IntegerField(choices=SCALE_CHOICES)

    class Meta:
        unique_together = ('employee', 'form', 'section', 'question')

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.form.title} - {self.question.description}"
