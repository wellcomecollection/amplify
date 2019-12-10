import xml.etree.ElementTree as ET

def parse(path):

    tree = ET.parse(path)
    root = tree.getroot()

    # print(root.tag)
    # print(root.attrib)

    for child in root:
        # print(child.tag, child.attrib)
        try:
            tag = child.get('tag')
            if tag == '245':
                for subchild in child:
                    code = subchild.get('code')
                    if code == 'a':
                        print('Title: ' + subchild.text)
                    elif code == 'c':
                        print('Author: ' + subchild.text)
            elif tag == '264' or tag == '260':
                for subchild in child:
                    code = subchild.get('code')
                    if code == 'a':
                        print('Location: ' + subchild.text)
                    elif code == 'b':
                        print('Publisher: ' + subchild.text)
                    elif code == 'c':
                        print('Publication Date: ' + subchild.text)
        except:
            pass


def get_record_identifiers(path):
    tree = ET.parse(path)
    root = tree.getroot()

    record_identifier_list = []
    title_list = []
    record_identifier_dict = {}
    for child in root:
        try:
            for entry in child:
                if entry.tag == '{http://www.w3.org/2005/Atom}title':
                    # print('Title: ' + entry.text)
                    title = entry.text
                    title_list.append(title)
                if entry.tag == '{http://purl.org/oclc/terms/}recordIdentifier':
                    # print('Record Identifire: ' + entry.text)
                    record_identifier = entry.text
                    record_identifier_list.append(record_identifier)
            for index in range(len(title_list)):
                record_identifier_dict[record_identifier_list[index]] = title_list[index]
        except:
            pass

    return record_identifier_dict, record_identifier_list