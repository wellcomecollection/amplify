import requests
import re
from re import finditer


def format_search_string(text):
    '''Format search string for search_record method's SEARCH expression.

    :param text: string
    :return: string (formatted)
    '''
    print(text)
    result = ''
    if text != None:
        if text == []:
            result = ''
        elif type(text) is list:
            for piece in text:
                piece = piece.lower().replace(' ', '+')
                result += piece + str(' ')
        else:
            result = text.lower().replace(' ', '+')
    print(result)
    return result


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

    print(SEARCH)

    response = requests.get(BASE_URL + SEARCH)

    return response.text


def parse_response(response):
    results = []

    start_positions = []
    end_positions = []

    for match in finditer("""<tr class="ep_search_result">
    <td style="padding-left: 0.5em">""", response):
        # print(match.span(), match.group())
        start_positions.append(match.span()[1])

    for match in finditer("""Publication]""", response):
        # print(match.span(), match.group())
        end_positions.append(match.span()[0])

    for i in range(len(start_positions)):
        document = str(response[start_positions[i]:end_positions[i]-1])
        document = document.replace("""</td>\n    <td style="padding-left: 0.5em">\n      \n\n\n   """, '')
        document = document.replace("""</em></a>\n\n\n""", '')
        results.append({'document': document})

    # results = [{'document': '1. Reddy, A. Madhusudana and&#13;\nB. Ravi Prasad Rao\n  \n\n(2011)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/62735/"><em>Medicinal plant wealth of Palakonda hill ranges, Kadapa district, Andhra Pradesh, India.    '},
    #            {'document': '2. Chakre, Onkar J.\n  \n\n(2010)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/55569/"><em>The Wealth of India -- a CSIR\'s encyclopaedia of information resource on economic plants, animals and minerals.    '}]

    splitted_results = []

    for i in results:
        splitted = re.split("""\n\n<a href="|\n\n|"><em>""", i['document'])
        splitted_results.append({'author': splitted[0], 'date': splitted[1], 'link': splitted[2], 'title': splitted[3]})

    print(splitted_results)

    return splitted_results
