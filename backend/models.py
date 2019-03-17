from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.conf import settings
import json
import qrcode


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        return obj.jsonSerialize()


class Classes(models.Model):
    """
    datas about the classes
    """
    name = models.CharField(max_length=30)
    qrCodeOpen = models.IntegerField(default=0)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL, blank=True,
                                null=True, related_name="classes")

    def __str__(self):
        return f"{self.id} - {self.name}"

    @property
    def presences(self):
        """
        all students that registered for the presence
        """
        attendances = {}
        for qr in self.qrCodes.all():
            try:
                students_qrCode = qr.students_qrCode.all()
                if qr.attendance_date not in attendances:
                    attendances.setdefault(qr.attendance_date,
                                           list(students_qrCode))
                else:
                    attendances[qr.attendance_date] += list(students_qrCode)
            except ObjectDoesNotExist:
                pass
        return attendances

    def jsonSerialize(self):
        """
        json serializable
        """
        d = {}
        for student in self.students.all():
            ra, name = str(student).split(':')
            d[ra] = name
        return d


class QrCodes(models.Model):
    """
    all qrcodes generated
    """
    qrCode = models.ImageField(default=False)
    attendance_date = models.DateField(default='2018-01-01')
    open = models.DateTimeField(default=None)
    close = models.DateTimeField(blank=True, null=True)
    classRef = models.ForeignKey(Classes, on_delete=models.CASCADE,
                                 default=1,
                                 related_name="qrCodes")

    def makeQrCode(self):
        self._openAttendance()
        self._makeQrCodeImage()

    def _openAttendance(self):
        """
        relates the qr code to the class.
        """
        self.classRef.qrCodeOpen = self.id
        self.classRef.save()

    def _makeQrCodeImage(self):
        """
        create the png image.
        """
        text = json.dumps(self.classRef, cls=JsonEncoder)
        datas = {
            'version': 1,
            'error_correction': qrcode.constants.ERROR_CORRECT_L,
            'box_size': 3,
            'border': 4,
        }
        qrCodeImage = qrcode.QRCode(**datas)
        qrCodeImage.add_data(text)
        qrCodeImage.make(fit=True)
        img = qrCodeImage.make_image(fill_color="black", back_color="white")
        img.save("backend/static/backend/media/" + str(self.qrCode))

    @property
    def imagePath(self):
        return self.qrCode
        return "backend/media/" + self.qrCode + ".png"


class Students(models.Model):
    """
    datas about the students
    """
    ra = models.CharField(max_length=10)
    name = models.CharField(max_length=70)
    class_student = models.ManyToManyField(Classes, blank=True,
                                           related_name="students")
    qrCodes = models.ManyToManyField(QrCodes, blank=True,
                                     related_name="students_qrCode")

    def __str__(self):
        return f"{self.ra}: {self.name}"
