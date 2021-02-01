import json


def find_by_key(dict_list, key, default_value=''):
    return next(iter([val['value'] for val in dict_list if val['key'] == key]), default_value)


def add_to_dict_list(dict_list, key, value):
    dict_list.append({
        "key": key,
        "value": value
    })


def process_resources(resources):
    new_resources = []
    for resource in resources:
        new_resources.append(process_resource(resource))
    return new_resources


def process_resource(resource):
    new_resource = {'name': resource['name'],
                    'mimetype': resource['mimetype'],
                    'url': resource['url'],
                    'description': resource['description'],
                    'acc_mod': 'Other',
                    'acc_int': 'Other',
                    'acc_con': 'Pull',
                    'acc_desc': {'fr': '', 'de': '', 'nl': '', 'en': ''},
                    'resource_language': 'http://publications.europa.eu/resource/authority/language/NLD',
                    'format': map_format(resource['format'])}
    return new_resource


def map_format(resource_format):
    return resource_format if resource_format in ['XML', 'JSON', 'CSV', 'ASN.1 encoding rules',
                                                  'Protocol buffers'] else 'Other'


def format_language(language):
    if language in ('http://lexvo.org/id/iso639-3/nld', 'nl', 'nld', 'http://id.loc.gov/vocabulary/iso639-1/nl'):
        return 'http://publications.europa.eu/resource/authority/language/NLD'
    if language in ('http://lexvo.org/id/iso639-3/fra', 'fr', 'fra', 'http://id.loc.gov/vocabulary/iso639-1/fr'):
        return 'http://publications.europa.eu/resource/authority/language/FRA'
    if language in ('http://lexvo.org/id/iso639-3/eng', 'en', 'eng', 'http://id.loc.gov/vocabulary/iso639-1/en'):
        return 'http://publications.europa.eu/resource/authority/language/ENG'
    if language in ('http://lexvo.org/id/iso639-3/deu', 'de', 'deu', 'http://id.loc.gov/vocabulary/iso639-1/de'):
        return 'http://publications.europa.eu/resource/authority/language/DEU'
    return input


def format_language_list(extras_keys, extras):
    if 'Language' in extras_keys or 'language' in extras_keys:
        new_languages = []
        languages = json.loads(find_by_key(extras, 'language'))
        if languages is '':
            languages = json.loads(find_by_key(extras, 'Language'))
        for language in languages:
            new_languages.append(format_language(language))
        return new_languages
    else:
        return ['http://publications.europa.eu/resource/authority/language/NLD']


def format_notes_translated(notes, language):
    notes_translated = {
        'fr': '',
        'de': '',
        'nl': '',
        'en': ''
    }
    if 'http://publications.europa.eu/resource/authority/language/NLD' in language:
        notes_translated['nl'] = notes
    if 'http://publications.europa.eu/resource/authority/language/FRA' in language:
        notes_translated['fr'] = notes
    if 'http://publications.europa.eu/resource/authority/language/DEU' in language:
        notes_translated['de'] = notes
    if 'http://publications.europa.eu/resource/authority/language/ENG' in language:
        notes_translated['en'] = notes
    return notes_translated


def tag_value_from_tag_object(tag_object):
    """

    :param tag_object: object that holds tags. ex: {'name': 'Car-sharing'}
    :return: tag value, a string with the actual tag value
    """
    if 'tag' in tag_object:
        return tag_object['tag']
    elif 'name' in tag_object:
        return tag_object['name']
    return None
