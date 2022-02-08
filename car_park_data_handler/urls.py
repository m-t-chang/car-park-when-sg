from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('scrape/', views.scrape, name='scrape'),
    path('transform/', views.transform_to_sql, name='transform'),
    path('<str:car_park_id>/', views.detail, name='detail'),
]
