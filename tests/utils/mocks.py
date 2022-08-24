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
