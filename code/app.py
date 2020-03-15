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
cors = CORS(app, resources={r"/visionStage1": {"origins": "http://localhost:4204"}, r"/post_vision": {"origins": "http://localhost:4204"}})


@app.route('/visionStage1', methods=["POST"])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_visionStage1():
    image = request.files['image']
    print(image)
    img_loc = config.IMAGE_PATH[0]
    print('Extracting text...')
    # google_vision_api_response = google_vision_api.detect_text('frontend/src/' + img_loc)
    google_vision_api_response = google_vision_api.detect_text(image, from_path=False)
    print('Translating text...')
    google_translate_api_response = google_translate_api.translate_text(google_vision_api_response)
    try:
        print('Analyzing text...')
        google_natural_language_api_response = google_natural_language_api.analyze_entities(google_translate_api_response['translatedText'])
        author, title, date, publisher, publisher_place, meta_data = google_natural_language_api.retrieve_entities(google_natural_language_api_response)
    except:
        author, title, date, publisher, publisher_place, meta_data = None, None, None, None, None, None

    print('Running Open Search on WorldCat...')
    worldcat_search_api_open_search_response = worldcat_search_api.open_search(google_vision_api_response)
    print('Retrieving record identifiers from WorldCat Open Search response...')
    record_identifier_dict, record_identifier_list = parse_message.get_record_identifiers(worldcat_search_api_open_search_response)

    # record_identifier_dict_list = []

    print('Retrieving individual MARC record XML from WorldCat Read endpoint...')
    try:
        # for item in record_identifier_dict:
        #     print('Printing dict list...')
        #     print(item)
        #     print(item['record_identifier'])
        worldcat_search_api_read_response = worldcat_search_api.read(record_identifier_list[0])
        # worldcat_search_api_read_response = worldcat_search_api.read(item['record_identifier'])
        print('Parse MARC record...')
        worldcat_author, worldcat_title, worldcat_publisher = parse_message.parse(worldcat_search_api_read_response)
        worldcat_results = parse_message.parse_detailed(worldcat_search_api_read_response)
        # item['worldcat_results'] = worldcat_results
        # record_identifier_dict_list.append(item)

        print('Searching for duplicates in Library Hub...')
        library_hub_api_response = library_hub_api.search_record(author=worldcat_author, title=worldcat_title, publisher=worldcat_publisher)
        print('Author: {}, Title: {}, Publisher: {}'.format(worldcat_author, worldcat_title, worldcat_publisher))
        print('Showing results...')
        library_hub_api_response = library_hub_api.show_results(library_hub_api_response)
    except:
        worldcat_results = {'No results': 'NA'}
        record_identifier_dict = {'No results': 'NA'}
        worldcat_author, worldcat_title, worldcat_publisher, library_hub_api_response = None, None, None, None

    print('Finished!')

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
                    'library_hub_api_response': library_hub_api_response,
                    'worldcat_results': worldcat_results})


@app.route('/visionStage2', methods=["POST"])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_visionStage2():
    print('Extracting text...')
    google_vision_api_response = request.get_json()['google_vision_api_response']
    print('Translating text...')
    google_translate_api_response = google_translate_api.translate_text(google_vision_api_response)
    try:
        print('Analyzing text...')
        google_natural_language_api_response = google_natural_language_api.analyze_entities(google_translate_api_response['translatedText'])
        author, title, date, publisher, publisher_place, meta_data = google_natural_language_api.retrieve_entities(google_natural_language_api_response)
    except:
        author, title, date, publisher, publisher_place, meta_data = None, None, None, None, None, None
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

    print('Finished!')

    return jsonify({'google_vision_api_response': google_vision_api_response,
                    'detectedSourceLanguage': google_translate_api_response['detectedSourceLanguage'],
                    'translatedText': google_translate_api_response['translatedText'],
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


@app.route('/visionStage3', methods=["POST"])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_visionStage3():
    google_translate_api_response = request.get_json()['translatedText']
    print(google_translate_api_response)
    try:
        print('Analyzing text...')
        google_natural_language_api_response = google_natural_language_api.analyze_entities(google_translate_api_response)
        author, title, date, publisher, publisher_place, meta_data = google_natural_language_api.retrieve_entities(google_natural_language_api_response)
    except:
        author, title, date, publisher, publisher_place, meta_data = None, None, None, None, None, None
    print('Running Open Search on WorldCat...')
    worldcat_search_api_open_search_response = worldcat_search_api.open_search(google_translate_api_response)
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

    print('Finished!')

    return jsonify({'author': author,
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
    app.run(port=4204)
