import config
import requests


def open_search(text):
    '''Search with WorldCat OpenSearch API endpoint.

    :param text: string
    :return: string, XML
    '''
    BASE_URL = 'http://www.worldcat.org/webservices/catalog/search/worldcat/opensearch'

    SEARCH = '?q=' + text + '&' \
             'wskey=' + config.WORLDCAT_WSKEY

    response = requests.post(BASE_URL + SEARCH)
    return response.text


def read(record_identifier):
    '''Search with WorldCat Read API endpoint.

    :param record_identifier: string
    :return: string, XML
    '''
    BASE_URL = 'http://www.worldcat.org/webservices/catalog/content/'

    SEARCH = record_identifier + '?' \
             'wskey=' + config.WORLDCAT_WSKEY

    response = requests.post(BASE_URL + SEARCH)
    return response.text
