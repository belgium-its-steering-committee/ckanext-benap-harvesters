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
        log.debug("package_dict")
        log.debug(json.dumps(package_dict, indent=2))

        log.debug('config')
        log.debug(harvest_object.source.config)

        package_dict['extras'] = self._process_extras(package_dict['extras'])

        package_dict['remote_harvest'] = True

        # Add tags
        package_dict['tags'].append({'name': 'harvested'})

        package_dict['Countries covered'] = ['http://publications.europa.eu/resource/authority/country/BEL']
        package_dict[u'Countries covered'] = ['http://publications.europa.eu/resource/authority/country/BEL']

        log.debug("final package_dict")
        log.debug(json.dumps(package_dict, indent=2))
        return package_dict

    def _process_extras(self, extras):
        extras_keys = [val['key'] for val in extras]

        new_extras = []

        # Temporal start
        if 'Temporal start' in extras_keys:
            self._add_to_dict_list(new_extras, 'Temporal start', self._find_by_key(extras, 'Temporal start'))
        elif 'modified' in extras_keys:
            self._add_to_dict_list(new_extras, 'Temporal start', self._find_by_key(extras, 'modified'))
        else:
            now = datetime.now()
            self._add_to_dict_list(new_extras, 'Temporal start', now.strftime("%Y-%m-%dT%H:%M:%S"))

        # Regions covered
        if 'Regions covered' in extras_keys:
            self._add_to_dict_list(new_extras, 'Regions covered', self._find_by_key(extras, 'Regions covered'))
        else:
            self._add_to_dict_list(new_extras, 'Regions covered',
                                   ['http://publications.europa.eu/resource/authority/nuts/code/BE3'])

        # Countries covered
        if 'Countries covered' in extras_keys:
            self._add_to_dict_list(new_extras, 'Countries covered', self._find_by_key(extras, 'Countries covered'))
        else:
            self._add_to_dict_list(new_extras, u'Countries covered',
                                   ['http://publications.europa.eu/resource/authority/country/BEL'])

        # Language
        if 'Language' in extras_keys or 'language' in extras_keys:
            new_languages = []
            languages = json.loads(self._find_by_key(extras, 'language'))
            if languages is None:
                languages = json.loads(self._find_by_key(extras, 'Language'))
            for language in languages:
                new_languages.append(self._format_language(language))
            self._add_to_dict_list(new_extras, 'Language', new_languages)
        else:
            self._add_to_dict_list(new_extras, 'Language',
                                   ['http://publications.europa.eu/resource/authority/language/NLD'])

        log.debug(json.dumps(new_extras, indent=2))
        return new_extras

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
            "key":key,
            "value":value
        })
