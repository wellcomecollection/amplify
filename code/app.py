import config
import parse_message
import google_vision_api

print('Extracting text...')
response = google_vision_api.detect_text(config.IMAGE_PATH[0])
print(response)

print('Searching on WorldCat...')
#TODO: Search (on WorldCat)

print('Retrieving record identifiers (IDs of books) from WorldCat...')
record_identifier_dict, record_identifier_list = parse_message.get_record_identifiers(config.WORLDCAT_SESRCH_API_RESPONSE_PATH[0])
print(record_identifier_list, record_identifier_dict)

print('Retrieving individual MARC record(s)...')
path = config.WORLDCAT_READ_API_RESPONSE_PATH[0]
parse_message.parse(path)
