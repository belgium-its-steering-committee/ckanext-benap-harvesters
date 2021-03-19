import json
import logging
from datetime import datetime

from ckanext.dcat.harvesters.rdf import DCATRDFHarvester

from ckanext.benapharvest.harvesters.utilities import find_by_key, format_language_list, format_notes_translated, \
    tag_value_from_tag_object, fluent_tag_object_from_tag_value

log = logging.getLogger(__name__)


class DcatSimpleHarvester(DCATRDFHarvester):

    def info(self):
        return {
            'name': 'simple_dcat',
            'title': 'SIMPLE DCAT',
            'description': 'Harvests remote DCAT metadata for use with transportdata.be',
            'form_config_interface': 'Text'
        }

    def modify_package_dict(self, package_dict, dcat_dict, harvest_object):
        log.debug("### simple_dcat ###")
        log.debug("---modify_package_dict---")

        extras_keys = [val['key'] for val in package_dict['extras']]

        resources_licenses = [val['license'] for val in package_dict['resources']]

        tags = [tag_value_from_tag_object(val) for val in package_dict['tags']]
        log.debug("---tags---")
        log.debug(package_dict['tags'])
        log.debug(tags)
        log.debug("---")
        #fluent_tags = [fluent_tag_object_from_tag_value(val) for val in tags]
        #log.debug(fluent_tags)
        package_dict['fluent_tags'] = []
        log.debug("---")


        package_dict['type'] = 'harvest-simple-dataset'
        package_dict['remote_harvest'] = True

        # Language
        package_dict['language'] = format_language_list(extras_keys, package_dict['extras'])

        # Notes
        package_dict['notes_translated'] = format_notes_translated(package_dict['notes'], package_dict['language'])

        # Identifier of dataset
        if 'identifier' in extras_keys:
            log.debug("---if identifier---")
            log.debug(find_by_key(package_dict['extras'], 'identifier'))
            log.debug("---")
            package_dict['custom_id'] = find_by_key(package_dict['extras'], 'identifier')
        else:
            # make a random UUID
            log.debug("---else identifier---")
            log.debug("---")
            package_dict['custom_id'] = "none"

        # publisher
        if 'publisher_uri' in extras_keys:
            package_dict['publisher_contact'] = find_by_key(package_dict['extras'], 'publisher_uri')
        else:
            package_dict['publisher_contact'] = "unknown"

        # maintainer
        if 'contact_uri' in extras_keys:
            package_dict['maintainer_contact'] = find_by_key(package_dict['extras'], 'contact_uri')
        else:
            package_dict['maintainer_contact'] = "unknown"

        # license
        if len(resources_licenses) > 0:
            package_dict['license_id'] = resources_licenses[0]

        # Temporal start
        if 'modified' in extras_keys:
            package_dict['date_modified'] = find_by_key(package_dict['extras'], 'modified')
        else:
            now = datetime.now()
            package_dict['date_modified'] = now.strftime("%Y-%m-%dT%H:%M:%S")

        log.debug("---end custom processing--")
        return package_dict
