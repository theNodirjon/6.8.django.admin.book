from django.shortcuts import render, redirect
from .models.books import Book

def create_book(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        published_date = request.POST.get('published_date')
        Book.objects.create(title=title, author=author, published_date=published_date)
        return redirect('home')
    return render(request, 'create.html')

def list_books(request):
    books = Book.objects.all()
    return render(request, 'list.html', {'books': books})

def update_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == "POST":
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.published_date = request.POST.get('published_date')
        book.save()
        return redirect('home')
    return render(request, 'edit.html', {'book': book})

def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect('home')
    return render(request, 'delete.html', {'book': book})

