from google.cloud import vision
import io, os, json

class Vision(object):
    def __init__(self, credentialJsonpath):
        # export GOOGLE_APPLICATION_CREDENTIALS as environmental path
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentialJsonpath

        self.client = vision.ImageAnnotatorClient()

    def detect_localImg(self, imgpath):

        with open(imgpath, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

        response = self.client.text_detection(image=image) # type is AnnotateImageResponse
        texts = response.text_annotations # EntityAnnotation sequence
        vision.InputConfig()

        """
        texts will be list of Product which is a predicted result
        See https://googleapis.dev/python/vision/latest/vision_v1/types.html for more details
        text
            description: str, predicted text
            bounding_poly: A bounding polygon for the detected image annotation.
                vertices: vertex sequence
                    x: int
                    y: int
                normalized_vertices: normalized vertex sequence
                    x: float
                    y: float
                
        """
        results = []

        # print('Texts:')
        for text in texts:
            ret = {}
            ret['text'] = text.description
            ret['bbox'] = [[vertex.x, vertex.y] for vertex in text.bounding_poly.vertices]
            results += [ret]
            """
            print('\n"{}"'.format(text.description))

            vertices = (['({},{})'.format(vertex.x, vertex.y)
                         for vertex in text.bounding_poly.vertices])

            print('bounds: {}'.format(','.join(vertices)))
            """
        # save results as json file
        with open(os.path.join('.', '.tda', 'tmp', 'result.json'), 'w') as f:
            json.dump(results, f)

        if response.error.message:
            raise PredictError(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        return results

class PredictError(Exception):
    pass