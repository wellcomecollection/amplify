import xml.etree.ElementTree as ET
tree = ET.parse('../data/response.xml')
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
        elif tag == '264':
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