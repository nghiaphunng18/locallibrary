from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from catalog.models import Book, Author, BookInstance, Genre
from catalog.constants import (
    LOAN_STATUS_AVAILABLE,
    LOAN_STATUS_MAINTENANCE,
    PAGINATE_BY_DEFAULT,
    LOAN_STATUS_ON_LOAN
)


def index(request):
    num_books = Book.objects.count()
    num_instances = BookInstance.objects.count()

    num_instances_available = BookInstance.objects.filter(status=LOAN_STATUS_AVAILABLE).count()

    num_authors = Author.objects.count()

    # number of visits to this view, as counted in the session variable
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
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


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = PAGINATE_BY_DEFAULT

    def get_queryset(self):
        return BookInstance.objects.filter(
            borrower=self.request.user,
            status=LOAN_STATUS_ON_LOAN
        ).order_by('due_back')
