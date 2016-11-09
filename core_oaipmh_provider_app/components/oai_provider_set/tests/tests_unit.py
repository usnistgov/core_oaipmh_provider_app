from unittest.case import TestCase
from bson.objectid import ObjectId
from mock.mock import Mock, patch
import core_oaipmh_provider_app.components.oai_provider_set.api as provider_set_api
from core_main_app.commons import exceptions
from core_oaipmh_provider_app.components.oai_provider_set.models import OaiProviderSet


class TestOaiProviderSetSave(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_set.models.OaiProviderSet.create_oai_provider_set')
    def test_save_oai_provider_set(self, mock_create):
        # Arrange
        mock_oai_provider_set = _get_oai_provider_set_mock()

        mock_create.return_value = mock_oai_provider_set

        # Act
        result = provider_set_api.save(mock_oai_provider_set.setSpec, mock_oai_provider_set.setName,
                                       mock_oai_provider_set.templates, mock_oai_provider_set.description)

        # Assert
        self.assertIsInstance(result, OaiProviderSet)


class TestOaiProviderSetGetById(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_set.models.OaiProviderSet.get_by_id')
    def test_get_by_id_return_object(self, mock_get_by_id):
        # Arrange
        mock_oai_provider_set = _get_oai_provider_set_mock()

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
        with self.assertRaises(exceptions.MDCSError):
            provider_set_api.get_by_id(mock_absent_id)


class TestOaiProviderSetGetBySetSpec(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_set.models.OaiProviderSet.get_by_set_spec')
    def test_get_by_set_spec_return_object(self, mock_get):
        # Arrange
        mock_oai_provider_set = _get_oai_provider_set_mock()

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
        with self.assertRaises(exceptions.MDCSError):
            provider_set_api.get_by_set_spec(mock_absent_set_spec)


class TestOaiProviderSetGetAll(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_set.models.OaiProviderSet.get_all')
    def test_list_contains_only_oai_provider_set(self, mock_get_all):
        # Arrange
        mock_oai_provider_set1 = _get_oai_provider_set_mock()
        mock_oai_provider_set2 = _get_oai_provider_set_mock()

        mock_get_all.return_value = [mock_oai_provider_set1, mock_oai_provider_set2]

        # Act
        result = provider_set_api.get_all()

        # Assert
        self.assertTrue(all(isinstance(item, OaiProviderSet) for item in result))


class TestOaiProviderSetGetAllByTemplates(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_set.models.OaiProviderSet.get_all_by_templates')
    def test_get_all_by_templates_return_object(self, mock_get):
        # Arrange
        mock_oai_provider_set1 = _get_oai_provider_set_mock()
        mock_oai_provider_set2 = _get_oai_provider_set_mock()

        mock_get.return_value = [mock_oai_provider_set1, mock_oai_provider_set2]

        # Act
        result = provider_set_api.get_all_by_templates(mock_oai_provider_set1.templates)

        # Assert
        self.assertTrue(all(isinstance(item, OaiProviderSet) for item in result))

    @patch('core_oaipmh_provider_app.components.oai_provider_set.models.OaiProviderSet.get_all_by_templates')
    def test_get_all_by_templates_throws_exception_if_object_does_not_exist(self, mock_get):
        # Arrange
        mock_absent_templates = [ObjectId()]

        mock_get.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(exceptions.MDCSError):
            provider_set_api.get_all_by_templates(mock_absent_templates)


class TestOaiProviderSetUpdateById(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_set.models.OaiProviderSet.get_by_id')
    def test_update_by_id_return_object(self, mock_get_by_id):
        # Arrange
        mock_oai_provider_set = _get_oai_provider_set_mock()

        mock_get_by_id.return_value = mock_oai_provider_set

        # Act
        result = provider_set_api.update_by_id(mock_oai_provider_set.id, mock_oai_provider_set.setSpec,
                                               mock_oai_provider_set.setName, mock_oai_provider_set.templates,
                                               mock_oai_provider_set.description)

        # Assert
        self.assertIsInstance(result, OaiProviderSet)

    @patch('core_oaipmh_provider_app.components.oai_provider_set.models.OaiProviderSet.get_by_id')
    def test_update_by_id_throws_exception_if_object_does_not_exist(self, mock_get_by_id):
        # Arrange
        mock_oai_provider_set = _get_oai_provider_set_mock()

        mock_get_by_id.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(exceptions.MDCSError):
            provider_set_api.update_by_id(mock_oai_provider_set.id, mock_oai_provider_set.setSpec,
                                          mock_oai_provider_set.setName, mock_oai_provider_set.templates,
                                          mock_oai_provider_set.description)


class TestOaiProviderSetDeleteById(TestCase):
    @patch('core_oaipmh_provider_app.components.oai_provider_set.models.OaiProviderSet.delete_by_id')
    def test_delete_all_by_id_throws_exception_if_object_does_not_exist(self, mock_delete_by_id):
        # Arrange
        mock_absent_provider_set = str(ObjectId())

        mock_delete_by_id.side_effect = Exception()

        # Act + Assert
        with self.assertRaises(exceptions.MDCSError):
            provider_set_api.delete_by_id(mock_absent_provider_set)


def _get_oai_provider_set_mock():
    """
    Mock an OaiProviderSet object
    :return:
    """
    mock_oai_provider_set = Mock(spec=OaiProviderSet)
    mock_oai_provider_set.setSpec = "oai_test"
    mock_oai_provider_set.setName = "test"
    mock_oai_provider_set.id = ObjectId()
    mock_oai_provider_set.templates = [ObjectId(), ObjectId()]
    mock_oai_provider_set.description = "OaiSet description"

    return mock_oai_provider_set
