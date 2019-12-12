import config
import parse_message
import google_vision_api
import google_translate_api
import library_hub_api

print('Extracting text...')
response = google_vision_api.detect_text(config.IMAGE_PATH[0])
print(response)

print('Translating text...')
result = google_translate_api.translate_text(response)

print('Searching on WorldCat...')
#TODO: Search (on WorldCat)

print('Retrieving record identifiers (IDs of books) from WorldCat...')
record_identifier_dict, record_identifier_list = parse_message.get_record_identifiers(config.WORLDCAT_SESRCH_API_RESPONSE_PATH[0])
print(record_identifier_list, record_identifier_dict)

print('Retrieving individual MARC record(s)...')
path = config.WORLDCAT_READ_API_RESPONSE_PATH[0]
parse_message.parse(path)

print('Searching for duplicates in Library Hub ...')
response = library_hub_api.search_record(author='david deutsch', title='the fabric of reality', publisher='penguin books')

print(response.json()['records'][0]['bibliographic_data'])
print('Author: ' + response.json()['records'][0]['bibliographic_data']['author'][0])
print('Title: ' + response.json()['records'][0]['bibliographic_data']['title'][0])
print('Publication details: ' + response.json()['records'][0]['bibliographic_data']['publication_details'][0])
print('Institution ID: ' + response.json()['records'][0]['holdings'][0]['held_at'][0]['institution']['institution_id'])

print(library_hub_api.checking_for_duplicates_at_wellcome(response, record_index=0))