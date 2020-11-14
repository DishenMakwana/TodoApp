from todoapp import views
from todolist.views import index
from django.contrib import admin
from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="TodoList"),
    path('todolist/',include('todolist.urls')),
]