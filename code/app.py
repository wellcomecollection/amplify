import config
import parse_message
import google_vision_api
import google_translate_api
import google_natural_language_api
import library_hub_api
import worldcat_search_api
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin


app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/vision": {"origins": "http://localhost:4201"}, r"/post_vision": {"origins": "http://localhost:4201"}})


@app.route('/vision', methods=["GET"])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_vision():
    img_loc = config.IMAGE_PATH[0]
    print('Extracting text...')
    google_vision_api_response = google_vision_api.detect_text('frontend/src/' + img_loc)
    print('Translating text...')
    google_translate_api_response = google_translate_api.translate_text(google_vision_api_response)
    print('Analyzing text...')
    google_natural_language_api_response = google_natural_language_api.analyze_entities(google_vision_api_response)
    author, title, date, publisher, publisher_place, meta_data = google_natural_language_api.retrieve_entities(google_natural_language_api_response)
    print('Running Open Search on WorldCat...')
    worldcat_search_api_open_search_response = worldcat_search_api.open_search(google_vision_api_response)
    print('Retrieving record identifiers from WorldCat Open Search response...')
    record_identifier_dict, record_identifier_list = parse_message.get_record_identifiers(worldcat_search_api_open_search_response)
    print('Retrieving individual MARC record XML from WorldCat Read endpoint...')
    try:
        worldcat_search_api_read_response = worldcat_search_api.read(record_identifier_list[0])
        print('Parse MARC record...')
        worldcat_author, worldcat_title, worldcat_publisher = parse_message.parse(worldcat_search_api_read_response)
        print('Searching for duplicates in Library Hub...')
        library_hub_api_response = library_hub_api.search_record(author=worldcat_author, title=worldcat_title, publisher=worldcat_publisher)
        print('Author: {}, Title: {}, Publisher: {}'.format(worldcat_author, worldcat_title, worldcat_publisher))
        print('Showing results...')
        library_hub_api_response = library_hub_api.show_results(library_hub_api_response)
    except:
        record_identifier_dict = {'No results': 'NA'}
        worldcat_author, worldcat_title, worldcat_publisher, library_hub_api_response = None, None, None, None

    return jsonify({'google_vision_api_response': google_vision_api_response,
                    'detectedSourceLanguage': google_translate_api_response['detectedSourceLanguage'],
                    'translatedText': google_translate_api_response['translatedText'],
                    'img_loc': img_loc,
                    'author': author,
                    'title': title,
                    'date': date,
                    'publisher': publisher,
                    'publisher_place': publisher_place,
                    'meta_data': meta_data,
                    'record_identifier_dict': record_identifier_dict,
                    'worldcat_author': worldcat_author,
                    'worldcat_title': worldcat_title,
                    'worldcat_publisher': worldcat_publisher,
                    'library_hub_api_response': library_hub_api_response})


if __name__ == "__main__":
    app.run(port=4201)


# print('Extracting text...')
# response = google_vision_api.detect_text(config.IMAGE_PATH[0])
# # response = google_vision_api.detect_text('../data/sample_5.1.png')
# # response = google_vision_api.detect_text('../data/IMG_8172.jpg')
# print(response)
#
# # response = "THE, WEALTH OF INDIA, A Dictionary of Indian Raw Materials, and Industrial Products, INDUSTRIAL"
#
# print('Translating text...')
# result = google_translate_api.translate_text(response)
#
# print('Analyzing text...')
# # response = u'David Deutsch, The Fabric of Reality, Penguin Books, 1997.'
# # response = u'David Deutsch, The Beginning of Infinity, Viking Publishing House, 2011'
# response_ne = google_natural_language_api.analyze_entities(response)
# author, title, date, publisher, meta_data = google_natural_language_api.retrieve_entities(response_ne)
# print('Author: {}, Title: {}, Publisher: {}, Date: {}'.format(author, title, publisher, date))
# print('Meta data related to search: {}'.format(meta_data))
#
# print('Running Open Search on WorldCat...')
# response = worldcat_search_api.open_search(response)
#
# print('Retrieving record identifiers from WorldCat Open Search response...')
# # record_identifier_dict, record_identifier_list = parse_message.get_record_identifiers(config.WORLDCAT_SESRCH_API_RESPONSE_PATH[0], from_file=True)
# record_identifier_dict, record_identifier_list = parse_message.get_record_identifiers(response)
# print(record_identifier_list, record_identifier_dict)
#
# print('Retrieving individual MARC record XML from WorldCat Read endpoint...')
# response = worldcat_search_api.read(record_identifier_list[0])
#
# print('Parse MARC record...')
# # parse_message.parse(config.WORLDCAT_READ_API_RESPONSE_PATH[0], from_file=True)
# author, title, publisher = parse_message.parse(response)
#
# print('Searching for duplicates in Library Hub...')
# response = library_hub_api.search_record(author=author, title=title, publisher=publisher)
#
# print('Showing results...')
# library_hub_api.show_results(response)