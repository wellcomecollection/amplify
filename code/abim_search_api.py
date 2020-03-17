import requests
import re
from re import finditer


def format_search_string(text):
    '''Format search string for search_record method's SEARCH expression.

    :param text: string
    :return: string (formatted)
    '''
    print(text)
    if text != None:
        if text == []:
            text = ''
        else:
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

    # print(response.text)

    return response.text


def parse_response(response):
    results = []

    start_positions = []
    end_positions = []

    for match in finditer("""<tr class="ep_search_result">
    <td style="padding-left: 0.5em">""", response):
        print(match.span(), match.group())
        start_positions.append(match.span()[1])

    for match in finditer("""Publication]""", response):
        print(match.span(), match.group())
        end_positions.append(match.span()[0])

    print(start_positions)
    print(end_positions)

    for i in range(len(start_positions)):
        print(response[start_positions[i]:end_positions[i]-1])
        results.append({'document': response[start_positions[i]:end_positions[i]-1]})

    return results


# response = search_record(author=None, title='the wealth of india', publisher=None, date=None)
#
# results = parse_response(response)
