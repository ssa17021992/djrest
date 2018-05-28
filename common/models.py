from django.db import models

from .utils import unique_id, get_object_or_none


class BaseModel(models.Model):
    """Base model"""

    id = models.CharField(max_length=22, editable=False, primary_key=True)

    def __make_id(self):
        uid = unique_id()[::2]  # Limited to 11 characters
        obj = get_object_or_none(self.__class__, pk=uid)

        self.id = uid if not obj else ''

    def save(self, *args, **kwargs):
        while not self.id: self.__make_id()
        super(BaseModel, self).save(*args, **kwargs)

    class Meta:
        abstract = True
