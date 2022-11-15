""" Mock classes for use in unit tests.
"""
from unittest.mock import Mock


class MockQuerySet(Mock):
    """Mock Query Set"""

    item_list = []

    def order_by(self, *field_names):
        """order_by

        Args:
            field_names:

        Returns:
        """
        return self.item_list


class MockPassThrough(Mock):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.args = args if args else None
        self.kwargs = kwargs if kwargs else None

    def all(self):
        return self
