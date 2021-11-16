"""
OaiProviderSet API
"""

from core_main_app.components.template_version_manager import (
    api as template_version_manager_api,
)
from core_main_app.components.template import (
    api as template_api,
)
from core_oaipmh_provider_app.components.oai_provider_set.models import OaiProviderSet


def upsert(oai_provider_set):
    """Create or update an OaiProviderSet.

    Args:
        oai_provider_set:

    Returns:
        The OaiProviderSet instance.

    """
    oai_provider_set.save()
    return oai_provider_set


def delete(oai_provider_set):
    """Delete an OaiProviderSet.

    Args:
        oai_provider_set: The OaiProviderSet to delete.

    """
    oai_provider_set.delete()


def get_by_id(oai_provider_set_id):
    """Get an OaiProviderSet by its id.

    Args:
        oai_provider_set_id: The OaiProviderSet id.

    Returns:
        The OaiProviderSet instance.

    """
    return OaiProviderSet.get_by_id(oai_set_id=oai_provider_set_id)


def get_by_set_spec(set_spec):
    """Get an OaiProviderSet by its set_spec.

    Args:
        set_spec: The OaiProviderSet set_spec.

    Returns:
        The OaiProviderSet instance.
    """
    return OaiProviderSet.get_by_set_spec(set_spec=set_spec)


def get_all(order_by_field=None):
    """Get all OaiProviderSet.
    Args:
        order_by_field: Order by field.

    Returns:
        List of OaiProviderSet.
    """
    return OaiProviderSet.get_all(order_by_field)


def get_all_by_templates_manager(templates_manager):
    """Get all OaiProviderSet used by a list of templates manager.

    Args:
        templates_manager: List of templates manager.

    Returns:
        List of OaiProviderSet.

    """
    return OaiProviderSet.get_all_by_templates_manager(
        templates_manager=templates_manager
    )


def get_all_by_template_ids(template_id_list, request):
    """Get all OaiProviderSet used by a list of templates ids.

    Args:
        template_id_list: List of templates ids:
        request:

    Returns:
        List of OaiProviderSet.

    """
    # Get all templates managers with the selected templates ids.
    templates_manager = set(
        [
            template_api.get_by_id(template_id, request).version_manager
            for template_id in template_id_list
        ]
    )
    # Get all OaiProviderSet used by those templates manager
    return get_all_by_templates_manager(templates_manager)
