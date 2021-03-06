import io
import os
from google.cloud.vision import types, ImageAnnotatorClient


def detect_text(image_file, from_path=True):
    '''Detects and returns texts in image.

    :param path: string
    :return: string, string
    '''
    client = ImageAnnotatorClient()

    if from_path:
        with io.open(image_file, 'rb') as image_file:
            content = image_file.read()
    else:
        content = image_file.read()

    image = types.Image(content=content)

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
