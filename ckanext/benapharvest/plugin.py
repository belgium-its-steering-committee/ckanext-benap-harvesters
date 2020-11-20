# coding=utf-8
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class BenapHarvesterPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IDatasetForm)

    # IConfigurer

    def update_config(self, config_):
        pass

    def create_package_schema(self):
        schema = super(BenapHarvesterPlugin, self).create_package_schema()
        schema.update({
            'id' : [toolkit.get_validator('ignore_missing'),
                    toolkit.get_convertor('convert_to_extras')]
        })
        return schema

    def update_package_schema(self):
        schema = super(BenapHarvesterPlugin, self).update_package_schema()
        schema.update({
            'id' : [toolkit.get_validator('ignore_missing'),
                    toolkit.get_convertor('convert_to_extras')]
        })
        return schema

    def show_package_schema(self):
        schema = super(BenapHarvesterPlugin, self).show_package_schema()
        schema.update({
            'id' : [toolkit.get_convertor('convert_from_extras'),
                    toolkit.get_validator('ignore_missing')]
        })
        return schema

    def is_fallback(self):
        return True

    def package_types(self):
        return []

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')

