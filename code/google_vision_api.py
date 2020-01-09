import io
import os
import config
from google.cloud import vision

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.GOOGLE_APPLICATION_CREDENTIALS_PATH


def detect_text(path):
    '''Detects and returns texts in image.

    :param path: string
    :return: string, string
    '''
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    # print_bounding_poly_vertices(texts)

    search_query = return_search_query(texts)

    return search_query


def print_bounding_poly_vertices(texts):
    '''Print bounding polygon vertices.

    :param texts: response from vision API
    :return: None
    '''
    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))


def return_search_query(texts):
    '''Concatenate texts found in image.

    :param texts: response.text_annotations from google vision API
    :return: string
    '''
    # results = []
    # for text in texts[1:]:
    #     results.append(text.description)
    # concatenated_results = " ".join(results)

    concatenated_results = texts[0].description.replace("\n", ", ").strip()

    return concatenated_results
