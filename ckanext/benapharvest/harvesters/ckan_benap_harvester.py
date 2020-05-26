from ckanext.harvest.harvesters.ckanharvester import CKANHarvester

import logging
log = logging.getLogger(__name__)


class CkanBenapHarvester(CKANHarvester):

    def info(self):
        return {
            'name': 'benap_ckan',
            'title': 'BENAP CKAN',
            'description': 'Harvests remote CKAN instances for use with transportdata.be',
            'form_config_interface': 'Text'
        }

    def modify_package_dict(self, package_dict, harvest_object):

        log.debug("package_dict")
        log.debug(package_dict)
        log.debug("harvest_object")
        log.debug(harvest_object)

        package_dict['remote_harvest'] = True

        # Add tags
        package_dict['tags'].append({'name': 'sdi'})

        return package_dict
