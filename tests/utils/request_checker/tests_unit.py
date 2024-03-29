""" Unit tests for the `core_oaipmh_provider_app.utils.request_checker` package.
"""

from unittest import TestCase
from unittest.mock import MagicMock, patch, call

from core_oaipmh_provider_app.utils import request_checker
from core_oaipmh_provider_app.commons import (
    exceptions as core_oaipmh_provider_exceptions,
)


class TestCheckResumptionToken(TestCase):
    """Unit tests for the `check_resumption_token` function."""

    def setUp(self):
        """setUp"""
        self.mock_kwargs = {"resumption_token": MagicMock()}

    @patch.object(request_checker, "oai_request_page_api")
    def test_get_by_resumption_token_called(self, mock_oai_request_page_api):
        """test_get_by_resumption_token_called"""
        with self.assertRaises(
            core_oaipmh_provider_exceptions.BadResumptionToken
        ):
            request_checker.check_resumption_token(**self.mock_kwargs)

        mock_oai_request_page_api.get_by_resumption_token.assert_called_with(
            self.mock_kwargs["resumption_token"]
        )

    @patch.object(request_checker, "oai_request_page_api")
    @patch.object(request_checker, "datetime_utils")
    def test_datetime_to_utc_datetime_iso8601_called(
        self, mock_datetime_utils, mock_oai_request_page_api
    ):
        """test_datetime_to_utc_datetime_iso8601_called"""
        mock_oai_request_page_object = MagicMock()
        mock_oai_request_page_api.get_by_resumption_token.return_value = (
            mock_oai_request_page_object
        )

        with self.assertRaises(
            core_oaipmh_provider_exceptions.BadResumptionToken
        ):
            request_checker.check_resumption_token(**self.mock_kwargs)

        mock_datetime_utils.datetime_to_utc_datetime_iso8601.assert_has_calls(
            [
                call(mock_oai_request_page_object.expiration_date),
                call(mock_datetime_utils.datetime_now()),
            ]
        )

    @patch.object(request_checker, "oai_request_page_api")
    @patch.object(request_checker, "datetime_utils")
    def test_expired_token_raises_bad_resumption_token(
        self, mock_datetime_utils, mock_oai_request_page_api
    ):
        """test_expired_token_raises_bad_resumption_token"""
        mock_oai_request_page_object = MagicMock()
        mock_oai_request_page_object.expiration_date = 0
        mock_oai_request_page_api.get_by_resumption_token.return_value = (
            mock_oai_request_page_object
        )

        mock_datetime_utils.datetime_now.return_value = 1
        mock_datetime_utils.datetime_to_utc_datetime_iso8601.side_effect = (
            lambda input_date: input_date
        )

        with self.assertRaises(
            core_oaipmh_provider_exceptions.BadResumptionToken
        ):
            request_checker.check_resumption_token(**self.mock_kwargs)

    @patch.object(request_checker, "oai_request_page_api")
    @patch.object(request_checker, "datetime_utils")
    def test_fresh_token_returns_page_object(
        self, mock_datetime_utils, mock_oai_request_page_api
    ):
        """test_fresh_token_returns_page_object"""
        mock_oai_request_page_object = MagicMock()
        mock_oai_request_page_object.expiration_date = 1
        mock_oai_request_page_api.get_by_resumption_token.return_value = (
            mock_oai_request_page_object
        )

        mock_datetime_utils.datetime_now.return_value = 0
        mock_datetime_utils.datetime_to_utc_datetime_iso8601.side_effect = (
            lambda input_date: input_date
        )

        results = request_checker.check_resumption_token(**self.mock_kwargs)

        self.assertEqual(results, mock_oai_request_page_object)
