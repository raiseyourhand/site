from rest_framework.authentication import (SessionAuthentication,
                                           BasicAuthentication)
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import StudentSerealizer, QrCodesSerializer
from backend.models import Students, QrCodes


class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return


class StudentsView(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication,
                              BasicAuthentication)

    def get(self, request, pk=None):
        try:
            if pk:
                try:
                    student = Students.objects.get(ra=pk)
                except ObjectDoesNotExist:
                    student = Students.objects.get(pk=pk)
                serealizer = StudentSerealizer(student)
            else:
                student = Students.objects.all()
                serealizer = StudentSerealizer(student, many=True)
            return Response(serealizer.data)
        except ObjectDoesNotExist:
            return Response(request.data, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        isAccepted = False
        try:
            student = Students.objects.get(pk=pk)
        except ObjectDoesNotExist:
            student = Students.objects.get(ra=pk)

        try:
            for pk in request.data['qrCodes']:
                qr = QrCodes.objects.get(pk=pk)
                if qr.close is None:
                    student.qrCodes.add(qr)
                    isAccepted = True
        except (KeyError, ObjectDoesNotExist):
            return Response(request.data,
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        if isAccepted:
            serializer = StudentSerealizer(student)
            return Response(serializer.data,
                            status=status.HTTP_202_ACCEPTED)
        return Response("esta chamada já foi fechada",
                        status=status.HTTP_401_UNAUTHORIZED)


class QrCodesView(APIView):
    def get(self, request, pk):
        try:
            qr = QrCodes.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = QrCodesSerializer(qr)
        return Response(serializer.data)
