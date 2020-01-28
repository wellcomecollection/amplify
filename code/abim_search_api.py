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
    BASE_URL = 'http://indianmedicine.eldoc.ub.rug.nl/cgi/search/archive/advanced?'

    SEARCH = 'screen=Search&' \
            'dataset=archive&' \
             '_action_search=Search&' \
            'title_merge=ALL&' \
            'title='+format_search_string(title)+'&' \
            'titleorder_merge=ALL&' \
            'titleorder=&' \
            'authors_merge=ALL&' \
            'authors='+format_search_string(author)+'&' \
            'authorsorder_merge=ALL&' \
            'authorsorder=&' \
             'date='+format_search_string(date)+'&' \
            'description_merge=ALL&' \
            'description=&' \
            'annote_merge=ALL&' \
            'annote=&' \
            'note_location_merge=ALL&' \
            'note_location=&' \
            'note_description_merge=ALL&' \
            'note_description=&' \
            'note_checked_merge=ALL&' \
             'note_checked=&' \
            'publisher_merge=ALL&' \
            'publisher='+format_search_string(publisher)+'&' \
            'identifier_referenceID_merge=ALL&' \
            'identifier_referenceID=&' \
            'satisfyall=ALL&' \
            'order=-date%2Fauthorsorder%2Ftitleorder'

    response = requests.get(BASE_URL + SEARCH)

    print(response.text)

    return response

search_record(author=None, title='', publisher=None, date=None)


def show_results(response):
    print(response.json()['records'][0]['bibliographic_data'])
    try:
        print('Author: ' + response.json()['records'][0]['bibliographic_data']['author'][0])
    except:
        print('No author found.')
    try:
        print('Title: ' + response.json()['records'][0]['bibliographic_data']['title'][0])
    except:
        print('No title found.')
    try:
        print('Publication details: ' + response.json()['records'][0]['bibliographic_data']['publication_details'][0])
    except:
        print('No publication details found.')
    try:
        print('Institution ID: ' + response.json()['records'][0]['holdings'][0]['held_at'][0]['institution'][
        'institution_id'])
    except:
        print('No institution ID found.')
