from django.core.exceptions import ObjectDoesNotExist
import json
from .models import Classes, QrCodes
import qrcode
import time
from datetime import datetime


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.jsonSerialize()


class QrCode:
    def __init__(self, classId):
        try:
            self.classRef = Classes.objects.get(pk=classId)
            self.name = str(self.classRef.id) + "_" + str(time.time())
            self.id = None
        except ObjectDoesNotExist:
            raise('Essa turma não existe')
        self.make()

    def make(self):
        self._makeQrCode()
        self._makeQrCodeImage()

    def _makeQrCode(self):
        qr = QrCodes.objects.create(qrCode=self.name,
                                    attendance_date=time.strftime("%Y-%m-%d"),
                                    open=datetime.now())
        self.classRef.qrCodes.add(qr)
        self.classRef.qrCodeOpen = qr
        self.classRef.save()
        self.id = qr.id

    def _makeQrCodeImage(self):
        text = json.dumps(self.classRef, cls=JsonEncoder)
        qr = qrcode.QRCode(version=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_L,
                           box_size=3,
                           border=4,
                           )
        qr.add_data(text)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save("backend/static/backend/media/" + self.name + ".png")

    @property
    def imagePath(self):
        return "backend/media/" + self.name + ".png"

    def attendanceId(self):
        return self.id
