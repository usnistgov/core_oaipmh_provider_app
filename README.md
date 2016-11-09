# core_oaipmh_provider_app

core_oaipmh_provider_app is a Django app providing functionalities for providing data thanks to OAI-PMH.

## Quickstart

  1. Add "core_oaipmh_provider_app" to your INSTALLED_APPS setting like this::

  ```python
  INSTALLED_APPS = [
      ...
      'core_oaipmh_provider_app',
  ]
  ```

  2. Include the core_oaipmh_provider_app URLconf in your project urls.py like this::

  ```python
  url(r'^oai_pmh/', include('core_oaipmh_provider_app.urls')),
  ```

