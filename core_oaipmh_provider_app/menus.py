from django.core.urlresolvers import reverse
from menu import Menu, MenuItem

sharing_children = (
    MenuItem("Identity", reverse("admin:core_oaipmh_provider_app_identity"), icon="gear"),
)

Menu.add_item(
    "admin", MenuItem("OAI-PMH PROVIDER", None, children=sharing_children)
)
