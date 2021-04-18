import numpy as np

def parse_annotations_forFile(model):
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