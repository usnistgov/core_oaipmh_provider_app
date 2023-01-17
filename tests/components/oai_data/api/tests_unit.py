""" Tests unit
"""

from random import randint
from unittest.case import TestCase
from unittest.mock import Mock
from unittest.mock import patch

import core_oaipmh_provider_app.components.oai_data.api as oai_data_api
from core_main_app.commons import exceptions
from core_main_app.commons.exceptions import DoesNotExist
from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_oaipmh_provider_app.commons import status
from core_oaipmh_provider_app.components.oai_data.models import OaiData
from tests.components.oai_data import _create_oai_data, _generic_get_all_test


class TestOaiDataUpsert(TestCase):
    """Test Oai Data Upsert"""

    def setUp(self):
        self.mock_oai_data = _create_oai_data()

    @patch.object(OaiData, "save")
    def test_oai_data_upsert_returns_object(self, mock_save):
        """test_oai_data_upsert_returns_object"""

        # Arrange
        mock_save.return_value = self.mock_oai_data

        # Act
        result = oai_data_api.upsert(self.mock_oai_data)

        # Assert
        self.assertIsInstance(result, OaiData)

    @patch.object(OaiData, "save")
    def test_oai_data_upsert_raises_error_if_save_failed(self, mock_save):
        """test_oai_data_upsert_raises_error_if_save_failed"""

        # Arrange
        mock_save.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(Exception):
            oai_data_api.upsert(self.mock_oai_data)


class TestOaiDataDelete(TestCase):
    """Test Oai Data Delete"""

    @patch.object(OaiData, "delete")
    def test_delete_oai_data_raises_exception_if_error(self, mock_delete):
        """test_delete_oai_data_raises_exception_if_error"""

        # Arrange
        oai_data = _create_oai_data()
        mock_delete.side_effect = Exception()

        # Act # Assert
        with self.assertRaises(Exception):
            oai_data_api.delete(oai_data)


class TestOaiDataGetById(TestCase):
    """Test Oai Data Get By Id"""

    @patch.object(OaiData, "get_by_id")
    def test_get_by_id_returns_object(self, mock_get_by_id):
        """test_get_by_id_returns_object"""

        # Arrange
        mock_oai_data = _create_oai_data()
        mock_oai_data.id = randint(1, 100)

        mock_get_by_id.return_value = mock_oai_data

        # Act
        result = oai_data_api.get_by_id(mock_get_by_id.id)

        # Assert
        self.assertIsInstance(result, OaiData)

    @patch.object(OaiData, "get_by_id")
    def test_get_by_id_raises_exception_if_object_does_not_exist(
        self, mock_get_by_id
    ):
        """test_get_by_id_raises_exception_if_object_does_not_exist"""

        # Arrange
        mock_absent_id = randint(1, 100)

        mock_get_by_id.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            oai_data_api.get_by_id(mock_absent_id)

    @patch.object(OaiData, "get_by_id")
    def test_get_by_id_raises_exception_if_internal_error(
        self, mock_get_by_id
    ):
        """test_get_by_id_raises_exception_if_internal_error"""

        # Arrange
        mock_absent_id = randint(1, 100)

        mock_get_by_id.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            oai_data_api.get_by_id(mock_absent_id)


class TestOaiDataGetByData(TestCase):
    """Test Oai Data Get By Data"""

    @patch.object(OaiData, "get_by_data")
    def test_get_by_data_returns_object(self, mock_get_by_data):
        """test_get_by_data_returns_object"""

        # Arrange
        mock_oai_data = _create_oai_data()
        mock_oai_data.data = Data()

        mock_get_by_data.return_value = mock_oai_data

        # Act
        result = oai_data_api.get_by_data(mock_get_by_data.data)

        # Assert
        self.assertIsInstance(result, OaiData)

    @patch.object(OaiData, "get_by_data")
    def test_get_by_data_raises_exception_if_object_does_not_exist(
        self, mock_get_by_data
    ):
        """test_get_by_data_raises_exception_if_object_does_not_exist"""

        # Arrange
        mock_absent_data = Data()

        mock_get_by_data.side_effect = exceptions.DoesNotExist("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.DoesNotExist):
            oai_data_api.get_by_data(mock_absent_data)

    @patch.object(OaiData, "get_by_data")
    def test_get_by_data_raises_exception_if_internal_error(
        self, mock_get_by_data
    ):
        """test_get_by_data_raises_exception_if_internal_error"""

        # Arrange
        mock_absent_data = Data()

        mock_get_by_data.side_effect = exceptions.ModelError("Error.")

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            oai_data_api.get_by_data(mock_absent_data)


class TestOaiDataGetAll(TestCase):
    """Test Oai Data Get All"""

    @patch.object(OaiData, "get_all")
    def test_get_all_contains_only_oai_data(self, mock_get_all):
        """test_get_all_contains_only_oai_data"""

        _generic_get_all_test(self, mock_get_all, oai_data_api.get_all())


class TestOaiDataGetAllByTemplate(TestCase):
    """Test Oai Data Get All By Template"""

    @patch.object(OaiData, "get_all_by_template_and_timeframe")
    def test_get_all_by_template_contains_only_oai_data(self, mock_get_all):
        """test_get_all_by_template_contains_only_oai_data"""

        _generic_get_all_test(
            self, mock_get_all, oai_data_api.get_all_by_template(Template())
        )


class TestOaiDataGetAllByStatus(TestCase):
    """Test Oai Data Get All By Status"""

    @patch.object(OaiData, "get_all_by_status")
    def test_get_all_by_status_contains_only_oai_data(self, mock_get_all):
        """test_get_all_by_status_contains_only_oai_data"""

        _generic_get_all_test(
            self, mock_get_all, oai_data_api.get_all_by_status(status.ACTIVE)
        )


class TestOaiDataGetEarliestDataDate(TestCase):
    """Test Oai Data Get Earliest Data Date"""

    @patch.object(OaiData, "get_earliest_data_date")
    def test_get_earliest_data_date_raises_exception_if_internal_error(
        self, mock_get_earliest_data_date
    ):
        """test_get_earliest_data_date_raises_exception_if_internal_error"""

        # Arrange
        mock_get_earliest_data_date.side_effect = exceptions.ModelError(
            "Error."
        )

        # Act + Assert
        with self.assertRaises(exceptions.ModelError):
            oai_data_api.get_earliest_data_date()


class TestOaiDataUpsertFromData(TestCase):
    @patch("core_oaipmh_provider_app.components.oai_data.api.get_by_data")
    @patch("core_oaipmh_provider_app.components.oai_data.api.upsert")
    def test_get_by_data_is_called(self, mock_upsert, mock_get_by_data):
        mock_document = "mock_document"
        mock_get_by_data.return_value = None
        mock_upsert.return_value = None
        oai_data_api.upsert_from_data(mock_document)

        self.assertTrue(mock_get_by_data.called_with(mock_document))

    @patch("core_oaipmh_provider_app.components.oai_data.api.get_by_data")
    @patch("core_oaipmh_provider_app.components.oai_data.api.upsert")
    def test_upsert_if_data_exists_and_force_update(
        self, mock_upsert, mock_get_by_data
    ):
        mock_document = "mock_document"
        mock_oai_data = Mock()

        mock_get_by_data.return_value = mock_oai_data
        mock_upsert.return_value = None
        oai_data_api.upsert_from_data(mock_document, force_update=True)

        self.assertTrue(mock_upsert.called_with(mock_oai_data))

    @patch("core_oaipmh_provider_app.components.oai_data.api.get_by_data")
    @patch("core_oaipmh_provider_app.components.oai_data.api.upsert")
    def test_no_upsert_if_data_exists_and_not_force_update(
        self, mock_upsert, mock_get_by_data
    ):
        mock_document = "mock_document"
        mock_oai_data = Mock()

        mock_get_by_data.return_value = mock_oai_data
        mock_upsert.return_value = None
        oai_data_api.upsert_from_data(mock_document, force_update=False)

        self.assertFalse(mock_upsert.called)

    @patch("core_oaipmh_provider_app.components.oai_data.api.get_by_data")
    @patch("core_oaipmh_provider_app.components.oai_data.api.upsert")
    def test_no_upsert_if_no_data_and_no_workspace(
        self, mock_upsert, mock_get_by_data
    ):
        mock_document = Mock()
        mock_document.workspace = None

        mock_get_by_data.side_effect = DoesNotExist(
            "mock_get_by_data_does_not_exist"
        )
        mock_upsert.return_value = None
        oai_data_api.upsert_from_data(mock_document, force_update=False)

        self.assertFalse(mock_upsert.called)

    @patch("core_oaipmh_provider_app.components.oai_data.api.get_by_data")
    @patch("core_oaipmh_provider_app.components.oai_data.api.upsert")
    @patch("core_oaipmh_provider_app.components.oai_data.api.OaiData")
    def test_upsert_if_no_data_and_workspace(
        self, _, mock_upsert, mock_get_by_data
    ):
        mock_document = Mock()
        mock_document.workspace = Mock()
        mock_document.workspace.is_public = True

        mock_get_by_data.side_effect = DoesNotExist(
            "mock_get_by_data_does_not_exist"
        )
        mock_upsert.return_value = None
        oai_data_api.upsert_from_data(mock_document, force_update=False)

        self.assertTrue(mock_upsert.called)
