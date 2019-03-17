from django.contrib.auth.models import User
from django.test import Client, TestCase
from unittest import skip
from backend.models import Classes, Students, QrCodes


class TestAuthView(TestCase):
    def test_index(self):
        c = Client()
        response = c.get('/')
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        c = Client(username='user', password='senha')
        response = c.get('/login')
        self.assertEqual(response.status_code, 200)


class TestClassesView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='senha')

    def test_show_classes_without_classes(self):
        c = Client()
        c.login(username='user', password='senha')

        response = c.get('/classes')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['classes'].count(), 0)

    def test_classes_whith_classes(self):
        Classes.objects.create(name='class1',
                               teacher=self.user)
        Classes.objects.create(name='class2',
                               teacher=self.user)
        c = Client()
        c.login(username='user', password='senha')
        response = c.get('/classes')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['classes'].count(), 2)

    def test_classes_no_user(self):
        """
        it should send the user to the login page.
        """
        c = Client()
        response = c.get('/classes')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/login?next=/classes")

    def test_create_class_post_new_students(self):
        """
        it create a new class with students that don't exist on the database.
        """
        arq = '/home/alisson/Documents/raiseyourhand/Turma.csv'
        fp = open(arq, 'rb')
        c = Client()
        c.login(username='user', password='senha')
        response = c.post('/create/class', {'name': 'turma 1', 'file': fp})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Classes.objects.count(), 1)
        self.assertEqual(Students.objects.count(), 29)

    def test_create_class_post_without_new_students(self):
        """
        it create a new class with students that exist on the database.
        """
        arq = '/home/alisson/Documents/raiseyourhand/Turma.csv'
        fp = open(arq, 'rb')
        c = Client()
        c.login(username='user', password='senha')
        c.post('/create/class', {'name': 'turma 1', 'file': fp})
        fp.close()
        fp = open(arq, 'rb')
        c.post('/create/class', {'name': 'turma 2', 'file': fp})
        fp.close()
        self.assertEqual(Classes.objects.count(), 2)
        self.assertEqual(Students.objects.count(), 29)


class TestAttendanceView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='senha')

    def test_create_attendance(self):
        Classes.objects.create(name='Intro', teacher=self.user)
        c = Client()
        c.login(username='user', password='senha')
        response = c.get('/attendance/1')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['img'])

    def test_create_attendance_no_user(self):
        Classes.objects.create(name='Intro', teacher=self.user)
        c = Client()
        response = c.get('/attendance/1')
        self.assertEqual(response.status_code, 302)

    def test_open_attendance(self):
        classRef = Classes.objects.create(name='Intro', teacher=self.user)
        c = Client()
        c.login(username='user', password='senha')
        response = c.get('/attendance/1')
        self.assertEqual(response.status_code, 200)

        qr = QrCodes.objects.get(pk=1)
        self.assertIsNotNone(qr.qrCode)

        classRef = Classes.objects.get(pk=1)
        self.assertEqual(classRef.qrCodeOpen, 1)

    def test_close_attendance(self):
        def open_attendance():
            c.get('/attendance/1')

        classRef = Classes.objects.create(name='Intro', teacher=self.user)
        c = Client()
        c.login(username='user', password='senha')
        open_attendance()
        response = c.get('/attendance/close/1')
        self.assertEqual(response.status_code, 302)
        classRef = Classes.objects.get(pk=1)
        self.assertEqual(classRef.qrCodeOpen, 0)
