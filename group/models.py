from django.db import models

from customer.models import STATUS


class Group(models.Model):
    STUDY_DAY_CHOICES = (
        ('toq', 'Dushanba, Chorshanba, Juma'),
        ('juft', 'Seshanba, Payshanba, Shanba')
    )
    title = models.CharField(max_length=50)
    course = models.ForeignKey('course.Course', related_name='groups', on_delete=models.CASCADE)
    mentor = models.ForeignKey('customer.Mentor', related_name='groups', on_delete=models.SET_NULL, null=True,
                               blank=True)
    image = models.ImageField(upload_to='group/images/', null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    started_time = models.DateTimeField(null=True, blank=True)
    finished_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='no_started')
    study_day = models.CharField(max_length=50, default='toq', choices=STUDY_DAY_CHOICES)

    objects = models.Manager()

    class Meta:
        ordering = ['title', 'course']

    def __str__(self):
        return f"{self.title} - {self.course}"
