""" discover Data for oai-pmh
"""
from core_oaipmh_provider_app.components.oai_data import api as oai_data_api
from core_main_app.components.data import api as data_api


def check_data_info():
    """ Check OAI-PMH data information.
    """
    try:
        data = data_api.get_all()
        for document in data:
            oai_data_api.upsert_from_data(document, force_update=False)
    except Exception, e:
        print('ERROR : Impossible to init the OAI-PMH data : %s' % e.message)
