from django.urls import path

from . import views

urlpatterns = [
    # path('', views.parking_map, name="parking_map"),
    path('', views.main_page, name="main_page"),
    path('form_login/', views.form_login, name="form_login"),
    path('form_signup/', views.form_signup, name="form_signup"),
    path('parking_map/', views.parking_map, name="parking_map"),
    path('signup_view/', views.signup_view, name="signup_view"),
    path('login_view/', views.login_view, name="login_view"),
    path('booking_view/', views.booking_view, name="booking_view"),
    path('logout_view/', views.logout_view, name="logout_view"),
    path('bringout_view/', views.bringout_view, name="bringout_view"),
    path('feedback_view/', views.feedback_view, name="feedback_view")

]
