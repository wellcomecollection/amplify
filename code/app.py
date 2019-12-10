import config
import parse_message
import google_vision_api

#Text extraction
response = google_vision_api.detect_text(config.IMAGE_PATH[0])
print(response)

#Work matching
#TODO: Search (on WorldCat)

#Retrieve record identifiers (IDs of books on WorldCat)
record_identifier_dict, record_identifier_list = parse_message.get_record_identifiers(config.WORLDCAT_SESRCH_API_RESPONSE_PATH[0])
print(record_identifier_list, record_identifier_dict)

#Retrieve individual MARC records
path = config.WORLDCAT_READ_API_RESPONSE_PATH[0]
parse_message.parse(path)
