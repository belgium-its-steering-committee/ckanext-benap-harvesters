import os
import logging

import six
import requests
import rdflib

from ckan import plugins as p
from ckan import model


from ckanext.harvest.harvesters import HarvesterBase
from ckanext.harvest.model import HarvestObject

from ckanext.dcat.interfaces import IDCATRDFHarvester


log = logging.getLogger(__name__)


class DcatBenapHarvester(HarvesterBase):

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

