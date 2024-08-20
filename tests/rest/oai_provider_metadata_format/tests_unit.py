""" Unit Test Rest OaiProviderMetadataFormat
"""

from random import randint
from unittest.mock import patch, Mock

import requests
from django.test.testcases import SimpleTestCase, TestCase
from rest_framework import status

from core_main_app.commons import exceptions
from core_main_app.components.template import api as template_api
from core_main_app.components.template.models import Template
from core_main_app.components.xsl_transformation.models import (
    XslTransformation,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_oaipmh_provider_app.components.oai_provider_metadata_format import (
    api as oai_provider_metadata_format_api,
)
from core_oaipmh_provider_app.components.oai_provider_metadata_format.models import (
    OaiProviderMetadataFormat,
)
from core_oaipmh_provider_app.components.oai_xsl_template.models import (
    OaiXslTemplate,
)
from core_oaipmh_provider_app.rest.oai_provider_metadata_format import (
    views as rest_oai_provider_metadata_format,
)


class TestSelectMetadataFormat(SimpleTestCase):
    """Test Select Metadata Format"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.param = {"metadata_format_id": randint(1, 100)}

    def test_select_metadata_format_unauthorized(self):
        """test_select_metadata_format_unauthorized"""

        # Arrange
        user = create_mock_user("1", is_staff=False)

        # Act
        response = RequestMock.do_request_get(
            rest_oai_provider_metadata_format.MetadataFormatDetail.as_view(),
            user,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(OaiProviderMetadataFormat, "get_by_id")
    def test_select_metadata_format_not_found(self, mock_get_by_id):
        """test_select_metadata_format_not_found"""

        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.do_request_get(
            rest_oai_provider_metadata_format.MetadataFormatDetail.as_view(),
            user=create_mock_user("1", is_staff=True),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestSelectAllMetadataFormats(SimpleTestCase):
    """Test Select All Metadata Formats"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = None

    def test_select_all_metadata_formats_unauthorized(self):
        """test_select_all_metadata_formats_unauthorized"""

        # Arrange
        user = create_mock_user("1", is_staff=False)

        # Act
        response = RequestMock.do_request_get(
            rest_oai_provider_metadata_format.MetadataFormatsList.as_view(),
            user,
            self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class TestAddMetadataFormat(SimpleTestCase):
    """Test Add Metadata Format"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = {
            "metadata_prefix": "oai_test",
            "schema_url": "http://www.dummy.org",
        }
        self.bad_data = {}

    def test_add_metadata_format_unauthorized(self):
        """test_add_metadata_format_unauthorized"""

        # Arrange
        user = create_mock_user("1", is_staff=False)

        # Act
        response = RequestMock.do_request_post(
            rest_oai_provider_metadata_format.MetadataFormatsList.as_view(),
            user,
            self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_metadata_format_serializer_invalid(self):
        """test_add_metadata_format_serializer_invalid"""

        # Act
        response = RequestMock.do_request_post(
            rest_oai_provider_metadata_format.MetadataFormatsList.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.bad_data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(requests, "get")
    def test_add_metadata_format_raises_exception_if_bad_schema_url(
        self, mock_get
    ):
        """test_add_metadata_format_raises_exception_if_bad_schema_url"""

        # Arrange
        text = "<test>Hello</test>"
        mock_get.return_value.status_code = status.HTTP_404_NOT_FOUND
        mock_get.return_value.text = text

        # Act
        response = RequestMock.do_request_post(
            rest_oai_provider_metadata_format.MetadataFormatsList.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(requests, "get")
    def test_add_metadata_format_raises_exception_if_bad_xml(self, mock_get):
        """test_add_metadata_format_raises_exception_if_bad_xml"""

        # Arrange
        text = "<test>Hello/test>"
        mock_get.return_value.status_code = status.HTTP_200_OK
        mock_get.return_value.text = text

        # Act
        response = RequestMock.do_request_post(
            rest_oai_provider_metadata_format.MetadataFormatsList.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestAddTemplateMetadataFormat(SimpleTestCase):
    """Test Add Template Metadata Format"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = {
            "metadata_prefix": "oai_test",
            "template_id": randint(1, 100),
        }
        self.bad_data = {}

    def test_add_template_metadata_format_unauthorized(self):
        """test_add_template_metadata_format_unauthorized"""

        # Arrange
        user = create_mock_user("1", is_staff=False)

        # Act
        response = RequestMock.do_request_post(
            rest_oai_provider_metadata_format.TemplateAsMetadataFormat.as_view(),
            user,
            self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_template_metadata_format_serializer_invalid(self):
        """test_add_template_metadata_format_serializer_invalid"""

        # Act
        response = RequestMock.do_request_post(
            rest_oai_provider_metadata_format.TemplateAsMetadataFormat.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.bad_data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(template_api, "get_by_id")
    def test_add_template_metadata_format_raises_exception_if_template_does_not_exist(
        self, mock_get_by_id
    ):
        """test_add_template_metadata_format_raises_exception_if_template_does_not_exist"""

        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.do_request_post(
            rest_oai_provider_metadata_format.TemplateAsMetadataFormat.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestUpdateMetadataFormat(SimpleTestCase):
    """Test Update Metadata Format"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = {"metadata_prefix": "oai_update"}
        self.param = {"metadata_format_id": randint(1, 100)}
        self.bad_data = {}

    def test_update_metadata_format_unauthorized(self):
        """test_update_metadata_format_unauthorized"""

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_provider_metadata_format.MetadataFormatDetail.as_view(),
            user=create_mock_user("1", is_staff=False),
            data=self.data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(OaiProviderMetadataFormat, "get_by_id")
    def test_update_metadata_format_serializer_invalid(
        self, mock_metadata_format
    ):
        """test_update_metadata_format_serializer_invalid"""

        # Arrange
        mock_metadata_format.return_value = Mock(
            spec=OaiProviderMetadataFormat()
        )
        # Act
        response = RequestMock.do_request_patch(
            rest_oai_provider_metadata_format.MetadataFormatDetail.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.bad_data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(OaiProviderMetadataFormat, "get_by_id")
    def test_update_metadata_format_not_found(self, mock_get_by_id):
        """test_update_metadata_format_not_found"""

        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.do_request_patch(
            rest_oai_provider_metadata_format.MetadataFormatDetail.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.data,
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestTemplateToMetadataFormatMappingXslt(TestCase):
    """Test Template To Metadata Format Mapping Xslt"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = {
            "template": randint(1, 100),
            "oai_metadata_format": randint(1, 100),
            "xslt": randint(1, 100),
        }
        self.bad_data = {}

    def test_template_to_metadata_format_mapping_xslt_unauthorized(self):
        """test_template_to_metadata_format_mapping_xslt_unauthorized"""

        # Act
        response = RequestMock.do_request_post(
            rest_oai_provider_metadata_format.TemplateMetadataFormatXSLT.as_view(),
            user=create_mock_user("1", is_staff=False),
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_template_to_metadata_format_mapping_xslt_serializer_invalid(self):
        """test_template_to_metadata_format_mapping_xslt_serializer_invalid"""

        # Act
        response = RequestMock.do_request_post(
            rest_oai_provider_metadata_format.TemplateMetadataFormatXSLT.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.bad_data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(Template, "get_by_id")
    def test_template_to_metadata_format_mapping_xslt_template_not_found(
        self, mock_get_by_id
    ):
        """test_template_to_metadata_format_mapping_xslt_template_not_found"""

        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.do_request_post(
            rest_oai_provider_metadata_format.TemplateMetadataFormatXSLT.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(XslTransformation, "get_by_id")
    @patch.object(Template, "get_by_id")
    def test_template_to_metadata_format_mapping_xslt_oai_xslt_template_not_found(
        self, mock_get_template, mock_get_by_id
    ):
        """test_template_to_metadata_format_mapping_xslt_oai_xslt_template_not_found"""

        # Arrange
        mock_get_template.return_value = Mock(spec=Template)
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.do_request_post(
            rest_oai_provider_metadata_format.TemplateMetadataFormatXSLT.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(OaiProviderMetadataFormat, "get_by_id")
    @patch.object(Template, "get_by_id")
    @patch.object(XslTransformation, "get_by_id")
    def test_template_to_metadata_format_mapping_xslt_metadata_format_not_found(
        self, mock_get_xslt, mock_get_template, mock_get_by_id
    ):
        """test_template_to_metadata_format_mapping_xslt_metadata_format_not_found"""

        # Arrange
        mock_get_xslt.return_value = Mock(spec=XslTransformation)
        mock_get_template.return_value = Mock(spec=Template)
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.do_request_post(
            rest_oai_provider_metadata_format.TemplateMetadataFormatXSLT.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    @patch.object(OaiProviderMetadataFormat, "get_by_id")
    @patch.object(Template, "get_by_id")
    @patch.object(XslTransformation, "get_by_id")
    def test_template_to_metadata_format_mapping_xslt_impossible_temp_meta_form(
        self, mock_get_xslt, mock_get_template, mock_get_meta_form
    ):
        """test_template_to_metadata_format_mapping_xslt_impossible_temp_meta_form"""

        # Arrange
        mock_get_xslt.return_value = Mock(spec=XslTransformation)
        mock_get_template.return_value = Mock(spec=Template)
        mock_metadata_format = OaiProviderMetadataFormat()
        # Metadata format is template
        mock_metadata_format.is_template = True
        mock_get_meta_form.return_value = mock_metadata_format

        # Act
        response = RequestMock.do_request_post(
            rest_oai_provider_metadata_format.TemplateMetadataFormatXSLT.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.data,
        )

        # Assert
        self.assertEqual(
            response.data["message"]["oai_metadata_format"],
            ["Impossible to map a XSLT to a template metadata format"],
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestTemplateToMetadataFormatUnMappingXslt(SimpleTestCase):
    """Test Template To Metadata Format UnMapping Xslt"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.data = {
            "template_id": randint(1, 100),
            "metadata_format_id": randint(1, 100),
        }
        self.bad_data = {}

    def test_template_to_metadata_format_unmapping_xslt_unauthorized(self):
        """test_template_to_metadata_format_unmapping_xslt_unauthorized"""

        # Act
        response = RequestMock.do_request_delete(
            rest_oai_provider_metadata_format.TemplateMetadataFormatXSLT.as_view(),
            user=create_mock_user("1", is_staff=False),
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_template_to_metadata_format_unmapping_xslt_serializer_invalid(
        self,
    ):
        """test_template_to_metadata_format_unmapping_xslt_serializer_invalid"""

        # Act
        response = RequestMock.do_request_delete(
            rest_oai_provider_metadata_format.TemplateMetadataFormatXSLT.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.bad_data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch.object(OaiXslTemplate, "get_by_template_id_and_metadata_format_id")
    def test_template_to_metadata_format_unmapping_xslt_not_found(
        self, mock_get_by_id
    ):
        """test_template_to_metadata_format_unmapping_xslt_not_found"""

        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.do_request_delete(
            rest_oai_provider_metadata_format.TemplateMetadataFormatXSLT.as_view(),
            user=create_mock_user("1", is_staff=True),
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class TestDeleteMetadataFormat(SimpleTestCase):
    """Test Delete Metadata Format"""

    def setUp(self):
        """setUp"""

        super().setUp()
        self.param = {"metadata_format_id": randint(1, 100)}

    def test_delete_metadata_format_unauthorized(self):
        """test_delete_metadata_format_unauthorized"""

        # Act
        response = RequestMock.do_request_delete(
            rest_oai_provider_metadata_format.MetadataFormatDetail.as_view(),
            user=create_mock_user("1", is_staff=False),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(oai_provider_metadata_format_api, "get_by_id")
    def test_delete_metadata_format_not_found(self, mock_get_by_id):
        """test_delete_metadata_format_not_found"""

        # Arrange
        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error")

        # Act
        response = RequestMock.do_request_delete(
            rest_oai_provider_metadata_format.MetadataFormatDetail.as_view(),
            user=create_mock_user("1", is_staff=True),
            param=self.param,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
