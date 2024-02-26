from django.db import models


class Attendance(models.Model):
    student = models.ForeignKey('customer.Student', related_name='attendances', on_delete=models.CASCADE)
    attended = models.BooleanField(default=True)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.student} - {self.date} - {self.date}"
