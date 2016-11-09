"""
OaiProviderSet API
"""

from core_oaipmh_provider_app.components.oai_provider_set.models import OaiProviderSet
from core_main_app.commons import exceptions


def save(set_spec, set_name, templates, description):
    """
    Create an OaiProviderSet
    :param set_spec:
    :param set_name:
    :param templates:
    :param description:
    :return:
    """
    new_oai_provider_set = OaiProviderSet.create_oai_provider_set(set_spec=set_spec,
                                                                  set_name=set_name,
                                                                  templates=templates,
                                                                  description=description)
    return new_oai_provider_set


def get_by_id(oai_provider_set_id):
    """
    Get an OaiProviderSet by its id
    :param oai_provider_set_id:
    :return:
    """
    try:
        return OaiProviderSet.get_by_id(oai_set_id=oai_provider_set_id)
    except:
        raise exceptions.MDCSError('No OaiProviderSet could be found with the given id')


def get_by_set_spec(set_spec):
    """
    Get an OaiProviderSet by its setSpec
    :param set_spec:
    :return:
    """
    try:
        return OaiProviderSet.get_by_set_spec(set_spec=set_spec)
    except:
        raise exceptions.MDCSError('No OaiProviderSet could be found with the given setSpec')


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
    try:
        return OaiProviderSet.get_all_by_templates(templates=templates)
    except:
        raise exceptions.MDCSError('No OaiProviderSet could be found with the given list of templates')


def update_by_id(oai_provider_set_id, set_spec, set_name, templates, description):
    """
    Update an OaiProviderSet by its id
    :param oai_provider_set_id:
    :param set_spec:
    :param set_name:
    :param templates:
    :param description:
    :return:
    """
    try:
        oai_provider_set = get_by_id(oai_provider_set_id)
        oai_provider_set.setSpec = set_spec
        oai_provider_set.setName = set_name
        oai_provider_set.templates = templates
        oai_provider_set.description = description

        oai_provider_set.update_object()
    except:
        raise exceptions.MDCSError('No OaiProviderSet could be found with the given id.')

    return oai_provider_set


def delete_by_id(oai_provider_set_id):
    """
    Delete an OaiProviderSet by its id
    :param oai_provider_set_id:
    :return:
    """
    try:
        OaiProviderSet.delete_by_id(oai_provider_set_id)
    except:
        raise exceptions.MDCSError('No OaiProviderSet could be found with the given registry.')
