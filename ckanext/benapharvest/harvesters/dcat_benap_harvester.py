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
        log.debug("dcat_dict")
        log.debug(dcat_dict)

        log.debug('harvest_object')
        log.debug(harvest_object)
        log.debug(harvest_object.source.config)

        package_dict['extras'] = self._process_extras(package_dict['extras'])

        package_dict['remote_harvest'] = True

        # Add tags
        package_dict['tags'].append({'name': 'harvested'})

        return package_dict

    def _process_extras(self, extras):
        new_extras = {}

        # Temporal start
        if 'Temporal start' in extras:
            new_extras['Temporal start'] = extras['Temporal start']
        elif 'modified' in extras:
            new_extras['Temporal start'] = extras['modified']
        else:
            now = datetime.now()
            new_extras['Temporal start'] = now.strftime("%Y-%m-%dT%H:%M:%S")

        # Regions covered
        if 'Regions covered' in extras:
            new_extras['Regions covered'] = extras['Regions covered']
        else:
            new_extras['Regions covered'] = ['http://publications.europa.eu/resource/authority/nuts/code/BE3']

        # Countries covered
        if 'Countries covered' in extras:
            new_extras['Countries covered'] = extras['Countries covered']
        else:
            new_extras['Countries covered'] = ['http://publications.europa.eu/resource/authority/country/BEL']

        # Language
        if 'Language' in extras:
            new_extras['Language'] = []
            languages = extras.get('Language', extras.get('language', []))
            for language in languages:
                new_extras['Language'].append(self._format_language(language))
        else:
            new_extras['Language'] = ['http://publications.europa.eu/resource/authority/country/BEL']

        log.debug(json.dumps(new_extras, indent=2))
        return new_extras

    @staticmethod
    def _format_language(language):
        log.debug(language)
        log.debug(language == 'http://lexvo.org/id/iso639-3/nld')
        if language == 'http://lexvo.org/id/iso639-3/nld':
            return 'http://publications.europa.eu/resource/authority/language/NLD'
        return input
