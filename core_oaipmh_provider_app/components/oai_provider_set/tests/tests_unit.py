from unittest.case import TestCase
from bson.objectid import ObjectId
from mock.mock import Mock, patch
import core_oaipmh_provider_app.components.oai_provider_set.api as provider_set_api
from core_main_app.commons import exceptions
from core_oaipmh_provider_app.components.oai_provider_set.models import OaiProviderSet


class TestOaiProviderSetUpsert(TestCase):
    def setUp(self):
        self.mock_oai_provider_set = _create_oai_provider_set()

    @patch('core_oaipmh_provider_app.components.oai_provider_set.models.OaiProviderSet.save')
    def test_oai_provider_set_upsert_return_object(self, mock_save):
        # Arrange
        mock_save.return_value = self.mock_oai_provider_set

        # Act
        result = provider_set_api.upsert(self.mock_oai_provider_set)

        # Assert
        self.assertIsInstance(result, OaiProviderSet)

    @patch('core_oaipmh_provider_app.components.oai_provider_set.models.OaiProviderSet.save')
    def test_oai_provider_set_upsert_throws_error_if_save_failed(self, mock_save):
        # Arrange
        mock_save.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(exceptions.ApiError):
            provider_set_api.upsert(self.mock_oai_provider_set)


class TestOaiProviderSetGetById(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_set.models.OaiProviderSet.get_by_id')
    def test_get_by_id_return_object(self, mock_get_by_id):
        # Arrange
        mock_oai_provider_set = _create_mock_oai_provider_set()
        mock_oai_provider_set.id = ObjectId()

        mock_get_by_id.return_value = mock_oai_provider_set

        # Act
        result = provider_set_api.get_by_id(mock_get_by_id.id)

        # Assert
        self.assertIsInstance(result, OaiProviderSet)

    @patch('core_oaipmh_provider_app.components.oai_provider_set.models.OaiProviderSet.get_by_id')
    def test_get_by_id_throws_exception_if_object_does_not_exist(self, mock_get_by_id):
        # Arrange
        mock_absent_id = ObjectId()

        mock_get_by_id.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            provider_set_api.get_by_id(mock_absent_id)


class TestOaiProviderSetGetBySetSpec(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_set.models.OaiProviderSet.get_by_set_spec')
    def test_get_by_set_spec_return_object(self, mock_get):
        # Arrange
        mock_oai_provider_set = _create_mock_oai_provider_set()

        mock_get.return_value = mock_oai_provider_set

        # Act
        result = provider_set_api.get_by_set_spec(mock_oai_provider_set.setSpec)

        # Assert
        self.assertIsInstance(result, OaiProviderSet)

    @patch('core_oaipmh_provider_app.components.oai_provider_set.models.OaiProviderSet.get_by_set_spec')
    def test_get_by_set_spec_throws_exception_if_object_does_not_exist(self, mock_get):
        # Arrange
        mock_absent_set_spec = ObjectId()

        mock_get.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(exceptions.ApiError):
            provider_set_api.get_by_set_spec(mock_absent_set_spec)


class TestOaiProviderSetGetAll(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_set.models.OaiProviderSet.get_all')
    def test_list_contains_only_oai_provider_set(self, mock_get_all):
        # Arrange
        mock_oai_provider_set1 = _create_mock_oai_provider_set()
        mock_oai_provider_set2 = _create_mock_oai_provider_set()

        mock_get_all.return_value = [mock_oai_provider_set1, mock_oai_provider_set2]

        # Act
        result = provider_set_api.get_all()

        # Assert
        self.assertTrue(all(isinstance(item, OaiProviderSet) for item in result))


class TestOaiProviderSetGetAllByTemplates(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_set.models.OaiProviderSet.get_all_by_templates')
    def test_get_all_by_templates_return_object(self, mock_get):
        # Arrange
        mock_oai_provider_set1 = _create_mock_oai_provider_set()
        mock_oai_provider_set2 = _create_mock_oai_provider_set()

        mock_get.return_value = [mock_oai_provider_set1, mock_oai_provider_set2]

        # Act
        result = provider_set_api.get_all_by_templates(mock_oai_provider_set1.templates)

        # Assert
        self.assertTrue(all(isinstance(item, OaiProviderSet) for item in result))


class TestOaiProviderSetDelete(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_set.models.OaiProviderSet.delete')
    def test_delete_oai_provider_set_throws_exception_if_object_does_not_exist(self, mock_delete):
        # Arrange
        oai_provider_set = _create_oai_provider_set()
        mock_delete.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(exceptions.ApiError):
            provider_set_api.delete(oai_provider_set)


def _create_oai_provider_set():
    """
    Get an OaiProviderSet object
    :return:
    """
    oai_provider_set = OaiProviderSet()
    _set_oai_provider_set_fields(oai_provider_set)

    return oai_provider_set


def _create_mock_oai_provider_set():
    """
    Mock an OaiProviderSet object
    :return:
    """
    mock_oai_provider_set = Mock(spec=OaiProviderSet)
    _set_oai_provider_set_fields(mock_oai_provider_set)

    return mock_oai_provider_set


def _set_oai_provider_set_fields(oai_provider_set):
    """
    Set OaiProviderSet fields
    :return:
    """
    oai_provider_set.setSpec = "oai_test"
    oai_provider_set.setName = "test"
    oai_provider_set.templates = [ObjectId(), ObjectId()]
    oai_provider_set.description = "OaiSet description"

    return oai_provider_set
