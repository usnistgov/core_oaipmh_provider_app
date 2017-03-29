from django.contrib.admin.views.decorators import staff_member_required
from core_main_app.utils.rendering import admin_render
from core_oaipmh_provider_app.components.oai_settings import api as oai_settings_api
from core_oaipmh_provider_app.components.oai_provider_metadata_format import api as oai_metadata_format_api
from core_oaipmh_provider_app.components.oai_provider_set import api as oai_provider_set_api
from core_main_app.components.version_manager import api as version_manager_api
from core_oaipmh_provider_app.views.admin.forms import SetForm
from core_oaipmh_provider_app import settings
from django.core.urlresolvers import reverse


@staff_member_required
def identity_view(request):
    assets = {
        "js": [
            {
                "path": "core_oaipmh_provider_app/admin/js/registry/identity/check_registry.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_provider_app/admin/js/registry/identity/modals/edit_identity.js",
                "is_raw": False
            }
        ],
        "css": [
            "core_oaipmh_provider_app/admin/css/registry/identity/table_info.css"
        ]
    }

    modals = [
        "core_oaipmh_provider_app/admin/registry/identity/modals/edit_identity.html"
    ]

    info = oai_settings_api.get()
    data_provider = {
        'name': info.repository_name,
        'baseURL': request.build_absolute_uri(reverse("core_oaipmh_provider_app_server_index")),
        'protocol_version': settings.OAI_PROTOCOL_VERSION,
        'admins': (email for name, email in settings.OAI_ADMINS),
        'deleted': settings.OAI_DELETED_RECORD,
        'granularity': settings.OAI_GRANULARITY,
        'identifier_scheme': settings.OAI_SCHEME,
        'repository_identifier': info.repository_identifier,
        'identifier_delimiter': settings.OAI_DELIMITER,
        'sample_identifier': settings.OAI_SAMPLE_IDENTIFIER,
        'enable_harvesting': info.enable_harvesting,
    }

    context = {
        "data_provider": data_provider
    }

    return admin_render(request, "core_oaipmh_provider_app/admin/registry/identity.html", assets=assets,
                        context=context, modals=modals)


@staff_member_required
def metadata_formats_view(request):
    assets = {
        "js": [
            {
                "path": "core_oaipmh_provider_app/admin/js/registry/metadata_formats/modals/add_metadata_format.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_provider_app/admin/js/registry/metadata_formats/modals/delete_metadata_format.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_provider_app/admin/js/registry/metadata_formats/modals/edit_metadata_format.js",
                "is_raw": False
            }
        ],
        "css": [
            "core_oaipmh_provider_app/admin/css/registry/metadata_formats/page.css"
        ]
    }

    modals = [
        "core_oaipmh_provider_app/admin/registry/metadata_formats/modals/add_metadata_format.html",
        "core_oaipmh_provider_app/admin/registry/metadata_formats/modals/delete_metadata_format.html",
        "core_oaipmh_provider_app/admin/registry/metadata_formats/modals/edit_metadata_format.html"
    ]

    order_field = 'metadata_prefix'
    default_metadata_formats = oai_metadata_format_api.get_all_default_metadata_format(order_by_field=order_field)
    metadata_formats = oai_metadata_format_api.get_all_custom_metadata_format(order_by_field=order_field)
    template_metadata_formats = _get_template_metadata_format(request, order_field=order_field)

    context = {
        'default_metadata_formats': default_metadata_formats,
        'metadata_formats': metadata_formats,
        'template_metadata_formats': template_metadata_formats
    }

    return admin_render(request, "core_oaipmh_provider_app/admin/registry/metadata_formats.html", assets=assets,
                        context=context, modals=modals)


@staff_member_required
def sets_view(request):
    assets = {
        "js": [
            {
                "path": "core_oaipmh_provider_app/admin/js/registry/sets/modals/init_select.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_provider_app/admin/libs/fSelect/js/fSelect.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_provider_app/admin/js/registry/sets/modals/add_set.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_provider_app/admin/js/registry/sets/modals/delete_set.js",
                "is_raw": False
            },
            {
                "path": "core_oaipmh_provider_app/admin/js/registry/sets/modals/edit_set.js",
                "is_raw": False
            }
        ],
        "css": [
            "core_oaipmh_provider_app/admin/libs/fSelect/css/fSelect.css",
            "core_oaipmh_provider_app/admin/css/registry/sets/add_set.css"
        ]
    }

    modals = [
        "core_oaipmh_provider_app/admin/registry/sets/modals/add_set.html",
        "core_oaipmh_provider_app/admin/registry/sets/modals/delete_set.html",
        "core_oaipmh_provider_app/admin/registry/sets/modals/edit_set.html"
    ]

    context = {
        'sets': oai_provider_set_api.get_all(order_by_field='set_spec'),
        'add_set_form': SetForm()
    }

    return admin_render(request, "core_oaipmh_provider_app/admin/registry/sets.html", assets=assets,
                        context=context, modals=modals)


def _get_template_metadata_format(request, order_field=None):
    """ Get template metadata format information.
    Args:
        order_field: Possibility to order by field.

    Returns:
        Template metadata format information.

    """
    items_template_metadata_format = []
    template_metadata_formats = oai_metadata_format_api.get_all_template_metadata_format(order_by_field=order_field)
    for template_item in template_metadata_formats:
        version_manager = version_manager_api.get_from_version(template_item.template)
        host_uri = request.build_absolute_uri('/')
        item_info = {
            'id': template_item.id,
            'metadata_prefix': template_item.metadata_prefix,
            'schema': oai_metadata_format_api.get_metadata_format_schema_url(template_item, host_uri),
            'title': version_manager.title,
            'metadata_namespace': template_item.metadata_namespace,
            'version': version_manager_api.get_version_number(version_manager, template_item.template.id)
        }
        items_template_metadata_format.append(item_info)

    return items_template_metadata_format
