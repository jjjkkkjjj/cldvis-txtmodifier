import numpy as np
from lxml import etree
from ..utils.modes import ShowingMode, AreaMode
from ..utils.funcs import cvimread_unicode
import os, cv2

def parse_annotations_forFile_basedTopLeft(model):
    from ..model import Model
    model: Model
    polys = np.array([anno.pts for anno in model.annotations], dtype=int)
    texts = np.array([anno.text for anno in model.annotations])

    ret = []
    while polys.shape[0] > 0:
        # target_poly: shape = (1, points_num, 2=(x, y))
        # target_text: shape = (1,)
        target_poly = polys[:1]
        target_text = texts[:1]

        # polys: shape = (cand_num, points_num, 2=(x, y))
        # texts: shape = (cand_num,)
        polys = polys[1:]
        texts = texts[1:]

        # extract the values with top-left y within the error for target_poly's one
        # shape = (cand_num,)
        line_bindices = np.abs(polys[:, 0, 1] - target_poly[:, 0, 1]) < model.config.export_sameRowY

        # line_polys: shape = (column_num, points_num, 2=(x,y))
        # line_texts: shape = (column_num,)
        line_polys = np.concatenate((target_poly, polys[line_bindices]), axis=0)
        line_texts = np.concatenate((target_text, texts[line_bindices]), axis=0)

        polys = polys[np.logical_not(line_bindices)]
        texts = texts[np.logical_not(line_bindices)]
        if polys.shape[0] == 0:
            break

        # sort top-left x with ascending order
        tlx_indices = np.argsort(line_polys[:, 0, 0])
        line_polys = np.take(line_polys, tlx_indices, axis=0)
        line_texts = np.take(line_texts, tlx_indices, axis=0)

        row = []
        while line_polys.shape[0] > 0:

            column_text = line_texts[0]

            # extract the values with top-left x(min) within the error for target_poly's maximum x
            concat_index = 1
            for r_index in range(1, line_polys.shape[0]):
                left_poly_maxX = line_polys[r_index - 1, :, 0].max()
                right_poly_minX = line_polys[r_index, :, 0].min()
                if np.abs(left_poly_maxX - right_poly_minX) < model.config.export_sameColX:
                    concat_index = r_index + 1
                    column_text += line_texts[r_index]
                else:
                    break

            # update
            line_polys = line_polys[concat_index:]
            line_texts = line_texts[concat_index:]

            row += [column_text]
        ret += [row]

    return ret

def parse_annotations_forFile_basedCentroid(model):
    from ..model import Model
    model: Model
    polys = np.array([anno.pts for anno in model.annotations], dtype=int)
    texts = np.array([anno.text for anno in model.annotations])
    centroids = polys.mean(axis=1)

    ret = []
    while polys.shape[0] > 0:
        # sort centroids' y with ascending order, shape = (points_num,)
        cy_indices = np.argsort(centroids[:, 1])
        # sort
        polys = np.take(polys, cy_indices, axis=0)
        texts = np.take(texts, cy_indices, axis=0)
        centroids = np.take(centroids, cy_indices, axis=0)

        # target_poly: shape = (1, points_num, 2=(x, y))
        # target_text: shape = (1,)
        # target_centroids: shape = (1, 2)
        target_poly = polys[:1]
        target_text = texts[:1]
        target_centroids = centroids[:1]

        # polys: shape = (cand_num, points_num, 2=(x, y))
        # texts: shape = (cand_num,)
        # centroids: shape = (cand_num, 2)
        polys = polys[1:]
        texts = texts[1:]
        centroids = centroids[1:]

        # extract the values with top-left y within the error for target_poly's one
        # shape = (cand_num,)
        line_bindices = np.abs(centroids[:, 1] - target_centroids[:, 1]) < model.config.export_sameRowY

        # line_polys: shape = (column_num, points_num, 2=(x,y))
        # line_texts: shape = (column_num,)
        line_polys = np.concatenate((target_poly, polys[line_bindices]), axis=0)
        line_texts = np.concatenate((target_text, texts[line_bindices]), axis=0)

        polys = polys[np.logical_not(line_bindices)]
        texts = texts[np.logical_not(line_bindices)]
        centroids = centroids[np.logical_not(line_bindices)]
        if polys.shape[0] == 0:
            break

        # sort top-left x with ascending order
        tlx_indices = np.argsort(line_polys[:, 0, 0])
        line_polys = np.take(line_polys, tlx_indices, axis=0)
        line_texts = np.take(line_texts, tlx_indices, axis=0)

        row = []
        while line_polys.shape[0] > 0:

            column_text = line_texts[0]

            # extract the values with top-left x(min) within the error for target_poly's maximum x
            concat_index = 1
            for r_index in range(1, line_polys.shape[0]):
                left_poly_maxX = line_polys[r_index - 1, :, 0].max()
                right_poly_minX = line_polys[r_index, :, 0].min()
                if np.abs(left_poly_maxX - right_poly_minX) < model.config.export_sameColX:
                    concat_index = r_index + 1
                    column_text += line_texts[r_index]
                else:
                    break

            # update
            line_polys = line_polys[concat_index:]
            line_texts = line_texts[concat_index:]

            row += [column_text]
        ret += [row]

    return ret

def parse_annotations_forVOC(model, imgpath):
    """
    Parameters
    ----------
    model: Model

    imgpath: str
        the annotated image file path.
        Note that this file must be saved before calling this function.

    Returns
    -------
    str:
        the xml string

    """
    from ..model import Model
    model: Model
    polys = np.array([anno.pts for anno in model.annotations], dtype=int)
    texts = np.array([anno.text for anno in model.annotations])

    def _subelement(el, name, value=None):
        subel = etree.SubElement(el, name)
        if value:
            subel.text = str(value)
        return subel

    imgname = os.path.basename(imgpath)
    img = cvimread_unicode(imgpath)
    h, w, c = img.shape

    root = etree.Element('annotation')
    # folder
    folderET = _subelement(root, 'folder', 'image')
    # filename
    filenameET = _subelement(root, 'filename', imgname)

    # size
    sizeET = _subelement(root, 'size', None)

    # width
    widthET = _subelement(sizeET, 'width', w)
    # height
    heightET = _subelement(sizeET, 'height', h)
    # depth
    depthET = _subelement(sizeET, 'depth', c)

    for b in range(polys.shape[0]):
        # object
        objectET = _subelement(root, 'object', None)

        # difficult
        difficultET = _subelement(objectET, 'difficult', '0')
        # content
        contentET = _subelement(objectET, 'content', '###')
        # name
        nameET = _subelement(objectET, 'name', texts[b])

        # bndbox
        bndboxET = etree.SubElement(objectET, 'bndbox')
        for q in range(polys[b].shape[0]):
            xET = _subelement(bndboxET, 'x{}'.format(q + 1), polys[b, q, 0])
            yET = _subelement(bndboxET, 'y{}'.format(q + 1), polys[b, q, 1])

    return etree.tostring(root, pretty_print=True, encoding='utf-8')
