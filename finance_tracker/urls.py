from django.contrib import admin
from django.urls import path, include
from expenses import views as expense_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('expenses/', include('expenses.urls')),
    path('', expense_views.index, name='home'),
]
