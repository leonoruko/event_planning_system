from django.urls import path
from .views import ProfileDetailView,CustomConfirmEmailView
urlpatterns=[
    path('profile/',ProfileDetailView.as_view(),name='user-profile'),
    path('account-confirm-email/<str:key>/',CustomConfirmEmailView.as_view(),name='account_confirm_email')
]