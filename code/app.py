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
    print(record_identifier_dict)

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


@app.route('/abim_search', methods=["POST"])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def abim_search():
    author = request.get_json()['author']
    title = request.get_json()['title']
    publisher = request.get_json()['publisher']
    date = request.get_json()['date']

    response = abim_search_api.search_record(author=author, title=title, publisher=publisher, date=date)

    results = abim_search_api.parse_response(response)

    print(results)

    # results = [{'document': '1. Reddy, A. Madhusudana and&#13;\nB. Ravi Prasad Rao\n  \n\n(2011)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/62735/"><em>Medicinal plant wealth of Palakonda hill ranges, Kadapa district, Andhra Pradesh, India.    '}, {'document': '2. Chakre, Onkar J.\n  \n\n(2010)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/55569/"><em>The Wealth of India -- a CSIR\'s encyclopaedia of information resource on economic plants, animals and minerals.    '}, {'document': '3. Mao, A.A.,&#13;\nT.M. Hynniewta and&#13;\nM. Sanjappa\n  \n\n(2009)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/50755/"><em>Plant wealth of Northeast India with reference to ethnobotany.    '}, {'document': '4. Ratha Krishnan, P. and&#13;\nM. Paramathma\n  \n\n(2009)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/53872/"><em>Potentials and Jatropha species wealth of India.    '}, {'document': '5. Wealth of India\n  \n\n(2009)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/53919/"><em>The wealth of India -- A dictionary of Indian raw materials and industrial products -- Second Supplement Series (Raw Materials), Vol. 3: Pi--Z.    '}, {'document': '6. Bhutani, K.K.\n  \n\n(2008)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/52190/"><em>Herbal wealth of North-East India -- A pictorial and herbaria guide.    '}, {'document': '7. Bhutani, K.K., compiled and edited by, assisted by Alok Goyal and Naresh Rajput\n  \n\n(2008)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/52189/"><em>Herbal wealth of North-East India -- Database and appraisal.    '}, {'document': '8. Brown, J. Coggin et al.\n  \n\n(2008)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/50688/"><em>Mineral wealth: a guide to the occurrences and economics of the useful minerals of India, Pakistan and Burma.    '}, {'document': '9. Pattanaik, Chiranjibi and&#13;\nC. Sudhakar Reddy\n  \n\n(2008)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/50901/"><em>Medicinal plant wealth of local communities in Kuldiha Wildlife Sanctuary, Orissa, India.    '}, {'document': '10. Wealth of India\n  \n\n(2006)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/51154/"><em>The wealth of India -- A dictionary of Indian raw materials and industrial products -- Second Supplement Series (Raw Materials), volume 1: A--F, volume 2: G--Ph.    '}, {'document': '11. Parinitha, Mahishi, B.H. Srinivasa and M.B. Shivanna\n  \n\n(2005)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/17522/"><em>Medicinal plant wealth of local communities in some villages in Shimoga District of Karnataka, India.    '}, {'document': '12. Rajan, G. Baskar, Irfan Ali Khan and Atiya Khanum\n  \n\n(2005)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/14394/"><em>Strength and wealth of therapeutic medicinal plants in India.    '}, {'document': '13. Masih, S.K.\n  \n\n(2003)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/74901/"><em>Diversity of ethnomedicinal wealth in Amar Kantak plateau region (India).    '}, {'document': '14. Rani, S.S.,&#13;\nK.S.R. Murthy,&#13;\nP.S.P. Goud and &#13;\nT. Pullaiah\n  \n\n(2003)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/62348/"><em>Tree wealth in the life and economy of the tribespeople of Andhra Pradesh, India.    '}, {'document': '15. Pande, Rohini P. and Abdo S. Yazbeck\n  \n\n(2002)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/16916/"><em>What\'s in a country average? -- Wealth, gender, and regional inequalities in immunization in India.    '}, {'document': '16. Raju, R.A.\n  \n\n(1997)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/14528/"><em>Forest wealth of India.    '}, {'document': '17. Mahato, A.K., P. Mahato and K. Prasad\n  \n\n(1996)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/22742/"><em>Ethnobotanical wealth of Chota Nagpur plateau of India, part III: some medicinal plants used against diarrhoea by people of Singhdhum district, Bihar.    '}, {'document': '18. Singh, K.K. and A. Prakash\n  \n\n(1994)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/9688/"><em>Tree wealth in the life and economy of the tribals of Uttar Pradesh, India.    '}, {'document': '19. Prasad, R. and R.K. Pandey\n  \n\n(1987)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/18810/"><em>Survey of medicinal wealth of Central India.    '}, {'document': '20. Majupuria, Trilok Chandra (Ed.)\n  \n\n(1986)\n\n<a href="http://indianmedicine.eldoc.ub.rug.nl/23120/"><em>Wildlife wealth of India (Resources and management).    '}]

    print('Finished!')

    return jsonify({'abim_results': results})


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
