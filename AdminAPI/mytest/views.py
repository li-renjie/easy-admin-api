from django.shortcuts import render
from django.http import HttpResponse
from .models import Student
from rest_framework.viewsets import ModelViewSet
from .serializers import StudentSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

