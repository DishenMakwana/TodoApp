from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>', views.index, name='index'),
]

# Add Django site authentication urls (for login, logout, password management)

urlpatterns += {
    path('accounts/', include('django.contrib.auth.urls')),
}

urlpatterns += [
    path("register/", views.register, name="register"),
]
