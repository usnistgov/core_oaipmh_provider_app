"""Admin AJAX views
"""

import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.urls import reverse_lazy
from django.utils.html import escape
from requests import ConnectionError
from rest_framework import status

from core_main_app.commons.exceptions import NotUniqueError
from core_main_app.utils.requests_utils.requests_utils import send_get_request
from core_main_app.views.common.ajax import (
    AddObjectModalView,
    EditObjectModalView,
    DeleteObjectModalView,
)
from core_oaipmh_provider_app.components.oai_provider_metadata_format import (
    api as oai_provider_metadata_format_api,
)
from core_oaipmh_provider_app.components.oai_provider_metadata_format.models import (
    OaiProviderMetadataFormat,
)
from core_oaipmh_provider_app.components.oai_provider_set import (
    api as oai_provider_set_api,
)
from core_oaipmh_provider_app.components.oai_provider_set.models import (
    OaiProviderSet,
)
from core_oaipmh_provider_app.components.oai_settings import (
    api as oai_settings_api,
)
from core_oaipmh_provider_app.components.oai_settings.models import OaiSettings
from core_oaipmh_provider_app.components.oai_xsl_template import (
    api as oai_xsl_template_api,
)
from core_oaipmh_provider_app.components.oai_xsl_template.models import (
    OaiXslTemplate,
)
from core_oaipmh_provider_app.utils.template import (
    check_template_manager_in_xsd_format,
)
from core_oaipmh_provider_app.views.admin.forms import (
    EditIdentityForm,
    MetadataFormatForm,
    EditMetadataFormatForm,
    TemplateMetadataFormatForm,
    SetForm,
    MappingXSLTForm,
)


@staff_member_required
def check_registry(request):
    """Check the availability of a registry.
    Args:
        request:

    Returns:

    """
    try:
        http_response = send_get_request(request.GET["url"])
        is_available = http_response.status_code == status.HTTP_200_OK
    except ConnectionError:
        return HttpResponseBadRequest(
            "Connection error while checking availability",
            content_type="application/javascript",
        )
    except Exception as exception:
        return HttpResponseBadRequest(
            escape(str(exception)), content_type="application/javascript"
        )

    return HttpResponse(
        json.dumps({"is_available": is_available}),
        content_type="application/javascript",
    )


class EditIdentityView(EditObjectModalView):
    """Edit Identity View"""

    form_class = EditIdentityForm
    model = OaiSettings
    success_url = reverse_lazy("core-admin:core_oaipmh_provider_app_identity")
    success_message = "Data provider edited."

    def _save(self, form):
        # Save treatment.
        try:
            oai_settings_api.upsert(self.object)
        except Exception as exception:
            form.add_error(None, str(exception))


class AddMetadataFormatView(AddObjectModalView):
    """Add Metadata Format View"""

    template_name = (
        "core_oaipmh_provider_app/admin/registry/forms/add_form.html"
    )
    form_class = MetadataFormatForm
    model = OaiProviderMetadataFormat
    success_url = reverse_lazy(
        "core-admin:core_oaipmh_provider_app_metadata_formats"
    )
    success_message = "Metadata format created."

    def _save(self, form):
        # Save treatment.
        try:
            oai_provider_metadata_format_api.add_metadata_format(
                self.object.metadata_prefix,
                self.object.schema,
                request=self.request,
            )
        except Exception as exception:
            form.add_error(None, str(exception))


class DeleteMetadataFormatView(DeleteObjectModalView):
    """Delete Metadata Format View"""

    model = OaiProviderMetadataFormat
    success_url = reverse_lazy(
        "core-admin:core_oaipmh_provider_app_metadata_formats"
    )
    success_message = "Metadata format deleted."
    field_for_name = "metadata_prefix"

    def _delete(self, form):
        # Delete treatment.
        oai_provider_metadata_format_api.delete(self.object)


class EditMetadataFormatView(EditObjectModalView):
    """Edit Metadata Format View"""

    form_class = EditMetadataFormatForm
    model = OaiProviderMetadataFormat
    success_url = reverse_lazy(
        "core-admin:core_oaipmh_provider_app_metadata_formats"
    )
    success_message = "Metadata format edited."

    def _save(self, form):
        # Save treatment.
        try:
            oai_provider_metadata_format_api.upsert(
                self.object, request=self.request
            )
        except NotUniqueError:
            form.add_error(
                None,
                "A Metadata format with the same prefix already exists. Please "
                "choose another prefix.",
            )
        except Exception as exception:
            form.add_error(None, str(exception))


class AddTemplateMetadataFormatView(AddObjectModalView):
    """Add Template Metadata Format View"""

    template_name = (
        "core_oaipmh_provider_app/admin/registry/forms/add_form.html"
    )
    form_class = TemplateMetadataFormatForm
    model = OaiProviderMetadataFormat
    success_url = reverse_lazy(
        "core-admin:core_oaipmh_provider_app_metadata_formats"
    )
    success_message = "Template Metadata format created."

    def _save(self, form):
        # Save treatment.
        try:
            oai_provider_metadata_format_api.add_template_metadata_format(
                self.object.metadata_prefix,
                self.object.template.id,
                self.request,
            )
        except Exception as exception:
            form.add_error(None, str(exception))

    def get_form_kwargs(self, *args, **kwargs):
        """get_form_kwargs

        Returns:
        """
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs["request"] = self.request
        return kwargs


class AddSetView(AddObjectModalView):
    """Add Set View"""

    template_name = (
        "core_oaipmh_provider_app/admin/registry/forms/add_form.html"
    )
    form_class = SetForm
    model = OaiProviderSet
    success_url = reverse_lazy("core-admin:core_oaipmh_provider_app_sets")
    success_message = "Set created."

    def _save(self, form):
        try:
            template_version_manager_id_list = form.cleaned_data[
                "templates_manager"
            ]
            check_template_manager_in_xsd_format(
                template_version_manager_id_list, self.request
            )

            saved_object = oai_provider_set_api.upsert(self.object)
            saved_object.templates_manager.set(
                template_version_manager_id_list
            )
            oai_provider_set_api.upsert(saved_object)
        except Exception as exception:
            form.add_error(None, str(exception))

    def get_form_kwargs(self, *args, **kwargs):
        """get_form_kwargs

        Returns:
        """
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs["request"] = self.request
        return kwargs


class DeleteSetView(DeleteObjectModalView):
    """Delete Set View"""

    model = OaiProviderSet
    success_url = reverse_lazy("core-admin:core_oaipmh_provider_app_sets")
    success_message = "Set deleted."
    field_for_name = "set_spec"

    def _delete(self, form):
        # Delete treatment.
        oai_provider_metadata_format_api.delete(self.object)


class EditSetView(EditObjectModalView):
    """Edit Set View"""

    form_class = SetForm
    model = OaiProviderSet
    success_url = reverse_lazy("core-admin:core_oaipmh_provider_app_sets")
    success_message = "Set edited."

    def _save(self, form):
        try:
            template_version_manager_id_list = form.cleaned_data[
                "templates_manager"
            ]
            check_template_manager_in_xsd_format(
                template_version_manager_id_list, self.request
            )

            saved_object = oai_provider_set_api.upsert(self.object)
            saved_object.templates_manager.set(
                template_version_manager_id_list
            )
            oai_provider_set_api.upsert(saved_object)
        except Exception as exception:
            form.add_error(None, str(exception))

    def get_initial(self):
        """get_initial

        Returns:
        """
        initial = super().get_initial()
        initial["templates_manager"] = [
            x.id for x in self.object.templates_manager.all()
        ]

        return initial

    def get_form_kwargs(self, *args, **kwargs):
        """get_form_kwargs

        Returns:
        """
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs["request"] = self.request
        return kwargs


class AddTemplateMappingView(AddObjectModalView):
    """Add Template Mapping View"""

    form_class = MappingXSLTForm
    model = OaiXslTemplate
    success_message = "Mapping created."

    def _save(self, form):
        # Save treatment.
        try:
            oai_xsl_template_api.upsert(self.object)
        except Exception as exception:
            form.add_error(None, str(exception))

    def get_initial(self):
        """get_initial

        Returns:
        """
        initial = super().get_initial()
        initial["oai_metadata_format"] = self.kwargs.pop("oai_metadata_format")

        return initial

    def get_form_kwargs(self, *args, **kwargs):
        """get_form_kwargs

        Returns:
        """
        kwargs = super().get_form_kwargs(*args, **kwargs)
        kwargs["request"] = self.request
        return kwargs

    def get_success_url(self):
        """get_success_url

        Returns:
        """
        return reverse_lazy(
            "core-admin:core_oaipmh_provider_app_xslt_template_mapping",
            args=(self.object.oai_metadata_format.id,),
        )


class DeleteTemplateMappingView(DeleteObjectModalView):
    """Delete Template Mapping View"""

    model = OaiXslTemplate
    success_url = reverse_lazy("core-admin:core_oaipmh_provider_app_sets")
    success_message = "Mapping deleted."

    def _delete(self, form):
        # Delete treatment.
        oai_xsl_template_api.delete(self.object)

    def get_success_url(self):
        """get_success_url

        Returns:
        """
        return reverse_lazy(
            "core-admin:core_oaipmh_provider_app_xslt_template_mapping",
            args=(self.object.oai_metadata_format.id,),
        )

    def _get_object_name(self):
        return "the mapping using the template {0} and the xslt {1} ".format(
            self.object.template.display_name, self.object.xslt.name
        )


class EditTemplateMappingView(EditObjectModalView):
    """Edit Template Mapping View"""

    form_class = MappingXSLTForm
    model = OaiXslTemplate
    success_message = "Mapping edited."

    def _save(self, form):
        # Save treatment.
        try:
            oai_xsl_template_api.upsert(self.object)
        except Exception as exception:
            form.add_error(None, str(exception))

    def get_initial(self):
        """get_initial

        Returns:
        """
        initial = super().get_initial()
        initial["xslt"] = self.object.xslt.id
        initial["template"] = self.object.template.id

        return initial

    def get_form_kwargs(self):
        """This method is what injects forms with their keyword
        arguments.

        Returns:
        """
        # grab the current set of form #kwargs
        kwargs = super().get_form_kwargs()
        # Update the kwargs
        kwargs["edit_mode"] = True
        kwargs["request"] = self.request

        return kwargs

    def get_success_url(self):
        """get_success_url

        Returns:
        """
        return reverse_lazy(
            "core-admin:core_oaipmh_provider_app_xslt_template_mapping",
            args=(self.object.oai_metadata_format.id,),
        )
