import json
import logging

from ckanext.dcat.harvesters.rdf import DCATRDFHarvester

from datetime import datetime

from ckanext.benapharvest.harvesters.utilities import format_language_list, format_notes_translated, find_by_key, \
    process_resources

log = logging.getLogger(__name__)


class DcatBenapHarvester(DCATRDFHarvester):

    def info(self):
        return {
            'name': 'benap_dcat',
            'title': 'BENAP DCAT',
            'description': 'Harvests remote DCAT metadata for use with transportdata.be, using full metadata profile',
            'form_config_interface': 'Text'
        }

    def modify_package_dict(self, package_dict, dcat_dict, harvest_object):
        log.debug("### benap_dcat ###")
        log.debug("---modify_package_dict---")
        config = json.loads(harvest_object.source.config)

        log.debug("\n" * 5)
        log.debug("###"*5)
        log.debug(package_dict)
        log.debug("###"*5)
        log.debug(dcat_dict)
        log.debug("###" * 5)
        log.debug(harvest_object)
        log.debug("###" * 5)
        log.debug("\n" * 5)

        extras_keys = [val['key'] for val in package_dict['extras']]

        package_dict['type'] = 'harvested-dataset'
        package_dict['remote_harvest'] = True

        package_dict['private'] = True

        # Add tags
        if 'fluent_tags' not in package_dict:
            package_dict['fluent_tags'] = []
        package_dict['fluent_tags'].append('Cycle')

        # License
        package_dict['license_id'] = "other-pd"
        package_dict['contract_license'] = "lifree"

        # Geographic location
        package_dict['countries_covered'] = ['http://publications.europa.eu/resource/authority/country/BEL']
        package_dict['regions_covered'] = ['http://data.europa.eu/nuts/code/BE2']

        # Frequency
        package_dict['frequency'] = 'http://publications.europa.eu/resource/authority/frequency/ANNUAL'

        # Language
        package_dict['language'] = format_language_list(extras_keys, package_dict['extras'])

        # Notes
        package_dict['notes_translated'] = format_notes_translated(package_dict['notes'], package_dict['language'])

        # Theme
        package_dict['theme'] = 'http://publications.europa.eu/resource/authority/data-theme/TRAN'

        # Temporal start
        if 'Temporal start' in extras_keys:
            package_dict['temporal_start'] = find_by_key(package_dict['extras'], 'Temporal start')
        elif 'issued' in extras_keys:
            package_dict['temporal_start'] = find_by_key(package_dict['extras'], 'issued')
        elif 'modified' in extras_keys:
            package_dict['temporal_start'] = find_by_key(package_dict['extras'], 'modified')
        else:
            now = datetime.now()
            package_dict['temporal_start'] = now.strftime("%Y-%m-%dT%H:%M:%S")

        # Publisher
        log.debug("---")
        log.debug(config['default_extras'])
        log.debug("---")
        package_dict['p_address'] = config['default_extras']['publisher_address']
        package_dict['p_tel'] = config['default_extras']['publisher_tel']
        package_dict['publisher_org'] = config['default_extras']['publisher_org']
        package_dict['publisher_name'] = config['default_extras']['publisher_name']
        package_dict['publisher_url'] = find_by_key(package_dict['extras'], 'publisher_uri')
        package_dict['publisher_email'] = config['default_extras']['publisher_email']

        # Contact
        package_dict['contact_name'] = find_by_key(package_dict['extras'], 'contact_uri')

        # Cont_res, value must be one of: Data set; Service
        package_dict['cont_res'] = 'Data set'

        # Agreement declaration
        package_dict['agreement_declaration'] = ['N']

        # Quality assessment
        package_dict['qual_ass'] = {'fr': '', 'de': '', 'nl': '', 'en': ''}

        # resources
        package_dict['resources'] = process_resources(package_dict['resources'])

        # remove extra's
        del package_dict['extras']

        # log.debug("final package_dict")
        # log.debug(json.dumps(package_dict, indent=2))
        return package_dict
