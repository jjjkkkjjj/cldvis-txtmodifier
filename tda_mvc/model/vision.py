from google.cloud import vision
from google.cloud import documentai_v1beta2 as documentai
import io, os, json, cv2

from .base import ModelAbstractMixin

class VisionModelMixin(ModelAbstractMixin):
    client: vision.ImageAnnotatorClient
    results: dict

    def __init__(self):
        self.client = None
        self.results = {}

    @property
    def credentialJsonpath(self):
        return self.config.credentialJsonpath

    @property
    def isExistCredPath(self):
        return self.config.credentialJsonpath is not None


    def set_credentialJsonpath(self, path):
        # export GOOGLE_APPLICATION_CREDENTIALS as environmental path
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = path

        self.client = vision.ImageAnnotatorClient()
        self.config.credentialJsonpath = path
        self.results = {}

    def detect_localImg(self, imgpath):

        with open(imgpath, 'rb') as image_file:
            content = image_file.read()

        h, w, _ = cv2.imread(imgpath).shape
        h, w = float(h), float(w)
        image = vision.Image(content=content)
        # https://googleapis.dev/python/vision/1.0.0/gapic/v1/api.html#google.cloud.vision_v1.ImageAnnotatorClient.document_text_detection
        response = self.client.document_text_detection(image=image)  # type is AnnotateImageResponse
        texts = response.text_annotations  # EntityAnnotation sequence
        vision.InputConfig()

        """
        texts will be list of Product which is a predicted result
        See https://googleapis.dev/python/vision/latest/vision_v1/types.html for more details
        text
            description: str, predicted text
            bounding_poly: A bounding annotation for the detected image annotation.
                vertices: vertex sequence
                    x: int
                    y: int
                normalized_vertices: normalized vertex sequence
                    x: float
                    y: float

        """
        results = {}
        prediction = []

        # print('Texts:')
        for text in texts:
            ret = {}
            ret['text'] = text.description
            ret['bbox'] = [[vertex.x / w, vertex.y / h] for vertex in text.bounding_poly.vertices]
            prediction += [ret]
            """
            print('\n"{}"'.format(text.description))

            vertices = (['({},{})'.format(vertex.x, vertex.y)
                         for vertex in text.bounding_poly.vertices])

            print('bounds: {}'.format(','.join(vertices)))
            """
        results["info"] = {"width": int(w), "height": int(h), "path": imgpath}
        results["prediction"] = prediction

        # save results as json file
        with open(os.path.join('.', '.tda', 'tmp', 'result.json'), 'w') as f:
            json.dump(results, f)

        if response.error.message:
            raise PredictError(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))

        self.results = results
        return results

    def detect_localTable(self):
        pass

    # def select_prediction(self, index):
    #    pass


class PredictError(Exception):
    pass