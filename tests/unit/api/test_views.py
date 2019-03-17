from backend.models import Classes, QrCodes, Students
from django.contrib.auth.models import User
from django.db.models import Max
import json
from rest_framework.test import APITestCase


class TestStudents(APITestCase):
    def setUp(self):
        dataStructure = Classes.objects.create(name='Estrutura de Dados')
        dataBase = Classes.objects.create(name='Banco de Dados')

        student1 = Students.objects.create(name='Gabriel', ra='201810173')
        student1.class_student.add(dataStructure)
        student1.class_student.add(dataBase)
        student2 = Students.objects.create(name='Ana', ra='201820164')
        student2.class_student.add(dataStructure)
        student3 = Students.objects.create(name='Eduarda', ra='201817515')
        student3.class_student.add(dataBase)

        qrCode1 = QrCodes.objects.create(qrCode='chave1',
                                         attendance_date='2018-01-01',
                                         open='2019-02-09 09:11:42.730855')
        qrCode2 = QrCodes.objects.create(qrCode='chave2',
                                         attendance_date='2018-05-01',
                                         open='2019-02-09 09:11:42.730855')
        qrCode3 = QrCodes.objects.create(qrCode='chave3',
                                         attendance_date='2018-06-06',
                                         open='2019-02-09 09:11:42.730855')
        qrCode4 = QrCodes.objects.create(qrCode='chave4',
                                         attendance_date='2018-06-06',
                                         open='2019-02-09 09:11:42.730855')

        student1.qrCodes.add(qrCode1)
        student1.qrCodes.add(qrCode2)
        student1.qrCodes.add(qrCode4)
        student2.qrCodes.add(qrCode1)
        student3.qrCodes.add(qrCode3)
        student3.qrCodes.add(qrCode4)

        dataStructure.qrCodes.add(qrCode1)
        dataStructure.qrCodes.add(qrCode2)
        dataBase.qrCodes.add(qrCode3)
        dataBase.qrCodes.add(qrCode4)

        self.student = student1

    def test_simple(self):
        response = self.client.get('http://localhost:8000/api/students/')
        assert response.status_code == 200
        self.assertEqual(len(response.data), 3)

    def test_students(self):
        response = self.client.get('http://localhost:8000/api/students/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_students_get_id(self):
        response = self.client.get('http://localhost:8000/api/students/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        result = {'id': 1, 'name': 'Gabriel', 'qrCodes': [1, 2, 4]}
        self.assertEqual(json.loads(response.content), result)

    def test_students_get_id_fail(self):
        max_id = Students.objects.all().aggregate(Max("id"))["id__max"]
        url = f'http://localhost:8000/api/students/{max_id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_students_get_ra(self):
        url = f'http://localhost:8000/api/students/{self.student.ra}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        result = {'id': 1, 'name': 'Gabriel', 'qrCodes': [1, 2, 4]}
        self.assertEqual(json.loads(response.content), result)

    def test_students_get_ra_fail(self):
        ra = '000000000'
        url = f'http://localhost:8000/api/students/{ra}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_students_patch_id(self):
        student = Students.objects.create(name='student', ra='201810132')
        qr = QrCodes.objects.create(qrCode='chave5',
                                    attendance_date='2018-06-06',
                                    open='2019-02-09 09:11:42.730855')
        url = f'http://localhost:8000/api/students/{student.id}'
        data = {'qrCodes': [qr.id]}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 202)
        self.assertEqual(list(student.qrCodes.all()), [qr])

    def test_students_patch_ra(self):
        student = Students.objects.create(name='student', ra='201810132')
        qr = QrCodes.objects.create(qrCode='chave5',
                                    attendance_date='2018-06-06',
                                    open='2019-02-09 09:11:42.730855')
        url = f'http://localhost:8000/api/students/{student.ra}'
        data = {'qrCodes': [qr.id]}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, 202)
        self.assertEqual(list(student.qrCodes.all()), [qr])
