""" Unit tests for `core_oaipmh_provider_app.views.admin.ajax` package.
"""
from unittest import TestCase
from unittest.mock import MagicMock, patch

from core_oaipmh_provider_app.views.admin import ajax as admin_ajax


class TestAddSetViewSave(TestCase):
    """Unit tests for `AddSetView._save` method."""

    def setUp(self):
        """setUp"""
        self.mock_view = admin_ajax.AddSetView()
        self.mock_view.object = MagicMock()
        self.mock_view.request = MagicMock()

        self.mock_form = MagicMock()
        self.mock_cleaned_data = MagicMock()
        self.mock_form.cleaned_data = self.mock_cleaned_data
        self.mock_kwargs = {"form": self.mock_form}

    @patch.object(admin_ajax, "oai_provider_set_api")
    @patch.object(admin_ajax, "check_template_manager_in_xsd_format")
    def test_check_template_manager_in_xsd_format_called(
        self,
        mock_check_template_manager_in_xsd_format,
        mock_oai_provider_set_api,
    ):
        """test_check_template_manager_in_xsd_format_called"""
        self.mock_view._save(**self.mock_kwargs)

        mock_check_template_manager_in_xsd_format.assert_called_with(
            self.mock_cleaned_data["templates_manager"], self.mock_view.request
        )

    @patch.object(admin_ajax, "oai_provider_set_api")
    @patch.object(admin_ajax, "check_template_manager_in_xsd_format")
    def test_check_template_manager_in_xsd_format_error_calls_add_error(
        self,
        mock_check_template_manager_in_xsd_format,
        mock_oai_provider_set_api,
    ):
        """test_check_template_manager_in_xsd_format_error_calls_add_error"""
        mock_check_template_manager_in_xsd_format.side_effect = Exception(
            "mock_check_template_manager_in_xsd_format_exception"
        )

        self.mock_view._save(**self.mock_kwargs)

        self.mock_form.add_error.assert_called()

    @patch.object(admin_ajax, "oai_provider_set_api")
    @patch.object(admin_ajax, "check_template_manager_in_xsd_format")
    def test_check_template_manager_in_xsd_format_error_does_not_upsert(
        self,
        mock_check_template_manager_in_xsd_format,
        mock_oai_provider_set_api,
    ):
        """test_check_template_manager_in_xsd_format_error_does_not_upsert"""

        mock_check_template_manager_in_xsd_format.side_effect = Exception(
            "mock_check_template_manager_in_xsd_format_exception"
        )

        self.mock_view._save(**self.mock_kwargs)

        mock_oai_provider_set_api.upsert.assert_not_called()

    @patch.object(admin_ajax, "oai_provider_set_api")
    @patch.object(admin_ajax, "check_template_manager_in_xsd_format")
    def test_upsert_called_twice(
        self,
        mock_check_template_manager_in_xsd_format,
        mock_oai_provider_set_api,
    ):
        """test_upsert_called_twice"""
        self.mock_view._save(**self.mock_kwargs)
        self.assertEqual(mock_oai_provider_set_api.upsert.call_count, 2)


class TestAddSetViewGetFormKwargs(TestCase):
    """Unit tests for `AddSetView.get_form_kwargs` method."""

    def setUp(self):
        """setUp"""
        self.mock_serializer = admin_ajax.AddSetView()
        self.mock_request = MagicMock()
        self.mock_serializer.request = self.mock_request

    @patch.object(admin_ajax.AddObjectModalView, "get_form_kwargs")
    def test_super_get_form_kwargs_called(self, mock_get_form_kwargs):
        """test_super_get_form_kwargs_called"""
        self.mock_serializer.get_form_kwargs()

        mock_get_form_kwargs.assert_called()

    @patch.object(admin_ajax.AddObjectModalView, "get_form_kwargs")
    def test_returns_kwargs_with_request(self, mock_get_form_kwargs):
        """test_returns_kwargs_with_request"""
        mock_kwargs = MagicMock()
        mock_get_form_kwargs.return_value = mock_kwargs
        mock_kwargs["request"] = self.mock_request

        self.assertEqual(self.mock_serializer.get_form_kwargs(), mock_kwargs)


class TestEditSetViewSave(TestCase):
    """Unit tests for `EditSetView._save` method."""

    def setUp(self):
        """setUp"""
        self.mock_view = admin_ajax.EditSetView()
        self.mock_view.object = MagicMock()
        self.mock_view.request = MagicMock()

        self.mock_form = MagicMock()
        self.mock_cleaned_data = MagicMock()
        self.mock_form.cleaned_data = self.mock_cleaned_data
        self.mock_kwargs = {"form": self.mock_form}

    @patch.object(admin_ajax, "oai_provider_set_api")
    @patch.object(admin_ajax, "check_template_manager_in_xsd_format")
    def test_check_template_manager_in_xsd_format_called(
        self,
        mock_check_template_manager_in_xsd_format,
        mock_oai_provider_set_api,
    ):
        """test_check_template_manager_in_xsd_format_called"""
        self.mock_view._save(**self.mock_kwargs)

        mock_check_template_manager_in_xsd_format.assert_called_with(
            self.mock_cleaned_data["templates_manager"], self.mock_view.request
        )

    @patch.object(admin_ajax, "oai_provider_set_api")
    @patch.object(admin_ajax, "check_template_manager_in_xsd_format")
    def test_check_template_manager_in_xsd_format_error_calls_add_error(
        self,
        mock_check_template_manager_in_xsd_format,
        mock_oai_provider_set_api,
    ):
        """test_check_template_manager_in_xsd_format_error_calls_add_error"""
        mock_check_template_manager_in_xsd_format.side_effect = Exception(
            "mock_check_template_manager_in_xsd_format_exception"
        )
        self.mock_view._save(**self.mock_kwargs)

        self.mock_form.add_error.assert_called()

    @patch.object(admin_ajax, "oai_provider_set_api")
    @patch.object(admin_ajax, "check_template_manager_in_xsd_format")
    def test_check_template_manager_in_xsd_format_error_does_not_upsert(
        self,
        mock_check_template_manager_in_xsd_format,
        mock_oai_provider_set_api,
    ):
        """test_check_template_manager_in_xsd_format_error_does_not_upsert"""
        mock_check_template_manager_in_xsd_format.side_effect = Exception(
            "mock_check_template_manager_in_xsd_format_exception"
        )
        self.mock_view._save(**self.mock_kwargs)

        mock_oai_provider_set_api.upsert.assert_not_called()

    @patch.object(admin_ajax, "oai_provider_set_api")
    @patch.object(admin_ajax, "check_template_manager_in_xsd_format")
    def test_upsert_called_twice(
        self,
        mock_check_template_manager_in_xsd_format,
        mock_oai_provider_set_api,
    ):
        """test_upsert_called_twice"""
        self.mock_view._save(**self.mock_kwargs)
        self.assertEqual(mock_oai_provider_set_api.upsert.call_count, 2)


class TestEditSetViewGetInitial(TestCase):
    """Unit tests for `EditSetView.get_initial` method."""

    def setUp(self):
        """setUp"""
        self.mock_serializer = admin_ajax.EditSetView()

        self.mock_request = MagicMock()
        self.mock_serializer.request = self.mock_request

        self.mock_object = MagicMock()
        self.mock_serializer.object = self.mock_object

    @patch.object(admin_ajax.EditObjectModalView, "get_initial")
    def test_super_get_initial_called(self, mock_get_initial):
        """test_super_get_initial_called"""
        self.mock_serializer.get_initial()

        mock_get_initial.assert_called()

    @patch.object(admin_ajax.EditObjectModalView, "get_initial")
    def test_returns_initial(self, mock_get_initial):
        """test_returns_initial_with_templates_manager"""
        mock_kwargs = MagicMock()
        mock_get_initial.return_value = mock_kwargs

        self.assertEqual(self.mock_serializer.get_initial(), mock_kwargs)


class TestEditSetViewGetFormKwargs(TestCase):
    """Unit tests for `EditSetView.get_form_kwargs` method."""

    def setUp(self):
        """setUp"""
        self.mock_serializer = admin_ajax.EditSetView()
        self.mock_request = MagicMock()
        self.mock_serializer.request = self.mock_request

    @patch.object(admin_ajax.EditObjectModalView, "get_form_kwargs")
    def test_super_get_form_kwargs_called(self, mock_get_form_kwargs):
        """test_super_get_form_kwargs_called"""
        self.mock_serializer.get_form_kwargs()

        mock_get_form_kwargs.assert_called()

    @patch.object(admin_ajax.EditObjectModalView, "get_form_kwargs")
    def test_returns_kwargs_with_request(self, mock_get_form_kwargs):
        """test_returns_kwargs_with_request"""
        mock_kwargs = MagicMock()
        mock_get_form_kwargs.return_value = mock_kwargs
        mock_kwargs["request"] = self.mock_request

        self.assertEqual(self.mock_serializer.get_form_kwargs(), mock_kwargs)
