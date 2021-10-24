from django.urls import path

from . import views

app_name = 'fin_con'

urlpatterns = [
    path('', views.home, name='home'),
    path('spending/', views.spending, name='spending'),
    path('report/', views.report, name='report'),
]
