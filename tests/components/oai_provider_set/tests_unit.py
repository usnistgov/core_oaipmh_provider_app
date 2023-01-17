""" Tests unit
"""

from random import randint
from unittest.case import TestCase
from unittest.mock import Mock, patch

import core_main_app.components.template.api as template_api
import core_oaipmh_provider_app.components.oai_provider_set.api as provider_set_api
from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import create_mock_request
from core_oaipmh_provider_app.components.oai_provider_set.models import (
    OaiProviderSet,
)


class TestOaiProviderSetUpsert(TestCase):
    """Test Oai Provider Set Upsert"""

    def setUp(self):
        """setUp"""
        self.mock_oai_provider_set = _create_oai_provider_set()

    @patch.object(OaiProviderSet, "save")
    def test_oai_provider_set_upsert_return_object(self, mock_save):
        """test_oai_provider_set_upsert_return_object"""

        # Arrange
        mock_save.return_value = self.mock_oai_provider_set

        # Act
        result = provider_set_api.upsert(self.mock_oai_provider_set)

        # Assert
        self.assertIsInstance(result, OaiProviderSet)

    @patch.object(OaiProviderSet, "save")
    def test_oai_provider_set_upsert_raises_error_if_save_failed(
        self, mock_save
    ):
        """test_oai_provider_set_upsert_raises_error_if_save_failed"""

        # Arrange
        mock_save.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(Exception):
            provider_set_api.upsert(self.mock_oai_provider_set)


class TestOaiProviderSetGetById(TestCase):
    """Test Oai Provider Set Get By Id"""

    @patch.object(OaiProviderSet, "get_by_id")
    def test_get_by_id_return_object(self, mock_get_by_id):
        """test_get_by_id_return_object"""

        # Arrange
        mock_oai_provider_set = _create_mock_oai_provider_set()
        mock_oai_provider_set.id = randint(1, 100)

        mock_get_by_id.return_value = mock_oai_provider_set

        # Act
        result = provider_set_api.get_by_id(mock_get_by_id.id)

        # Assert
        self.assertIsInstance(result, OaiProviderSet)

    @patch.object(OaiProviderSet, "get_by_id")
    def test_get_by_id_raises_exception_if_object_does_not_exist(
        self, mock_get_by_id
    ):
        """test_get_by_id_raises_exception_if_object_does_not_exist"""

        # Arrange
        mock_absent_id = randint(1, 100)

        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            provider_set_api.get_by_id(mock_absent_id)

    @patch.object(OaiProviderSet, "get_by_id")
    def test_get_by_id_raises_exception_if_internal_error(
        self, mock_get_by_id
    ):
        """test_get_by_id_raises_exception_if_internal_error"""

        # Arrange
        mock_absent_id = randint(1, 100)

        mock_get_by_id.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            provider_set_api.get_by_id(mock_absent_id)


class TestOaiProviderSetGetBySetSpec(TestCase):
    """Test Oai Provider Set Get By Set Spec"""

    @patch.object(OaiProviderSet, "get_by_set_spec")
    def test_get_by_set_spec_return_object(self, mock_get):
        """test_get_by_set_spec_return_object"""

        # Arrange
        mock_oai_provider_set = _create_mock_oai_provider_set()

        mock_get.return_value = mock_oai_provider_set

        # Act
        result = provider_set_api.get_by_set_spec(
            mock_oai_provider_set.set_spec
        )

        # Assert
        self.assertIsInstance(result, OaiProviderSet)

    @patch.object(OaiProviderSet, "get_by_set_spec")
    def test_get_by_set_spec_raises_exception_if_object_does_not_exist(
        self, mock_get
    ):
        """test_get_by_set_spec_raises_exception_if_object_does_not_exist"""

        # Arrange
        mock_absent_set_spec = randint(1, 100)

        mock_get.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            provider_set_api.get_by_set_spec(mock_absent_set_spec)

    @patch.object(OaiProviderSet, "get_by_set_spec")
    def test_get_by_set_spec_raises_exception_if_internal_error(
        self, mock_get
    ):
        """test_get_by_set_spec_raises_exception_if_internal_error"""

        # Arrange
        mock_absent_set_spec = randint(1, 100)

        mock_get.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            provider_set_api.get_by_set_spec(mock_absent_set_spec)


class TestOaiProviderSetGetAll(TestCase):
    """Test Oai Provider Set Get All"""

    @patch.object(OaiProviderSet, "get_all")
    def test_list_contains_only_oai_provider_set(self, mock_get_all):
        """test_list_contains_only_oai_provider_set"""

        # Arrange
        mock_oai_provider_set1 = _create_mock_oai_provider_set()
        mock_oai_provider_set2 = _create_mock_oai_provider_set()

        mock_get_all.return_value = [
            mock_oai_provider_set1,
            mock_oai_provider_set2,
        ]

        # Act
        result = provider_set_api.get_all()

        # Assert
        self.assertTrue(
            all(isinstance(item, OaiProviderSet) for item in result)
        )


class TestOaiProviderSetGetAllByTemplatesManager(TestCase):
    """Test Oai Provider Set Get All By Templates Manager"""

    @patch.object(OaiProviderSet, "get_all_by_templates_manager")
    def test_get_all_by_templates_manager_return_object(self, mock_get):
        """test_get_all_by_templates_manager_return_object"""

        # Arrange
        mock_oai_provider_set1 = _create_mock_oai_provider_set()
        mock_oai_provider_set2 = _create_mock_oai_provider_set()

        mock_get.return_value = [
            mock_oai_provider_set1,
            mock_oai_provider_set2,
        ]

        # Act
        result = provider_set_api.get_all_by_templates_manager(
            mock_oai_provider_set1.templates_manager
        )

        # Assert
        self.assertTrue(
            all(isinstance(item, OaiProviderSet) for item in result)
        )


class TestOaiProviderSetGetAllByTemplates(TestCase):
    """Test Oai Provider Set Get All By Templates"""

    @patch.object(OaiProviderSet, "get_all_by_templates_manager")
    @patch.object(template_api, "get_by_id")
    def test_get_all_by_templates_return_object(
        self,
        mock_template_api_get_by_id,
        mock_oai_provider_set_get_all_by_templates_manager,
    ):
        """test_get_all_by_templates_return_object"""

        # Arrange
        mock_user = create_mock_user("1", is_superuser=True)
        mock_request = create_mock_request(user=mock_user)
        template_id = randint(1, 100)
        mock_oai_provider_set1 = _create_mock_oai_provider_set()
        mock_oai_provider_set2 = _create_mock_oai_provider_set()

        mock_oai_provider_set_get_all_by_templates_manager.return_value = [
            mock_oai_provider_set1,
            mock_oai_provider_set2,
        ]
        mock_template_api_get_by_id.return_value = _create_mock_template()

        # Act
        result = provider_set_api.get_all_by_template_ids(
            [template_id], mock_request
        )

        # Assert
        self.assertTrue(
            all(isinstance(item, OaiProviderSet) for item in result)
        )


class TestOaiProviderSetDelete(TestCase):
    """Test Oai Provider Set Delete"""

    @patch.object(OaiProviderSet, "delete")
    def test_delete_oai_provider_set_raises_exception_if_object_does_not_exist(
        self, mock_delete
    ):
        """test_delete_oai_provider_set_raises_exception_if_object_does_not_exist"""

        # Arrange
        oai_provider_set = _create_oai_provider_set()
        mock_delete.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(Exception):
            provider_set_api.delete(oai_provider_set)


def _create_mock_template():
    mock_template = Mock(spec=Template)
    mock_template.version_manager = 1

    return mock_template


def _create_template_version_manager():
    template_version_manager = TemplateVersionManager(
        title=f"template{randint(1, 100) * randint(1, 100)}", user=1
    )
    template_version_manager.save()

    return template_version_manager


def _create_oai_provider_set():
    """Get an OaiProviderSet object

    Returns:
        OaiProviderSet instance.

    """
    oai_provider_set = OaiProviderSet()
    _set_oai_provider_set_fields(oai_provider_set)

    return oai_provider_set


def _create_mock_oai_provider_set():
    """Mock an OaiProviderSet.

    Returns:
        OaiProviderSet mock.

    """
    mock_oai_provider_set = Mock(spec=OaiProviderSet)
    _set_oai_provider_set_fields(mock_oai_provider_set)

    return mock_oai_provider_set


def _set_oai_provider_set_fields(oai_provider_set):
    """Set OaiProviderSet fields.

    Args:
        oai_provider_set:

    Returns:
        OaiProviderSet with assigned fields.

    """
    oai_provider_set.set_spec = "oai_test"
    oai_provider_set.set_name = "test"
    oai_provider_set.description = "OaiSet description"

    return oai_provider_set
