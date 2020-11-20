# coding=utf-8
import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class BenapHarvesterPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer, plugins.IDatasetForm, inherit=True)

    # IConfigurer

    def update_config(self, config_):
        pass
