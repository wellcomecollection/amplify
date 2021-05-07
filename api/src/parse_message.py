import xml.etree.ElementTree as ET
from .worldcat_search_api import read


def parse(data, from_file=False):
    '''Parse and print individual MARC record retrieved by WorldCat Read API.

    :param data: string, XML or path to XML
    :param from_file: boolean
    :return: None
    '''

    author = ''
    title = ''
    publisher = ''

    if from_file:
        tree = ET.parse(data)
        root = tree.getroot()
    else:
        root = ET.fromstring(data)

    for child in root:
        try:
            tag = child.get('tag')
            if tag == '245':
                for subchild in child:
                    code = subchild.get('code')
                    if code == 'a':
                        title = subchild.text
                    elif code == 'c':
                        author = subchild.text
            elif tag == '264' or tag == '260':
                for subchild in child:
                    code = subchild.get('code')
                    if code == 'b':
                        publisher = subchild.text
        except:
            pass

    return author, title, publisher


def parse_detailed(data, from_file=False):
    '''Parse and print individual MARC record retrieved by WorldCat Read API.

    :param data: string, XML or path to XML
    :param from_file: boolean
    :return: None
    '''

    results = []

    if from_file:
        tree = ET.parse(data)
        root = tree.getroot()
    else:
        root = ET.fromstring(data)

    for child in root:
        try:
            tag = child.get('tag')
            for subchild in child:
                code = subchild.get('code')
                subfield = subchild.text
                results.append(
                    {'tag': tag, 'code': code, 'subfield': subfield})
        except:
            pass
    return results


def get_record_identifiers(data, from_file=False):
    '''Retrieve record identifiers from WorldCat Open Search API result.

    :param data: string, XML or path to XML
    :param from_file: boolean
    :return: dict, list (containing record identifiers)
    '''
    if from_file:
        tree = ET.parse(data)
        root = tree.getroot()
    else:
        root = ET.fromstring(data)

    record_identifier_list = []
    title_list = []
    record_identifier_dict_list = []
    for child in root:
        try:
            for entry in child:
                if entry.tag == '{http://www.w3.org/2005/Atom}title':
                    title = entry.text
                    title_list.append(title)
                if entry.tag == '{http://purl.org/oclc/terms/}recordIdentifier':
                    record_identifier = entry.text
                    record_identifier_list.append(record_identifier)
        except:
            pass

    for index in range(len(title_list)):
        worldcat_search_api_read_response = read(record_identifier_list[index])
        worldcat_results = parse_detailed(worldcat_search_api_read_response)
        record_identifier_dict_list.append(
            {'record_identifier': record_identifier_list[index], 'title': title_list[index], 'worldcat_results': worldcat_results})

    return record_identifier_dict_list
