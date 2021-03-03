import json
import logging
from datetime import datetime

from ckanext.dcat.harvesters.rdf import DCATRDFHarvester

from ckanext.benapharvest.harvesters.utilities import find_by_key, format_language_list, format_notes_translated, \
    tag_value_from_tag_object

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
        log.debug("---")
        log.debug("---object---")
        log.debug(harvest_object)
        log.debug("---")
        log.debug("---")
        log.debug("---package_dict---")
        log.debug(package_dict)
        log.debug("---")
        # log.debug("---")
        # log.debug("---dcat_dict---")
        # log.debug(dcat_dict)
        # log.debug("---")
        config = json.loads(harvest_object.source.config)
        # log.debug("---")
        # log.debug("---config---")
        # log.debug(config)
        # log.debug("---")

        extras_keys = [val['key'] for val in package_dict['extras']]
        # log.debug("---")
        log.debug("---extras keys---")
        log.debug(extras_keys)
        log.debug("---")

        resources_licenses = [val['license'] for val in package_dict['resources']]
        log.debug("---")
        log.debug("---resources licenses---")
        log.debug(resources_licenses)
        log.debug("---")

        log.debug(package_dict['tags'])
        tags = [tag_value_from_tag_object(val) for val in package_dict['tags']]
        log.debug("---")
        log.debug("---tags---")
        log.debug(tags)
        log.debug("---")

        package_dict['type'] = 'harvest-simple-dataset'
        package_dict['remote_harvest'] = True

        # Language
        package_dict['language'] = format_language_list(extras_keys, package_dict['extras'])

        # Notes
        log.debug("---")
        log.debug("notes_translated")
        log.debug(package_dict['notes'])
        log.debug(package_dict['language'])
        log.debug(format_notes_translated(package_dict['notes'], package_dict['language']))
        log.debug("---")
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
        log.debug("publisher")
        if 'publisher_uri' in extras_keys:
            package_dict['publisher_contact'] = find_by_key(package_dict['extras'], 'publisher_uri')
        else:
            package_dict['publisher_contact'] = "unknown"

        # maintainer
        log.debug("maintainer")
        if 'contact_uri' in extras_keys:
            package_dict['maintainer_contact'] = find_by_key(package_dict['extras'], 'contact_uri')
        else:
            package_dict['maintainer_contact'] = "unknown"

        # license
        log.debug("license")
        if len(resources_licenses) > 0:
            package_dict['license_id'] = resources_licenses[0]

        # Temporal start
        log.debug("Temporal start")
        if 'modified' in extras_keys:
            package_dict['date_modified'] = find_by_key(package_dict['extras'], 'modified')
        else:
            now = datetime.now()
            package_dict['date_modified'] = now.strftime("%Y-%m-%dT%H:%M:%S")

        log.debug("---end custom processing--")
        log.debug("="*35)
        log.debug(package_dict)
        log.debug("="*35)
        return package_dict
