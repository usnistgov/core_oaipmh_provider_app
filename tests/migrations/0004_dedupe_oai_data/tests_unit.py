"""Unit tests for data migrations"""

import importlib
from unittest.mock import MagicMock

from django.test import TestCase as DjangoTestCase

dedupe_oai_data = importlib.import_module(
    "core_oaipmh_provider_app.migrations.0004_dedupe_oai_data"
).dedupe_oai_data


class TestDedupeOaiDataMigration(DjangoTestCase):
    @staticmethod
    def _mock_apps(duplicate_data_ids, group_querysets):
        """Build a fake `apps` registry returning a mocked OaiData model.

        Args:
            duplicate_data_ids: data ids returned as having duplicates.
            group_querysets: dict mapping data_id -> queryset mock returned by
                `OaiData.objects.filter(data_id=<id>)`.

        Returns:
            Fake apps registry.
        """
        duplicates_qs = MagicMock()
        duplicates_qs.values.return_value.annotate.return_value.filter.return_value.values_list.return_value = (
            duplicate_data_ids
        )

        def filter_side_effect(*args, **kwargs):
            if "data_id" in kwargs:
                return group_querysets[kwargs["data_id"]]
            return duplicates_qs

        mock_model = MagicMock()
        mock_model.objects.filter.side_effect = filter_side_effect

        class MockApps:
            @staticmethod
            def get_model(app_label, model_name):  # noqa
                return mock_model

        return MockApps()

    def test_dedupe_oai_data_keeps_latest_deletes_rest(self):
        """test_dedupe_oai_data_keeps_latest_deletes_rest"""
        best = MagicMock(pk=10)
        group_qs = MagicMock()
        group_qs.order_by.return_value.first.return_value = best
        excluded_qs = MagicMock()
        group_qs.exclude.return_value = excluded_qs

        apps = self._mock_apps([1], {1: group_qs})

        dedupe_oai_data(apps, None)

        group_qs.exclude.assert_called_once_with(pk=10)
        excluded_qs.delete.assert_called_once()

    def test_dedupe_oai_data_no_duplicates_does_not_delete(self):
        """test_dedupe_oai_data_no_duplicates_does_not_delete"""
        apps = self._mock_apps([], {})

        # No duplicate group means no further filter/delete call happens;
        # `group_querysets` being empty would raise KeyError otherwise.
        dedupe_oai_data(apps, None)
