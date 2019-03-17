from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.shortcuts import render
from django.views import View
from . import models


class ClassesView(View):
    @method_decorator(login_required(login_url='/login'))
    def get(self, request):
        context = {'classes': request.user.classes.all()}
        return render(request, 'backend/classes.html', context)


@method_decorator(login_required(login_url='/login'), name='dispatch')
class CreateClassView(View):
    """ Ainda não possui as rotinas de testes"""
    import csv
    import io
    from backend.forms import CreateClassForm

    def get(self, request):
        form = self.CreateClassForm()
        return render(request, 'backend/create_class.html', {'form': form})

    def post(self, request):
        form = self.CreateClassForm(request.POST, request.FILES)
        if form.is_valid():
            className = form.cleaned_data['name']
            file = form.cleaned_data['file']
            self._createClass(className, request.user, file)
        return HttpResponseRedirect(reverse('index'))

    def _createClass(self, className, user, students_csv):
        c = models.Classes.objects.create(name=className, teacher=user)
        self._registerStudents(c, students_csv)

    def _registerStudents(self, c, csv_file):
        """
        relates the student with the class if he already exist. Otherwise
        create it first.
        """
        csv_file.seek(0)
        fileIo = self.io.StringIO(csv_file.read().decode('ISO-8859-1'))
        reader = self.csv.DictReader(fileIo)
        students_created = []
        for row in reader:
            for student in row.values():
                r = student.split(';')
                try:
                    s = models.Students.objects.get(ra=r[0])
                    students_created.append(s)
                except ObjectDoesNotExist:
                    student_data = {"name": r[1], 'ra': r[0]}
                    student = models.Students.objects.create(**student_data)
                    students_created.append(student)
        c.students.add(*students_created)
