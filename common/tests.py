from django.test import TestCase

from .utils import unique_id, to_object


class UniqueIdTestCase(TestCase):
    """Unique id test case"""

    def test_unique_id_length(self):
        uid = unique_id()
        self.assertEqual(len(uid), 22)


class ToObjectTestCase(TestCase):
    """To object test case"""

    def test_dict_to_object(self):
        obj = to_object({'pi': 3.14})
        self.assertTrue(hasattr(obj, 'pi'))
