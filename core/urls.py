from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.index, name="index"),
    path('register/', views.register, name='register'),
    path("upload/", views.file_upload_view, name="file_upload"),
    # path("upload/", views.upload_view, name="upload"),
    path("download/<int:pk>/", views.download_decrypt, name="download"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", views.logout_view, name="logout"),
]

handler404 = views.custom_404_view
handler500 = views.custom_500_view
