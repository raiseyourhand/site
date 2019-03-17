from django.test import TestCase
from datetime import date
from backend.models import QrCodes, Classes, Students


class TestStudentsModels(TestCase):
    def setUp(self):
        dataStructure = Classes.objects.create(name='Estrutura de Dados')

        students = [{'name': 'Gabriel', 'ra': '201810173'},
                    {'name': 'Ana', 'ra': '201820164'},
                    {'name': 'Eduarda', 'ra': '201817515'}
                    ]
        for student in students:
            s = Students.objects.create(**student)
            s.class_student.add(dataStructure)

    def test_students_class(self):
        dataStructure = Classes.objects.get(name='Estrutura de Dados')
        numStudents = dataStructure.students
        self.assertEqual(numStudents.count(), 3)


class TestQrCodesModel(TestCase):
    def setUp(self):
        dataStructure = Classes.objects.create(name='Estrutura de Dados')
        dataBase = Classes.objects.create(name='Banco de Dados')

        students = [
            {'name': 'Gabriel', 'ra': '201810173', 'classes': [dataStructure,
                                                               dataBase]},
            {'name': 'Ana', 'ra': '201820164', 'classes': [dataStructure]},
            {'name': 'Eduarda', 'ra': '201817515', 'classes': [dataBase]}
        ]
        for student in students:
            s = Students.objects.create(name=student['name'], ra=student['ra'])
            for c in student['classes']:
                s.class_student.add(c)

        qrCodes = [
            {'qrCode': 'chave1',
             'attendance_date': '2018-01-01',
             'open': '2019-02-09 09:11:42.730855',
             'classRef': dataStructure},
            {'qrCode': 'chave2', 'attendance_date': '2018-05-01',
             'open': '2019-02-09 09:11:42.730855',
             'classRef': dataStructure},
            {'qrCode': 'chave3',
             'attendance_date': '2018-06-06',
             'open': '2019-02-09 09:11:42.730855',
             'classRef': dataBase},
            {'qrCode': 'chave4',
             'attendance_date': '2018-06-06',
             'open': '2019-02-09 09:11:42.730855',
             'classRef': dataBase},
        ]
        for qr in qrCodes:
            QrCodes.objects.create(**qr)

        qr_students = [(1, 1), (1, 2), (1, 4), (2, 1), (3, 3), (3, 4)]
        for student_id, qrCode_id in qr_students:
            student = Students.objects.get(pk=student_id)
            qr = QrCodes.objects.get(pk=qrCode_id)
            student.qrCodes.add(qr)

    def test_presence_list_more_then_one_qr_code(self):
        """
        test for the getter of the presence list
        """
        result = {date(2018, 1, 1): [Students.objects.get(name='Gabriel'),
                                     Students.objects.get(name='Ana')],
                  date(2018, 5, 1): [Students.objects.get(name='Gabriel')]
                  }
        classRef = Classes.objects.get(name='Estrutura de Dados')
        self.assertEqual(classRef.presences, result)

    def test_presence_list_one_qr_code(self):
        """
        test for the getter of the presence list
        """
        result = {date(2018, 6, 6): [Students.objects.get(name='Eduarda'),
                                     Students.objects.get(name='Gabriel'),
                                     Students.objects.get(name='Eduarda'),
                                     ],
                  }
        classRef = Classes.objects.get(name='Banco de Dados')
        self.assertEqual(classRef.presences, result)
