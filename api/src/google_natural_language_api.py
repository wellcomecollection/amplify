import os

from google.cloud.language import LanguageServiceClient, enums, types


def analyze_entities(text):
    '''Returns a set of detected entities, and parameters associated with those entities, such as the
    entity's type, relevance of the entity to the overall text, and locations in the text that refer to the same entity.
    Entities are returned in the order (highest to lowest) of their salience scores, which reflect their relevance to
    the overall text.

    :param text: string
    :return: JSON
    '''

    client = LanguageServiceClient()

    document = types.Document(
        content=text, type=enums.Document.Type.PLAIN_TEXT)
    encoding_type = enums.EncodingType.UTF8

    entities = client.analyze_entities(
        document=document, encoding_type=encoding_type)

    return entities


def get_meta_data(entity):
    '''Return wikipedia links if exists for given entity.

    :param entity: google natural language api response.entities
    :return: string or None
    '''
    for metadata_name, metadata_value in entity.metadata.items():
        if metadata_name == 'wikipedia_url':
            return metadata_value
        else:
            return None


def retrieve_entities(response):
    '''Retrieve key fields from google natural language api named entity search.

    :param response: google natural language api analyze_entities
    :return:
    '''
    author, title, date, publisher, publisher_place = [], [], [], [], []
    meta_data = {}
    for entity in response.entities:
        entity_type = enums.Entity.Type(entity.type).name
        if entity_type == 'PERSON':
            author.append(entity.name)
            meta_data[entity.name] = get_meta_data(entity)
        elif entity_type == 'WORK_OF_ART':
            title.append(entity.name)
            meta_data[entity.name] = get_meta_data(entity)
        elif entity_type == 'ORGANIZATION':
            publisher.append(entity.name)
            meta_data[entity.name] = get_meta_data(entity)
        elif entity_type == 'LOCATION':
            publisher_place.append(entity.name)
            meta_data[entity.name] = get_meta_data(entity)
        elif entity_type == 'DATE':
            date.append(entity.name)
            meta_data[entity.name] = get_meta_data(entity)

    return author, title, date, publisher, publisher_place, meta_data
