from django.urls import reverse
from menu import Menu, MenuItem

sharing_children = (
    MenuItem(
        "Identity", reverse("admin:core_oaipmh_provider_app_identity"), icon="cog"
    ),
    MenuItem(
        "Metadata Formats",
        reverse("admin:core_oaipmh_provider_app_metadata_formats"),
        icon="book",
    ),
    MenuItem("Sets", reverse("admin:core_oaipmh_provider_app_sets"), icon="bars"),
)

Menu.add_item("admin", MenuItem("OAI-PMH PROVIDER", None, children=sharing_children))
