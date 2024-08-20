""" Fixtures files for OAI provider
"""

import json
from os.path import join

from core_main_app.components.data.models import Data
from core_main_app.components.template.models import Template
from core_main_app.components.template_version_manager.models import (
    TemplateVersionManager,
)
from core_main_app.components.workspace import api as workspace_api
from core_main_app.components.workspace.models import Workspace
from core_main_app.utils.integration_tests.fixture_interface import (
    FixtureInterface,
)
from core_oaipmh_provider_app.components.oai_data.models import OaiData
from core_oaipmh_provider_app.components.oai_provider_metadata_format.models import (
    OaiProviderMetadataFormat,
)
from core_oaipmh_provider_app.components.oai_provider_set.models import (
    OaiProviderSet,
)
from core_oaipmh_provider_app.components.oai_settings.models import OaiSettings
from core_oaipmh_provider_app.settings import OAI_SCHEME, OAI_REPO_IDENTIFIER
from tests.test_settings import OAI_PROVIDER_ROOT

DUMP_OAI_PMH_TEST_PATH = join(OAI_PROVIDER_ROOT, "utils", "tests", "data")


class OaiPmhFixtures(FixtureInterface):
    """Represent OaiPmh Integration Fixture"""

    url = "http://www.server.com"
    harvest_rate = 5000
    harvest = True
    registry = None
    oai_identify = None
    settings = None
    templates = []
    template_version_managers = []
    oai_sets = []
    oai_metadata_formats = []
    oai_records = []
    data = []
    oai_data = []
    name = "Registry"
    identifier = "dummy"
    data_identifiers = []
    workspaces = []
    nb_public_data = 0
    nb_oai_data = 0

    def insert_data(self):
        """Insert data"""
        self.insert_settings()
        self.insert_workspaces()
        self.insert_template_version_managers()
        self.insert_templates()
        self.insert_record()
        self.insert_oai_record()
        self.insert_oai_metadata_format()
        self.insert_oai_set()

        self.loaded = True

    def insert_settings(self):
        """Insert settings fixtures"""
        oai_settings = OaiSettings(
            repository_name=self.name,
            repository_identifier=self.identifier,
            enable_harvesting=True,
        )
        oai_settings.save()
        self.settings = oai_settings

    def insert_template_version_managers(self):
        """Insert template version manager fixtures"""
        saved_template_version_managers = []
        list_template_version_manager = (
            OaiPmhMock.mock_template_version_manager()
        )

        for template_version_manager in list_template_version_manager:
            template_version_manager.save()
            saved_template_version_managers.append(template_version_manager)

        self.template_version_managers = saved_template_version_managers

    def insert_templates(self):
        """Template's methods"""
        saved_templates = []
        list_templates = OaiPmhMock.mock_template(
            template_version_manager_map={
                template_version_manager.id: template_version_manager
                for template_version_manager in self.template_version_managers
            }
        )

        for template in list_templates:
            template.save_template()
            saved_templates.append(template)

        self.templates = saved_templates

    def insert_workspaces(self):
        """Workspace's methods"""
        saved_workspaces = []
        list_workspaces = OaiPmhMock.mock_workspaces()
        for workspace in list_workspaces:
            workspace.save()
            saved_workspaces.append(workspace)

        self.workspaces = saved_workspaces

    def insert_record(self):
        """Data's methods"""
        saved_data = []
        self.nb_public_data = 0
        list_data = OaiPmhMock.mock_data(
            template_map={
                template.id: template for template in self.templates
            },
            workspace_map={
                workspace.id: workspace for workspace in self.workspaces
            },
        )
        for elt in list_data:
            elt.save()
            saved_data.append(elt)
            if (
                elt.workspace is not None
                and workspace_api.is_workspace_public(elt.workspace)
            ):
                self.nb_public_data += 1

        self.data = saved_data

    def insert_oai_record(self):
        """OaiData's methods"""
        self.nb_oai_data = 0
        saved_data = []
        list_data = OaiPmhMock.mock_oai_data(
            template_map={
                template.id: template for template in self.templates
            },
            data_map={data.id: data for data in self.data},
        )
        for elt in list_data:
            saved_data.append(elt.save())
            identifier = "%s:%s:id/%s" % (
                OAI_SCHEME,
                OAI_REPO_IDENTIFIER,
                str(elt.id),
            )
            self.data_identifiers.append(identifier)
            self.nb_oai_data += 1

        self.oai_data = saved_data

    def insert_oai_metadata_format(self):
        """OaiPmhProviderMetadataFormat's methods"""
        saved_data = []
        list_data = OaiPmhMock.mock_oai_metadata_format(
            template_map={
                template.id: template for template in self.templates
            },
        )
        for elt in list_data:
            saved_data.append(elt.save())

        self.oai_metadata_formats = saved_data

    def insert_oai_set(self):
        """Insert OAI sets"""
        saved_data = []
        list_data = OaiPmhMock.mock_oai_set(
            template_version_manager_map={
                template_version_manager.id: template_version_manager
                for template_version_manager in self.template_version_managers
            }
        )
        for elt in list_data:
            elt["object"].save()
            elt["object"].templates_manager.set(elt["templates_manager"])
            saved_data.append(elt)

        self.oai_sets = saved_data


class OaiPmhMock:
    """OaiPmh Mock"""

    @staticmethod
    def load_json_data(filename):
        """load_json_data

        Args:
            filename:

        Returns:
        """
        with open(join(DUMP_OAI_PMH_TEST_PATH, filename)) as fp:
            return json.load(fp)

    @staticmethod
    def mock_template(version="", template_version_manager_map=None):
        """mock_template

        Args:
            version:
            template_version_manager_map:

        Returns:
        """
        list_templates = list()
        for template_data in OaiPmhMock.load_json_data(
            f"template{version}.json"
        ):
            template_version_manager_data = template_data["version_manager"]
            del template_data["version_manager"]

            template = Template(**template_data)

            if template_version_manager_map:
                template.version_manager = template_version_manager_map[
                    template_version_manager_data["id"]
                ]
                template.is_current = template_version_manager_data[
                    "is_current"
                ]

            list_templates.append(template)

        return list_templates

    @staticmethod
    def mock_template_version_manager(version=""):
        """mock_template_version_manager

        Args:
            version:

        Returns:
        """
        data_json = OaiPmhMock.load_json_data(
            f"template_version_manager{version}.json"
        )
        list_templates = [TemplateVersionManager(**x) for x in data_json]
        return list_templates

    @staticmethod
    def mock_oai_first_template(version=""):
        """mock_oai_first_template

        Args:
            version:

        Returns:
        """
        list_templates = OaiPmhMock.mock_template(version)
        return list_templates[0]

    @staticmethod
    def mock_workspaces(version=""):
        """mock_workspaces

        Args:
            version:

        Returns:
        """
        data_json = OaiPmhMock.load_json_data(f"workspaces{version}.json")
        list_data = [Workspace(**x) for x in data_json]
        return list_data

    @staticmethod
    def mock_data(version="", template_map=None, workspace_map=None):
        """mock_data

        Args:
            version:
            template_map:
            workspace_map:

        Returns:
        """
        data_list = list()
        for json_data in OaiPmhMock.load_json_data(f"data{version}.json"):
            template_id = json_data["template"]
            del json_data["template"]

            workspace_id = None
            if "workspace" in json_data.keys():
                workspace_id = json_data["workspace"]
                del json_data["workspace"]

            data = Data(**json_data)

            if template_map:
                data.template = template_map[template_id]

            if workspace_map and workspace_id:
                data.workspace = workspace_map[workspace_id]

            data_list.append(data)

        return data_list

    @staticmethod
    def mock_oai_data(version="", template_map=None, data_map=None):
        """mock_oai_data

        Args:
            version:
            template_map:
            data_map:

        Returns:
        """
        list_data = list()

        for data_json in OaiPmhMock.load_json_data(f"oai_data{version}.json"):
            template_id = data_json["template"]
            del data_json["template"]

            data_id = data_json["data"]
            del data_json["data"]

            oai_data = OaiData(**data_json)

            if template_map and data_map:
                oai_data.template = template_map[template_id]

                if data_id:
                    oai_data.data = data_map[data_id]

            list_data.append(oai_data)

        return list_data

    @staticmethod
    def mock_oai_metadata_format(version="", template_map=None):
        """mock_oai_metadata_format

        Args:
            version:
            template_map:

        Returns:
        """
        list_metadata_format = list()

        for oai_metadata_format_data in OaiPmhMock.load_json_data(
            f"oai_metadata_format{version}.json"
        ):
            oai_metadata_format_template_id = oai_metadata_format_data[
                "template"
            ]
            del oai_metadata_format_data["template"]

            oai_metadata_format = OaiProviderMetadataFormat(
                **oai_metadata_format_data
            )

            if template_map:
                oai_metadata_format.template = template_map[
                    oai_metadata_format_template_id
                ]

            list_metadata_format.append(oai_metadata_format)

        return list_metadata_format

    @staticmethod
    def mock_oai_first_metadata_format(version=""):
        """mock_oai_first_metadata_format

        Args:
            version:

        Returns:
        """
        list_oai_metadata_formats = OaiPmhMock.mock_oai_metadata_format(
            version
        )
        return list_oai_metadata_formats[0]

    @staticmethod
    def mock_oai_set(version="", template_version_manager_map=None):
        """mock_oai_set

        Args:
            version:
            template_version_manager_map:

        Returns:
        """
        list_set = list()

        for oai_set_data in OaiPmhMock.load_json_data(
            f"oai_set{version}.json"
        ):
            oai_set_templates_manager = oai_set_data["templates_manager"]
            del oai_set_data["templates_manager"]

            oai_set = OaiProviderSet(**oai_set_data)

            templates_manager = list()
            if template_version_manager_map:
                templates_manager = [
                    template_version_manager_map[template_version_manager_id]
                    for template_version_manager_id in oai_set_templates_manager
                ]

            list_set.append(
                {
                    "object": oai_set,
                    "templates_manager": templates_manager,
                }
            )

        return list_set

    @staticmethod
    def mock_oai_first_set(version=""):
        """mock_oai_first_set

        Args:
            version:

        Returns:
        """
        list_oai_sets = OaiPmhMock.mock_oai_set(version)
        return list_oai_sets[0]["object"]
