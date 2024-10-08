""" OAI pmh provider admin form file
"""

import logging

from django import forms
from django.conf import settings

from core_main_app.commons import exceptions
from core_main_app.components.template import api as template_api
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager import (
    api as template_version_manager_api,
)
from core_main_app.components.xsl_transformation import (
    api as xsl_transformation_api,
)
from core_oaipmh_provider_app.components.oai_provider_metadata_format import (
    api as oai_provider_metadata_format_api,
)
from core_oaipmh_provider_app.components.oai_provider_metadata_format.models import (
    OaiProviderMetadataFormat,
)
from core_oaipmh_provider_app.components.oai_provider_set.models import (
    OaiProviderSet,
)
from core_oaipmh_provider_app.components.oai_settings.models import OaiSettings
from core_oaipmh_provider_app.components.oai_xsl_template.models import (
    OaiXslTemplate,
)

logger = logging.getLogger(__name__)


class EditIdentityForm(forms.ModelForm):
    """Edit Identity Form"""

    repository_name = forms.CharField(
        label="Name",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Type the new name"}
        ),
    )

    enable_harvesting = forms.BooleanField(
        label="Enable Harvesting?",
        required=False,
        initial=False,
        widget=forms.CheckboxInput(),
    )

    repository_identifier = forms.CharField(
        label="Repository Identifier",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    class Meta:
        """Meta"""

        model = OaiSettings
        fields = [
            "repository_name",
            "repository_identifier",
            "enable_harvesting",
        ]


class MetadataFormatForm(forms.ModelForm):
    """
    A metadata format form.
    """

    metadata_prefix = forms.CharField(
        label="Metadata Prefix",
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "example: oai_dc", "class": "form-control"}
        ),
    )
    schema = forms.URLField(
        label="Schema URL",
        required=True,
        widget=forms.URLInput(attrs={"class": "form-control"}),
        help_text="The provided link must point to an XSD schema.",
    )

    class Meta:
        """Meta"""

        model = OaiProviderMetadataFormat
        fields = ["metadata_prefix", "schema"]


class EditMetadataFormatForm(forms.ModelForm):
    """
    A metadata format edit form.
    """

    metadata_prefix = forms.CharField(
        label="Metadata Prefix",
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Type the new name"}
        ),
    )

    class Meta:
        """Meta"""

        model = OaiProviderMetadataFormat
        fields = ["metadata_prefix"]


class TemplateMetadataFormatForm(forms.ModelForm):
    """
    A template metadata format form.
    """

    metadata_prefix = forms.CharField(
        label="Metadata Prefix",
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "example: oai_dc", "class": "form-control"}
        ),
    )
    template = forms.ChoiceField(
        label="Template",
        widget=forms.Select(),
        help_text="Only XSD templates can be added as metadata formats.",
    )

    class Meta:
        """Meta"""

        model = OaiProviderMetadataFormat
        fields = ["metadata_prefix", "template"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields["template"].choices = _get_templates_versions(
            request=self.request
        )
        if settings.BOOTSTRAP_VERSION.startswith("4"):
            self.fields["template"].widget.attrs["class"] = "form-control"
        elif settings.BOOTSTRAP_VERSION.startswith("5"):
            self.fields["template"].widget.attrs["class"] = "form-select"

    def clean_template(self):
        data = self.cleaned_data["template"]
        return template_api.get_by_id(data, request=self.request)


class SetForm(forms.ModelForm):
    """
    A Set edit form.
    """

    set_spec = forms.CharField(
        label="Set spec",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    set_name = forms.CharField(
        label="Set name",
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    templates_manager = forms.MultipleChoiceField(
        label="Templates",
        widget=forms.CheckboxSelectMultiple(attrs={"class": "double-columns"}),
        required=True,
        help_text="Only XSD templates can be added as metadata formats.",
    )
    description = forms.CharField(
        label="Description",
        required=True,
        widget=forms.Textarea(
            attrs={
                "cols": "60",
                "rows": "5",
                "class": "form-control",
                "style": "height:14em;width:100%;",
            }
        ),
    )

    class Meta:
        """Meta"""

        model = OaiProviderSet
        fields = [
            "set_spec",
            "set_name",
            "templates_manager",
            "description",
        ]

    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields["templates_manager"].choices = _get_templates_manager(
            request=request
        )


class MappingXSLTForm(forms.ModelForm):
    """
    A MappingXSLTForm form.
    """

    oai_metadata_format = forms.ModelChoiceField(
        widget=forms.HiddenInput(),
        queryset=oai_provider_metadata_format_api.get_all(),
        label="Metadata Prefix",
        required=True,
    )
    template = forms.ChoiceField(label="Template", widget=forms.Select())
    xslt = forms.ChoiceField(label="XSLT", widget=forms.Select())

    class Meta:
        """Meta"""

        model = OaiXslTemplate
        fields = ["oai_metadata_format", "template", "xslt"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        edit_mode = kwargs.pop("edit_mode", None)
        super().__init__(*args, **kwargs)
        self.fields["template"].choices = _get_templates_versions(
            request=self.request
        )
        self.fields["xslt"].choices = _get_xsl_transformation()
        if edit_mode:
            self.fields["template"].widget = forms.HiddenInput()

        if settings.BOOTSTRAP_VERSION.startswith("4"):
            self.fields["xslt"].widget.attrs["class"] = "form-control"
            self.fields["template"].widget.attrs["class"] = "form-control"
        elif settings.BOOTSTRAP_VERSION.startswith("5"):
            self.fields["xslt"].widget.attrs["class"] = "form-select"
            self.fields["template"].widget.attrs["class"] = "form-select"

    def clean_xslt(self):
        data = self.cleaned_data["xslt"]
        return xsl_transformation_api.get_by_id(data)

    def clean_template(self):
        data = self.cleaned_data["template"]
        return template_api.get_by_id(data, request=self.request)


def _get_templates_versions(request):
    """Get templates versions.

    Returns:
        List of templates versions.

    """
    templates = []
    try:
        # Retrieve all template version manager in the allowed format (currently XSD).
        template_version_manager_list = (
            template_version_manager_api.get_active_global_version_manager(
                request=request
            ).filter(template__format=Template.XSD)
        )

        for template_version_manager in template_version_manager_list:
            for template_version in template_version_manager.versions:
                template = template_api.get_by_id(
                    template_version, request=request
                )
                version_name = template.display_name
                templates.append((template_version, version_name))
    except exceptions.DoesNotExist as exception:
        logger.warning(
            "_get_templates_versions threw an exception: %s", str(exception)
        )

    return templates


def _get_templates_manager(request):
    """Get templates manager.

    Args:
        request:

    Returns:
        List of templates manager.

    """
    return [
        (template_version_manager.id, template_version_manager.title)
        for template_version_manager in template_version_manager_api.get_active_global_version_manager(
            request=request
        ).filter(
            template__format=Template.XSD
        )
    ]


def _get_xsl_transformation():
    """Get XSLT.

    Returns:
        List of XSLT.

    """
    xsl_transformation = []
    list_ = xsl_transformation_api.get_all()
    for elt in list_:
        xsl_transformation.append((elt.id, elt.name))
    return xsl_transformation
