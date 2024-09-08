from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission, User


class Task(models.Model):
    course = models.CharField(max_length=20)
    task_title = models.CharField(max_length=100)
    description = models.TextField(max_length=2000)

    def get_absolute_url(self):
        return reverse('assignments:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.course + ' - ' + self.task_title


class Hw(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='hw')
    hw_title = models.CharField(max_length=100)
    hw_content = models.TextField(max_length=10000)
    hw_object = models.FileField(null=True, blank=True)
    writer = models.ForeignKey(User)

    def __str__(self):
        return self.hw_title