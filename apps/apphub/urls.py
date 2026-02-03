from django.urls import path
from . import views

app_name = 'apphub'

urlpatterns = [
    path('', views.app_list_view, name='app_list'),
    path('<slug:slug>/', views.app_access_view, name='app_access'),
    path('<slug:slug>/content/', views.app_html_content, name='app_html_content'),
]
