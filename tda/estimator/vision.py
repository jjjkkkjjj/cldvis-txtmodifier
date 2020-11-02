from google.cloud import vision
import io, os

class Vision(object):
    def __init__(self, credentialJsonpath):
        # export GOOGLE_APPLICATION_CREDENTIALS as environmental path
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentialJsonpath

        self.client = vision.ImageAnnotatorClient()

    def detect_localImg(self, imgpath):

        with open(imgpath, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)

        response = self.client.text_detection(image=image)
        texts = response.text_annotaions
        vision.InputConfig()
        print('Texts:')

        for text in texts:
            print('\n"{}"'.format(text.description))

            vertices = (['({},{})'.format(vertex.x, vertex.y)
                         for vertex in text.bounding_poly.vertices])

            print('bounds: {}'.format(','.join(vertices)))

        if response.error.message:
            raise Exception(
                '{}\nFor more info on error messages, check: '
                'https://cloud.google.com/apis/design/errors'.format(
                    response.error.message))