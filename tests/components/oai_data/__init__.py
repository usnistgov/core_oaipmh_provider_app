""" Test utils for OaiData
"""
from unittest.mock import Mock

from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.utils.datetime import datetime_now
from core_oaipmh_provider_app.commons import status
from core_oaipmh_provider_app.components.oai_data.models import OaiData


def _generic_get_all_test(self, mock_get_all, act_function):
    """generic_get_all_test.

    Args:
        mock_get_all:
        act_function:

    Returns:

    """
    # Arrange
    mock_oai_data1 = _create_mock_oai_data()
    mock_oai_data2 = _create_mock_oai_data()

    mock_get_all.return_value = [mock_oai_data1, mock_oai_data2]

    # Act
    result = act_function

    # Assert
    self.assertTrue(all(isinstance(item, OaiData) for item in result))


def _create_oai_data():
    """Get an OaiData object.

    Returns:
        OaiData instance.

    """
    oai_data = OaiData()
    oai_data = _set_oai_data_fields(oai_data)

    return oai_data


def _create_mock_oai_data():
    """Mock an OaiData.

    Returns:
        OaiData mock.

    """
    mock_oai_data = Mock(spec=OaiData)
    mock_oai_data = _set_oai_data_fields(mock_oai_data)

    return mock_oai_data


def _set_oai_data_fields(oai_data):
    """Set OaiData fields.

    Returns:
        OaiData with assigned fields.

    """
    oai_data.status = status.ACTIVE
    oai_data.data = Data()
    oai_data.template = Template()
    oai_data.oai_date_stamp = datetime_now()

    return oai_data
