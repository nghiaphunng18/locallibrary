import uuid

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .constants import (
    MAX_LENGTH_TITLE,
    MAX_LENGTH_NAME,
    MAX_LENGTH_ISBN,
    MAX_LENGTH_IMPRINT,
    MAX_LENGTH_SUMMARY,
    MAX_LENGTH_LOAN_STATUS,
    LOAN_STATUS
)

# Create your models here.
class Genre(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        help_text=_('Enter a book genre (e.g.Science Fiction)')
    )

    def __str__(self):
        """String for representing the Model object"""
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=MAX_LENGTH_TITLE)

    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=MAX_LENGTH_SUMMARY, help_text=_('Enter a brief description of the book'))
    isbn = models.CharField('ISBN', max_length=MAX_LENGTH_ISBN, unique=True,
                            help_text=_('13-Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>'))

    genre = models.ManyToManyField(Genre, help_text=_('Select a genre for this book'))

    def __str__(self):
        """String for representing the Model object"""
        return self.title

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text=_('Unique ID for this particular book across whole library'))
    book = models.ForeignKey('Book', on_delete=models.RESTRICT)
    imprint = models.CharField(max_length=MAX_LENGTH_IMPRINT)
    due_back = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=MAX_LENGTH_LOAN_STATUS,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text=_('Book availability'),
    )

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        """String for representing the Model object"""
        return f'{self.id} ({self.book.title})'

class Author(models.Model):
    first_name = models.CharField(max_length=MAX_LENGTH_NAME)
    last_name = models.CharField(max_length=MAX_LENGTH_NAME)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object"""
        return f'{self.last_name}, {self.first_name}'
