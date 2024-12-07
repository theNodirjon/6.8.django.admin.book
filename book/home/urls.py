from django.urls import path
from . import views

urlpatterns = [
    path('', views.list_books, name='home'),
    path('create/', views.create_book, name='create_book'),
    path('update/<int:book_id>/', views.update_book, name='update_book'),
    path('delete/<int:book_id>/', views.delete_book, name='delete_book'),
]
