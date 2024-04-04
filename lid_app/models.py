from django.db import models


STATUS = [
    ('no_started', 'Not Started'),
    ('continues', 'Continues'),
    ('completed', 'Completed'),
    ('deleted', 'Deleted'),
]


class Lid(models.Model):
    fullname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    parents = models.TextField()
    coming = models.CharField(max_length=255, null=True, blank=True)
    school = models.CharField(max_length=500, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    course = models.ForeignKey('course.Course', related_name='lids', on_delete=models.CASCADE)
    group = models.ForeignKey('group.Group', related_name='lids', on_delete=models.SET_NULL, null=True, blank=True)
    balance = models.DecimalField(max_digits=11, decimal_places=2, default=0)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS, default='no_started')

    objects = models.Manager()

    class Meta:
        ordering = ['fullname', '-update_time']

    def __str__(self):
        return f"{self.fullname} - {self.status}"


class Contact(models.Model):
    fullname = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    location = models.CharField(max_length=50)
    was_answered = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.fullname} - {self.phone_number}"

    class Meta:
        ordering = ['-created_time']
