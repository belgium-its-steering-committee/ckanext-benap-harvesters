import json
import logging
import uuid
import random

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
        log.debug("---")
        log.debug("---object---")
        log.debug(harvest_object)
        log.debug("---")
        log.debug("---")
        log.debug("---package_dict---")
        log.debug(package_dict)
        log.debug("---")
        #log.debug("---")
        #log.debug("---dcat_dict---")
        #log.debug(dcat_dict)
        #log.debug("---")
        config = json.loads(harvest_object.source.config)
        #log.debug("---")
        #log.debug("---config---")
        #log.debug(config)
        #log.debug("---")

        extras_keys = [val['key'] for val in package_dict['extras']]
        #log.debug("---")
        log.debug("---extras keys---")
        log.debug(extras_keys)
        log.debug("---")

        resources_licenses = [val['license'] for val in package_dict['resources']]
        log.debug("---")
        log.debug("---resources licenses---")
        log.debug(resources_licenses)
        log.debug("---")

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

        #Identifier of dataset
        if 'identifier' in extras_keys:
            log.debug("---if identifier---")
            log.debug(self._find_by_key(package_dict['extras'], 'identifier'))
            log.debug("---")
            #package_dict['id'] = self._find_by_key(package_dict['extras'], 'identifier')
        else:
            #make a random UUID
            log.debug("---else identifier---")
            log.debug(uuid.uuid4())
            log.debug("---")
            #package_dict['id'] = uuid.uuid4()

        #publisher
        if 'publisher_uri' in extras_keys:
            package_dict['publisher_contact'] = self._find_by_key(package_dict['extras'], 'publisher_uri')
        else:
            package_dict['publisher_contact'] = "unknown"

        #maintainer
        if 'contact_uri' in extras_keys:
            package_dict['maintainer_contact'] = self._find_by_key(package_dict['extras'], 'contact_uri')
        else:
            package_dict['maintainer_contact'] = "unknown"

        #license
        if(len(resources_licenses) > 0):
            package_dict['license_id'] = resources_licenses[0]

        # Temporal start
        if 'modified' in extras_keys:
            package_dict['date_modified'] = self._find_by_key(package_dict['extras'], 'modified')

        else:
            now = datetime.now()
            package_dict['date_modified'] = now.strftime("%Y-%m-%dT%H:%M:%S")


        return package_dict

    @staticmethod
    def _format_language(language):
        if language == 'http://lexvo.org/id/iso639-3/nld':
            return 'http://publications.europa.eu/resource/authority/language/NLD'
        return input

    @staticmethod
    def _find_by_key(dict_list, key, default_value=''):
        return next(iter([val['value'] for val in dict_list if val['key'] == key]), default_value)