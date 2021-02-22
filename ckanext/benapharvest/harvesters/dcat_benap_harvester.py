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
        config = json.loads(harvest_object.source.config)

        extras_keys = [val['key'] for val in package_dict['extras']]

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
        if 'Language' in extras_keys or 'language' in extras_keys:
            new_languages = []
            languages = json.loads(self._find_by_key(package_dict['extras'], 'language'))
            if languages is '':
                languages = json.loads(self._find_by_key(package_dict['extras'], 'Language'))
            for language in languages:
                new_languages.append(self._format_language(language))
            package_dict['language'] = new_languages
        else:
            package_dict['language'] = ['http://publications.europa.eu/resource/authority/language/NLD']

        # Notes
        notes_translated = {
            'fr': '',
            'de': '',
            'nl': '',
            'en': ''
        }
        if 'http://publications.europa.eu/resource/authority/language/NLD' in package_dict['language']:
            notes_translated['nl'] = package_dict['notes']
        if 'http://publications.europa.eu/resource/authority/language/FRA' in package_dict['language']:
            notes_translated['fr'] = package_dict['notes']
        if 'http://publications.europa.eu/resource/authority/language/DEU' in package_dict['language']:
            notes_translated['de'] = package_dict['notes']
        if 'http://publications.europa.eu/resource/authority/language/ENG' in package_dict['language']:
            notes_translated['en'] = package_dict['notes']
        package_dict['notes_translated'] = notes_translated

        # Theme
        package_dict['theme'] = 'http://publications.europa.eu/resource/authority/data-theme/TRAN'

        # Temporal start
        if 'Temporal start' in extras_keys:
            package_dict['temporal_start'] = self._find_by_key(package_dict['extras'], 'Temporal start')
        elif 'issued' in extras_keys:
            package_dict['temporal_start'] = self._find_by_key(package_dict['extras'], 'issued')
        elif 'modified' in extras_keys:
            package_dict['temporal_start'] = self._find_by_key(package_dict['extras'], 'modified')
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
        package_dict['publisher_url'] = self._find_by_key(package_dict['extras'], 'publisher_uri')
        package_dict['publisher_email'] = config['default_extras']['publisher_email']

        # Contact
        package_dict['contact_name'] = self._find_by_key(package_dict['extras'], 'contact_uri')

        # Cont_res, value must be one of: Data set; Service
        package_dict['cont_res'] = 'Data set'

        # Agreement declaration
        package_dict['agreement_declaration'] = ['N']

        # Quality assessment
        package_dict['qual_ass'] = {'fr': '', 'de': '', 'nl': '', 'en': ''}

        # resources
        package_dict['resources'] = self._process_resources(package_dict['resources'])

        # remove extra's
        del package_dict['extras']

        # log.debug("final package_dict")
        # log.debug(json.dumps(package_dict, indent=2))
        return package_dict

    @staticmethod
    def _format_language(language):
        if language == 'http://lexvo.org/id/iso639-3/nld':
            return 'http://publications.europa.eu/resource/authority/language/NLD'
        return input

    @staticmethod
    def _find_by_key(dict_list, key, default_value=''):
        return next(iter([val['value'] for val in dict_list if val['key'] == key]), default_value)

    @staticmethod
    def _add_to_dict_list(dict_list, key, value):
        dict_list.append({
            "key": key,
            "value": value
        })

    def _process_resources(self, resources):
        new_resources = []
        for resource in resources:
            new_resources.append(self._process_resource(resource))
        return new_resources

    def _process_resource(self, resource):
        new_resource = {'name': resource['name'], 'mimetype': resource['mimetype'], 'url': resource['url'],
                        'description': resource['description']}
        new_resource['acc_mod'] = 'Other'
        new_resource['acc_int'] = 'Other'
        new_resource['acc_con'] = 'Pull'
        new_resource['acc_desc'] = {'fr': '', 'de': '', 'nl': '', 'en': ''}
        new_resource['resource_language'] = 'http://publications.europa.eu/resource/authority/language/NLD'
        new_resource['format'] = self._map_format(resource['format'])
        return new_resource

    @staticmethod
    def _map_format(resource_format):
        return resource_format if resource_format in ['XML', 'JSON', 'CSV', 'ASN.1 encoding rules',
                                                      'Protocol buffers'] else 'Other'
