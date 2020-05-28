import logging

from ckanext.dcat.harvesters.rdf import DCATRDFHarvester

log = logging.getLogger(__name__)


class DcatBenapHarvester(DCATRDFHarvester):

    def info(self):
        return {
            'name': 'benap_dcat',
            'title': 'BENAP DCAT',
            'description': 'Harvests remote DCAT metadata for use with transportdata.be',
            'form_config_interface': 'Text'
        }

    def gather_stage(self, harvest_job):
        log.debug(harvest_job)
        log.debug(self)
        log.debug(super(DcatBenapHarvester, self))
        log.debug(super(DcatBenapHarvester, self).gather_stage)
        super(DcatBenapHarvester, self).gather_stage(harvest_job)

    def modify_package_dict(self, package_dict, dcat_dict, harvest_object):
        log.debug("---modify_package_dict---")
        log.debug("package_dict")
        log.debug(package_dict)
        log.debug("harvest_object")
        log.debug(harvest_object)
        log.debug("dcat_dict")
        log.debug(dcat_dict)

        package_dict['remote_harvest'] = True

        # Add tags
        package_dict['tags'].append({'name': 'sdi'})

        return package_dict
