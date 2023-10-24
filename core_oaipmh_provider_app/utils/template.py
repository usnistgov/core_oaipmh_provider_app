""" Utilities for managing templates.
"""
from core_main_app.commons.exceptions import CoreError
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager import (
    api as template_version_manager_api,
)


def check_template_manager_in_xsd_format(template_managers_id_list, request):
    """Check that all template manager from a given list of ID are in XSD format.

    Args:
        template_managers_id_list:
        request:

    Returns:
    """
    template_version_manager_list = (
        template_version_manager_api.get_by_id_list(
            template_managers_id_list, request
        )
    )

    if (
        template_version_manager_list.filter(
            template__format=Template.XSD
        ).count()
        != template_version_manager_list.count()
    ):
        raise CoreError("Not all templates are in XSD format.")
