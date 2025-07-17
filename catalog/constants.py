from django.utils.translation import gettext_lazy as _

MAX_LENGTH_TITLE = 200
MAX_LENGTH_NAME = 100
MAX_LENGTH_SUMMARY = 1000
MAX_LENGTH_ISBN = 13
MAX_LENGTH_IMPRINT = 200
MAX_LENGTH_LOAN_STATUS = 1

MAX_DISPLAY_GENRES = 3

# Loan status choices
LOAN_STATUS_AVAILABLE = 'a'
LOAN_STATUS = (
    ('m', _('Maintenance')),
    ('o', _('On loan')),
    (LOAN_STATUS_AVAILABLE, _('Available')),
    ('r', _('Reserved')),
)
