from api.serializers import BookSerializer
from books.models import Book
from rest_framework import viewsets


class BooksView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
