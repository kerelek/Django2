# medical_data/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_medical_record, name='create_record'),
    path('upload/', views.upload_json_file, name='upload_json'),  # ← убедись что именно такое имя
    path('files/', views.view_json_files, name='view_json_files'),
    #path('records/', views.view_medical_records, name='view_records'),
]
