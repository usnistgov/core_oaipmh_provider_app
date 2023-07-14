""" Test forms from `views.admin.forms`.
"""
from unittest.case import TestCase


from core_main_app.utils.tests_tools.RequestMock import create_mock_request

from core_main_app.utils.tests_tools.MockUser import create_mock_user

from core_oaipmh_provider_app.views.admin.forms import (
    TemplateMetadataFormatForm,
    MappingXSLTForm,
)
from django.test import override_settings


class TestTemplateMetadataFormatForm(TestCase):
    """Test Template Metadata Format Form"""

    @override_settings(BOOTSTRAP_VERSION="4.6.2")
    def test_template_metadata_format_form_bootstrap_v4(self):
        """test_template_metadata_format_form_bootstrap_v4

        Returns:

        """
        # Arrange
        mock_request = create_mock_request(user=create_mock_user("1"))
        data = {"metadata_prefix": "test"}

        # Act
        form = TemplateMetadataFormatForm(data, request=mock_request)

        # Assert
        self.assertEquals(
            form.fields["template"].widget.attrs["class"], "form-control"
        )

    @override_settings(BOOTSTRAP_VERSION="5.1.3")
    def test_template_metadata_format_form_bootstrap_v5(self):
        """test_template_metadata_format_form_bootstrap_v5

        Returns:

        """
        # Arrange
        mock_request = create_mock_request(user=create_mock_user("1"))
        data = {"metadata_prefix": "test"}

        # Act
        form = TemplateMetadataFormatForm(data, request=mock_request)

        # Assert
        self.assertEquals(
            form.fields["template"].widget.attrs["class"], "form-select"
        )


class TestMappingXSLTForm(TestCase):
    """Test Mapping XSLT Form"""

    @override_settings(BOOTSTRAP_VERSION="4.6.2")
    def test_mapping_xslt_form_bootstrap_v4(self):
        """test_mapping_xslt_form_bootstrap_v4

        Returns:

        """
        # Arrange
        mock_request = create_mock_request(user=create_mock_user("1"))
        data = {"oai_metadata_format": "test"}

        # Act
        form = MappingXSLTForm(data, request=mock_request)

        # Assert
        self.assertEquals(
            form.fields["template"].widget.attrs["class"], "form-control"
        )
        self.assertEquals(
            form.fields["xslt"].widget.attrs["class"], "form-control"
        )

    @override_settings(BOOTSTRAP_VERSION="5.1.3")
    def test_mapping_xslt_form_bootstrap_v5(self):
        """test_mapping_xslt_form_bootstrap_v5

        Returns:

        """
        # Arrange
        mock_request = create_mock_request(user=create_mock_user("1"))
        data = {"oai_metadata_format": "test"}

        # Act
        form = MappingXSLTForm(data, request=mock_request)

        # Assert
        self.assertEquals(
            form.fields["template"].widget.attrs["class"], "form-select"
        )
        self.assertEquals(
            form.fields["xslt"].widget.attrs["class"], "form-select"
        )
