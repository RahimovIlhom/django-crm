from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return self.title
