import os
import requests


def open_search(text):
    '''Search with WorldCat OpenSearch API endpoint.

    :param text: string
    :return: string, XML
    '''
    BASE_URL = 'http://www.worldcat.org/webservices/catalog/search/worldcat/opensearch'

    SEARCH = {
        "q": text,
        'wskey': os.environ.get('WORLDCAT_WSKEY')
    }

    response = requests.post(BASE_URL, params=SEARCH)
    return response.text


def read(record_identifier):
    '''Search with WorldCat Read API endpoint.

    :param record_identifier: string
    :return: string, XML
    '''
    BASE_URL = 'http://www.worldcat.org/webservices/catalog/content/' + record_identifier

    SEARCH = {'wskey': os.environ.get('WORLDCAT_WSKEY')}

    response = requests.post(BASE_URL, params=SEARCH)
    return response.text
