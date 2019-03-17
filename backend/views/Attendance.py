from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.views import View
from datetime import datetime
from backend import models


class CreateAttendanceView(View):
    from backend.helpers import QrCode
    import time

    @method_decorator(login_required(login_url='/login'))
    def get(self, request, id):
        try:
            classRef = models.Classes.objects.get(pk=id)
            if not classRef.qrCodeOpen:
                qrCode = self._makeQrCode(classRef)
                context = {'img': qrCode, 'id_class': classRef.id}
            else:
                qrCode = models.QrCodes.objects.get(pk=classRef.qrCodeOpen)
                context = {'img': qrCode,
                           'id_class': classRef.id}
        except ObjectDoesNotExist:
            context = {'error': 'aconteceu um erro'}
        return render(request, 'backend/attendance.html', context)

    def _makeQrCode(self, classRef):
        name = str(classRef.id) + "_" + str(self.time.time())
        datas = {
                 'qrCode': name + ".png",
                 'attendance_date': self.time.strftime("%Y-%m-%d"),
                 'open': datetime.now(),
                 'classRef': classRef,
        }
        qrCode = models.QrCodes.objects.create(**datas)
        qrCode.makeQrCode()
        return qrCode


class CloseAttendanceView(View):
    @method_decorator(login_required(login_url='/login'))
    def get(self, request, id):
        classRef = models.Classes.objects.get(pk=id)
        if classRef.qrCodeOpen:
            qrCode = models.QrCodes.objects.get(pk=classRef.qrCodeOpen)
            qrCode.close = datetime.now()
            qrCode.save()
            classRef.qrCodeOpen = 0
            classRef.save()
        return HttpResponseRedirect(reverse('index'))
