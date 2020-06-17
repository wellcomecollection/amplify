import config
import parse_message
import google_vision_api
import google_translate_api
import google_natural_language_api
import library_hub_api
import worldcat_search_api
import abim_search_api
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin


app = Flask(__name__)

app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/visionStage1": {"origins": "http://localhost:4204"}, r"/post_vision": {"origins": "http://localhost:4204"}})


@app.route('/visionStage1', methods=["POST"])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def get_visionStage1():
    image = request.files['image']
    # img_loc = config.IMAGE_PATH[0]
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
    try:
        print('Retrieving record identifiers from WorldCat Open Search response...')
        record_identifier_dict = parse_message.get_record_identifiers(worldcat_search_api_open_search_response)
    except:
        record_identifier_dict = [{'record_identifier': 'No results', 'title': 'No results'}]

    print('Finished!')

    return jsonify({'google_vision_api_response': google_vision_api_response,
                    'detectedSourceLanguage': google_translate_api_response['detectedSourceLanguage'],
                    'translatedText': google_translate_api_response['translatedText'],
                    # 'img_loc': img_loc,
                    'author': author,
                    'title': title,
                    'date': date,
                    'publisher': publisher,
                    'publisher_place': publisher_place,
                    'meta_data': meta_data,
                    'record_identifier_dict': record_identifier_dict
                    })


@app.route('/library_hub_search', methods=["POST"])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def library_hub_search():
    worldcat_results = request.get_json()
    author = ''
    title = ''
    publisher = ''

    for row in worldcat_results:
        try:
            if row['tag'] == '245':
                if row['code'] == 'a':
                    print('Title: ' + row['subfield'])
                    title = row['subfield']
                elif row['code'] == 'c':
                    print('Author: ' + row['subfield'])
                    author = row['subfield']
            elif row['tag'] == '264' or row['tag'] == '260':
                if row['code'] == 'b':
                    print('Publisher: ' + row['subfield'])
                    publisher = row['subfield']
        except:
            pass

    try:
        print('Searching for duplicates in Library Hub...')
        library_hub_api_response = library_hub_api.search_record(author=author, title=title, publisher=publisher)
        print('Showing results...')
        library_hub_api_response = library_hub_api.show_results(library_hub_api_response)
    except:
        library_hub_api_response = None

    return jsonify({'library_hub_api_response': library_hub_api_response})


@app.route('/abim_search', methods=["POST"])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def abim_search():
    author = request.get_json()['author']
    title = request.get_json()['title']
    publisher = request.get_json()['publisher']
    date = request.get_json()['date']

    response = abim_search_api.search_record(author=author, title=title, publisher=publisher, date=date)

    results = abim_search_api.parse_response(response)

    print('Running Open Search on WorldCat...')
    worldcat_search_api_open_search_response = worldcat_search_api.open_search(abim_search_api.format_search_string(title))

    print('Retrieving record identifiers from WorldCat Open Search response...')
    record_identifier_dict = parse_message.get_record_identifiers(worldcat_search_api_open_search_response)

    print('Finished!')

    return jsonify({'abim_results': results,
                    'record_identifier_dict': record_identifier_dict,})


@app.route('/abim_search_detailed', methods=["POST"])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def abim_search_detailed():
    link = request.get_json()['link']

    results = abim_search_api.pull_details(link=link)

    return jsonify({'abim_results_detailed': results})


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
    record_identifier_dict = parse_message.get_record_identifiers(worldcat_search_api_open_search_response)
    print('Retrieving individual MARC record XML from WorldCat Read endpoint...')

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
                    'record_identifier_dict': record_identifier_dict
                    })


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
    record_identifier_dict = parse_message.get_record_identifiers(worldcat_search_api_open_search_response)
    print('Retrieving individual MARC record XML from WorldCat Read endpoint...')

    print('Finished!')

    return jsonify({'author': author,
                    'title': title,
                    'date': date,
                    'publisher': publisher,
                    'publisher_place': publisher_place,
                    'meta_data': meta_data,
                    'record_identifier_dict': record_identifier_dict
                    })


if __name__ == "__main__":
    app.run(port=4204)
