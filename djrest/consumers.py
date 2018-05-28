import json

from django.utils.translation import gettext as _

from common.consumers import Consumer


class NotFoundConsumer(Consumer):
    """Not found consumer"""

    def connect(self):
        self.accept()

        self.send(text_data=json.dumps({
            'detail': _('Not found.')
        }))

        self.close()
