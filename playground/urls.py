from django.urls import path
from . import views

# URLConf
urlpatterns = [path("hello/", views.TestChacheView.as_view())]
