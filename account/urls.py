from django.urls import path
from .views import register
from django.contrib.auth.views import (LoginView,LogoutView,
                                        PasswordChangeView,PasswordChangeDoneView,
                                        PasswordResetCompleteView,PasswordResetConfirmView,
                                        PasswordResetDoneView,PasswordResetView)

urlpatterns = [
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('password_change/',PasswordChangeView.as_view(),name="password_change"),
    path('password_change_done/',PasswordChangeDoneView.as_view(),name="password_change_done"),
    #reset password
    path('password_reset/',PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/',PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/',PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    #register
    path('register/',register,name="register")

]
