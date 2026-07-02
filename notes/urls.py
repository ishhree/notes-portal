from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload_note, name='upload'),
    path('edit/<int:id>/', views.edit_note, name='edit'),
    path('delete/<int:id>/', views.delete_note, name='delete'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('adminboard/', views.adminboard, name='adminboard'),
    path('fav/<int:id>/', views.toggle_fav, name='toggle_fav'),
    path('favorites/', views.favorites, name='favorites'),
    path('edit/<int:id>/', views.edit_note, name='edit_note'),
    path('view-pdf/<int:id>/', views.open_pdf, name='view_pdf'),
]