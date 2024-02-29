from django.db import models


class Mentor(models.Model):
    fullname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    photo = models.ImageField(upload_to='mentor/photos/', null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='mentors')

    objects = models.Manager()

    class Meta:
        ordering = ['fullname']

    def __str__(self):
        return f'{self.fullname} - {self.course}'


STATUS = [
    ('no_started', 'Not Started'),
    ('continues', 'Continues'),
    ('completed', 'Completed'),
    ('deleted', 'Deleted'),
]


class Student(models.Model):
    fullname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    parents = models.TextField()
    coming = models.CharField(max_length=255, null=True, blank=True)
    course = models.ForeignKey('course.Course', related_name='students', on_delete=models.CASCADE)
    group = models.ForeignKey('group.Group', related_name='students', on_delete=models.SET_NULL, null=True, blank=True)
    balance = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS, default='no_started')

    objects = models.Manager()

    class Meta:
        ordering = ['fullname', '-update_time']

    def __str__(self):
        return f"{self.fullname} - {self.status}"
