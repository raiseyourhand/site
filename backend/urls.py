from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('login', views.AuthView.as_view(), name='login'),
    path('logout', views.logout_view, name='logout'),
    path('classes', views.ClassesView.as_view(), name='classes'),
    path('attendance/<int:id>', views.CreateAttendanceView.as_view(),
         name='attendance'),
    path('attendance/close/<int:id>', views.CloseAttendanceView.as_view(),
         name='attendanceClose'),
    path('create/class', views.CreateClassView.as_view(), name='createClass'),
]
