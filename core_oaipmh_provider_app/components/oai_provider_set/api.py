"""
OaiProviderSet API
"""

from core_oaipmh_provider_app.components.oai_provider_set.models import OaiProviderSet
from core_main_app.commons import exceptions


def upsert(oai_provider_set):
    """
    Create or update an OaiProviderSet
    :param oai_provider_set:
    :return:
    """
    try:
        return oai_provider_set.save()
    except:
        raise exceptions.ApiError('Save OaiProviderSet failed.')


def delete(oai_provider_set):
    """
    Delete an OaiProviderSet
    :param oai_provider_set:
    :return:
    """
    try:
        oai_provider_set.delete()
    except:
        raise exceptions.ApiError('Impossible to delete OaiProviderSet.')


def get_by_id(oai_provider_set_id):
    """
    Get an OaiProviderSet by its id
    :param oai_provider_set_id:
    :return:
    """
    try:
        return OaiProviderSet.get_by_id(oai_set_id=oai_provider_set_id)
    except:
        raise exceptions.ApiError('No OaiProviderSet could be found with the given id.')


def get_by_set_spec(set_spec):
    """
    Get an OaiProviderSet by its setSpec
    :param set_spec:
    :return:
    """
    try:
        return OaiProviderSet.get_by_set_spec(set_spec=set_spec)
    except:
        raise exceptions.ApiError('No OaiProviderSet could be found with the given setSpec.')


def get_all():
    """
    Get all OaiProviderSet
    :return:
    """
    return OaiProviderSet.get_all()


def get_all_by_templates(templates):
    """
    Get all OaiProviderSet used by a list of templates
    :param templates:
    :return:
    """
    return OaiProviderSet.get_all_by_templates(templates=templates)
