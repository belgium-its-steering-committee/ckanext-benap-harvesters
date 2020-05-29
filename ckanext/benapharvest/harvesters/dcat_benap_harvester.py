import json
import logging

from ckanext.dcat.harvesters.rdf import DCATRDFHarvester

from datetime import datetime

log = logging.getLogger(__name__)


class DcatBenapHarvester(DCATRDFHarvester):

    def info(self):
        return {
            'name': 'benap_dcat',
            'title': 'BENAP DCAT',
            'description': 'Harvests remote DCAT metadata for use with transportdata.be',
            'form_config_interface': 'Text'
        }

    def modify_package_dict(self, package_dict, dcat_dict, harvest_object):
        log.debug("---modify_package_dict---")
        log.debug('config')
        log.debug(harvest_object.source.config)
        log.debug("-------")

        extras_keys = [val['key'] for val in package_dict['extras']]

        package_dict['remote_harvest'] = True

        # Add tags
        package_dict['tags'].append({'name': 'harvested'})
        if 'fluent_tags' not in package_dict:
            package_dict['fluent_tags'] = []
        package_dict['fluent_tags'].append({'name': 'Cycle'})

        # License
        package_dict['license_id'] = "CC0-1.0"
        package_dict['contract_license'] = "nolinoco"

        # Geographic location
        package_dict['countries_covered'] = ['http://publications.europa.eu/resource/authority/country/BEL']
        package_dict['regions_covered'] = ['http://data.europa.eu/nuts/code/BE3']

        # Frequency
        package_dict['frequency'] = 'http://publications.europa.eu/resource/authority/frequency/MONTHLY'

        # Language

        if 'Language' in extras_keys or 'language' in extras_keys:
            new_languages = []
            languages = json.loads(self._find_by_key(package_dict['extras'], 'language'))
            if languages is None:
                languages = json.loads(self._find_by_key(package_dict['extras'], 'Language'))
            for language in languages:
                new_languages.append(self._format_language(language))
            package_dict['language'] = new_languages
        else:
            package_dict['language'] = ['http://publications.europa.eu/resource/authority/language/NLD']

        # Theme
        package_dict['theme'] = 'http://publications.europa.eu/resource/authority/data-theme/TRAN'

        # Temporal start
        if 'Temporal start' in extras_keys:
            package_dict['temporal_start'] = self._find_by_key(package_dict['extras'], 'Temporal start')
        elif 'modified' in extras_keys:
            package_dict['temporal_start'] = self._find_by_key(package_dict['extras'], 'modified')
        else:
            now = datetime.now()
            package_dict['temporal_start'] = now.strftime("%Y-%m-%dT%H:%M:%S")

        # Publisher
        package_dict['p_address'] = 'publisher avenue, 1000 Bruxelles (Belgique)'
        package_dict['p_tel'] = '+32488999999'
        package_dict['publisher_org'] = 'new publisher'
        package_dict['publisher_name'] = 'publisher name'
        package_dict['publisher_url'] = 'https://www.publisher.com'
        package_dict['publisher_email'] = 'publisher@example.com'

        # Contact
        package_dict['contact_name'] = 'contact point name'

        # Other
        package_dict['cont_res'] = 'Cont Res'

        log.debug("final package_dict")
        log.debug(json.dumps(package_dict, indent=2))
        return package_dict

    @staticmethod
    def _format_language(language):
        if language == 'http://lexvo.org/id/iso639-3/nld':
            return 'http://publications.europa.eu/resource/authority/language/NLD'
        return input

    @staticmethod
    def _find_by_key(dict_list, key):
        return next(iter([val['value'] for val in dict_list if val['key'] == key]), None)

    @staticmethod
    def _add_to_dict_list(dict_list, key, value):
        dict_list.append({
            "key": key,
            "value": value
        })
