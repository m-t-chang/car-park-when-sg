from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from . import views

urlpatterns = [
    # authentication
    path('token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # user management
    path('user/signup/', views.UserAddNew.as_view(), name='user_add_new'),

    # data
    path('carpark-list/', views.CarparkList.as_view()),
    path('carpark-detail/<str:carpark_id>/', views.CarparkDetail.as_view()),
]
