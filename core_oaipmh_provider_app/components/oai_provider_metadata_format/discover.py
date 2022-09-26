""" discover settings for oai-pmh
"""
import logging
from os.path import join

from django.contrib.staticfiles import finders

from core_oaipmh_provider_app.system import api as system_api
from core_oaipmh_provider_app.components.oai_provider_metadata_format import (
    api as oai_provider_metadata_format_api,
)
from core_oaipmh_provider_app.components.oai_provider_metadata_format.models import (
    OaiProviderMetadataFormat,
)

logger = logging.getLogger(__name__)


def init():
    """Init default metadata formats for OAI-PMH"""

    logger.info("START oai provider metadata format discovery.")

    try:
        metadata_formats = oai_provider_metadata_format_api.get_all()
        if len(metadata_formats) == 0:
            # Add dublin core metadata prefix
            schema_url = "http://www.openarchives.org/OAI/2.0/oai_dc.xsd"
            metadata_namespace = "http://www.openarchives.org/OAI/2.0/oai_dc/"
            with open(
                finders.find(
                    join("core_oaipmh_provider_app", "xsd", "oai_dc.xsd")
                )
            ) as file:
                xml_schema = file.read()
                simpledc_path = finders.find(
                    join(
                        "core_oaipmh_provider_app",
                        "xsd",
                        "simpledc20021212.xsd",
                    )
                )

                # replace the simpledc schema URL with the local file version to avoid the HTTPS bug
                xml_schema = xml_schema.replace(
                    "http://dublincore.org/schemas/xmls/simpledc20021212.xsd",
                    simpledc_path,
                )

                oai_dublin_core = OaiProviderMetadataFormat(
                    metadata_prefix="oai_dc",
                    metadata_namespace=metadata_namespace,
                    schema=schema_url,
                    xml_schema=xml_schema,
                    is_default=True,
                    is_template=False,
                )

                system_api.upsert_oai_provider_metadata_format(oai_dublin_core)
    except Exception as exception:
        logger.error(
            "ERROR : Impossible to init the metadata formats: %s",
            str(exception),
        )

    logger.info("FINISH oai provider metadata format discovery.")
