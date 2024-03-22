from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Payment
        fields = '__all__'


class PaymentListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_time = serializers.DateTimeField(read_only=True)
    update_time = serializers.DateTimeField(read_only=True)
    student_info = serializers.SerializerMethodField('get_student')

    class Meta:
        model = Payment
        fields = ['id', 'student', 'student_info', 'amount', 'month', 'payment_type', 'created_time', 'update_time', ]

    def get_student(self, obj) -> dict:
        from customer.serializers import StudentSerializer
        return StudentSerializer(obj.student).data
