from django.conf.urls import url
from services import views

app_name = "services"

urlpatterns = [
    url(r'^user_login/$', views.user_login, name = 'user_login'),
    url(r'^account/', views.user_account, name = 'account'),
    url(r'^upload/', views.upload, name = 'upload_file'),
    url(r'^$logout/', views.user_logout, name = 'logout')
]
