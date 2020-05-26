from ckanext.harvest.harvesters.ckanharvester import CKANHarvester


class CkanBenapHarvester(CKANHarvester):

    def info(self):
        return {
            'name': 'benap_ckan',
            'title': 'BENAP CKAN',
            'description': 'Harvests remote CKAN instances for use with transportdata.be',
            'form_config_interface': 'Text'
        }

    def modify_package_dict(self, package_dict, harvest_object):
        # Set a default custom field

        print("#" * 30)
        print(package_dict)
        print("#" * 30)
        print(harvest_object)
        print("#" * 30)

        package_dict['remote_harvest'] = True

        # Add tags
        package_dict['tags'].append({'name': 'sdi'})

        return package_dict
