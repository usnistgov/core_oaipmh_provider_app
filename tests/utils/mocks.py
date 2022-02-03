""" Mock classes for use in unit tests.
"""
from unittest.mock import Mock


class MockQuerySet(Mock):
    item_list = []

    def order_by(self, *field_names):
        return self.item_list
