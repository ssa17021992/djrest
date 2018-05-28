from django.utils.translation import gettext_lazy as _
from django.utils.deconstruct import deconstructible
from django.core.validators import ValidationError


@deconstructible
class FileSizeValidator:
    """File size validator"""

    message = _('Maximum file size allowed is %(max_size)s KB.')
    code = 'invalid_size'

    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, value):
        size = value.size / 1024.0
        if size > self.max_size:
            raise ValidationError(self.message % {
                'max_size': self.max_size
            }, code=self.code)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.message == other.message and
            self.code == other.code
        )
