from django.db import models


PAYMENT_CHOICES = [
    ('cash', 'Cash'),
    ('plastic', 'Plastic'),
    ('bank', 'Bank'),
]


class Payment(models.Model):
    student = models.ForeignKey('customer.Student', related_name='payments', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=11, decimal_places=2)
    month = models.CharField(max_length=20, default='1-oy')
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='cash')
    created_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return f"{self.student} - {self.amount}"

    def save(self, *args, **kwargs):
        if self.pk:
            old_payment = Payment.objects.get(pk=self.pk)
            self.student.balance -= old_payment.amount
        self.student.balance += self.amount
        self.student.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.student.balance -= self.amount
        self.student.save()
        super().delete(*args, **kwargs)
