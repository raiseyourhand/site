from backend.models import Students, QrCodes
from rest_framework import serializers


class StudentSerealizer(serializers.ModelSerializer):

    class Meta:
        model = Students
        fields = ('id', 'name', 'qrCodes')


class QrCodesSerializer(serializers.ModelSerializer):
    students_qrCode = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
     )

    class Meta:
        model = QrCodes
        fields = ('students_qrCode', )
