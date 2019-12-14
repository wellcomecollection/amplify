import xml.etree.ElementTree as ET


def parse(data, from_file=False):
    '''Parse and print individual MARC record retrieved by WorldCat Read API.

    :param data: string, XML or path to XML
    :param from_file: boolean
    :return: None
    '''

    if from_file:
        tree = ET.parse(data)
        root = tree.getroot()
    else:
        root = ET.fromstring(data)

    for child in root:
        # print(child.tag, child.attrib)
        try:
            tag = child.get('tag')
            if tag == '245':
                for subchild in child:
                    code = subchild.get('code')
                    if code == 'a':
                        print('Title: ' + subchild.text)
                        title = subchild.text
                    elif code == 'c':
                        print('Author: ' + subchild.text)
                        author = subchild.text
            elif tag == '264' or tag == '260':
                for subchild in child:
                    code = subchild.get('code')
                    if code == 'a':
                        print('Location: ' + subchild.text)
                    elif code == 'b':
                        print('Publisher: ' + subchild.text)
                        publisher = subchild.text
                    elif code == 'c':
                        print('Publication Date: ' + subchild.text)
        except:
            pass
    return author, title, publisher


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
    record_identifier_dict = {}
    for child in root:
        try:
            for entry in child:
                if entry.tag == '{http://www.w3.org/2005/Atom}title':
                    title = entry.text
                    title_list.append(title)
                if entry.tag == '{http://purl.org/oclc/terms/}recordIdentifier':
                    record_identifier = entry.text
                    record_identifier_list.append(record_identifier)
            for index in range(len(title_list)):
                record_identifier_dict[record_identifier_list[index]] = title_list[index]
        except:
            pass

    return record_identifier_dict, record_identifier_list

