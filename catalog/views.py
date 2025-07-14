from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404

from catalog.models import Book, Author, BookInstance, Genre
from catalog.constants import (
    LOAN_STATUS_AVAILABLE,
    LOAN_STATUS_MAINTENANCE,
    PAGINATE_BY_DEFAULT,
)


def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    num_instances_available = BookInstance.objects.filter(status=LOAN_STATUS_AVAILABLE).count()

    num_authors = Author.objects.count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
    }

    return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
    model = Book
    paginate_by = PAGINATE_BY_DEFAULT


class BookDetailView(generic.DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = self.object
        copies = book.bookinstance_set.all()

        context['copies'] = copies
        context['STATUS_AVAILABLE'] = LOAN_STATUS_AVAILABLE
        context['STATUS_MAINTENANCE'] = LOAN_STATUS_MAINTENANCE
        return context
