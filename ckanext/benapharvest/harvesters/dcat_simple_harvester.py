import json
import logging

from ckanext.dcat.harvesters.rdf import DCATRDFHarvester

from datetime import datetime

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
        log.debug("---modify_package_dict---")
        config = json.loads(harvest_object.source.config)

        extras_keys = [val['key'] for val in package_dict['extras']]

        package_dict['type'] = 'harvest-simple-dataset'
        package_dict['remote_harvest'] = True

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

        return package_dict
