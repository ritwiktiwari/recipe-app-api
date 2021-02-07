from django.urls import path

from . import views

app_name = 'user'

urlpatterns = [
    path('create/', view=views.CreateUserView.as_view(), name='create'),
    path('token/', view=views.CreateTokenView.as_view(), name='token'),
]
