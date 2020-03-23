import requests


def format_search_string(text):
    '''Format search string for search_record method's SEARCH expression.

    :param text: string
    :return: string (formatted)
    '''
    if text != None:
        text = text.lower().replace(' ', '+')
    else:
        text = ''
    return text


def search_record(author=None, title=None, publisher=None, date=None):
    '''Search record on Library Hub.

    :param author: string
    :param title: string
    :param publisher: string
    :param date: string
    :return: JSON
    '''
    BASE_URL = 'https://discover.libraryhub.jisc.ac.uk/search'

    SEARCH = '?format=json&' \
             'author='+format_search_string(author)+'&' \
             'title='+format_search_string(title)+'&' \
             'publisher='+format_search_string(publisher)+'&' \
             'publisher-place=&' \
             'isn=&' \
             'date='+format_search_string(date)+'&s' \
             'ubject=&' \
             'map-scale=&' \
             'held-by=&' \
             'keyword='

    response = requests.post(BASE_URL + SEARCH)
    return response


def checking_for_duplicates_at_wellcome(response, record_index=0):
    '''Checking for duplicates at Wellcome Library through Library Hub.

    :param response: JSON response from search_record method
    :param record_index: search_record method returns multiple records, thus a record_index must be specified
    :return: boolean
    '''
    for index in range(len(response.json()['records'][record_index]['holdings'])):
        institution_id = response.json()['records'][record_index]['holdings'][index]['held_at'][0]['institution'][
            'institution_id']
        if institution_id == 'wel':
            print('Book is in Wellcome Library!')
            return True
        else:
            return False


def show_results(response):
    # print(response.json()['records'][0]['bibliographic_data'])
    # try:
    #     print('Author: ' + response.json()['records'][0]['bibliographic_data']['author'][0])
    # except:
    #     print('No author found.')
    # try:
    #     print('Title: ' + response.json()['records'][0]['bibliographic_data']['title'][0])
    # except:
    #     print('No title found.')
    # try:
    #     print('Publication details: ' + response.json()['records'][0]['bibliographic_data']['publication_details'][0])
    # except:
    #     print('No publication details found.')
    # try:
    #     print('Institution ID: ' + response.json()['records'][0]['holdings'][0]['held_at'][0]['institution'][
    #     'institution_id'])
    # except:
    #     print('No institution ID found.')
    if checking_for_duplicates_at_wellcome(response, record_index=0) == True:
        print('Record is held by Wellcome!')
        return ('Record is held by Wellcome!')
    else:
        print('Record is not held by Wellcome!')
        return ('Record is not held by Wellcome!')

# Sample record from Library Hub::

# {'bibliographic_data': {'author': ['Deutsch, David.'],
#                         'isbn': ['9780141969619 (EPUB)', '014196961X (EPUB)'],
#                         'physical_description': ['1 online resource (400 pages).'],
#                         'publication_details': ['London : Penguin, 2011.'],
#                         'title': ['The fabric of reality / David Deutsch.'],
#                         'url': ['ark:/81055/vdc_100048487899.0x000001 https://tcdlibrary.ldls.org.uk/vdc_100048487759.0x000001 Available on Library reading room PCs only. Click here for access.']},
#  'holdings': [{'document_type': ['book'],
#                'held_at': [{'institution': {'institution_id': 'tcd',
#                                             'name': 'Trinity College Dublin Library'},
#                             'latitude': 53.3436012268066,
#                             'longitude': -6.25604009628296}],
#                'item_id': 45394468,
#                'physical_format': ['online']},
#               {'document_type': ['book'],
#                'held_at': [{'institution': {'institution_id': 'bli',
#                                             'name': 'British Library'},
#                             'latitude': 51.5289001464844,
#                             'longitude': -0.127482995390892}],
#                'item_id': 73962548,
#                'physical_format': ['online']},
#               {'document_type': ['book'],
#                'held_at': [{'institution': {'institution_id': 'nlw',
#                                             'name': 'National Library of Wales / Llyfrgell Genedlaethol Cymru'},
#                             'latitude': 52.4142990112305,
#                             'longitude': -4.06845998764038}],
#                'item_id': 188585216,
#                'physical_format': ['online']}],
#  'uri': 'https://discover.libraryhub.jisc.ac.uk/search?id=45394468&rn=1'}