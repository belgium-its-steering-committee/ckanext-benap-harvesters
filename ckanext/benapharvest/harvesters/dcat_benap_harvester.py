import os
import logging

import six
import requests
import rdflib

from ckan import plugins as p
from ckan import model

from ckanext.dcat.harvesters.base import DCATHarvester


log = logging.getLogger(__name__)


class DcatBenapHarvester(DCATHarvester):

    def info(self):
        return {
            'name': 'benap_dcat',
            'title': 'BENAP DCAT',
            'description': 'Harvests remote DCAT metadata for use with transportdata.be',
            'form_config_interface': 'Text'
        }

    def modify_package_dict(self, package_dict, harvest_object):
        log.debug("---modify_package_dict---")
        log.debug("package_dict")
        log.debug(package_dict)
        log.debug("harvest_object")
        log.debug(harvest_object)

        package_dict['remote_harvest'] = True

        # Add tags
        package_dict['tags'].append({'name': 'sdi'})

        return package_dict

