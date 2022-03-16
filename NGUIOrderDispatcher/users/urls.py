from django.urls import path
import users.views as views


urlpatterns = [
    path('login/', views.loginUser, name="login_view"),
    path('logout', views.logout_view, name="logout_view"),
]
