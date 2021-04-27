
class English(object):
    def __init__(self):
        # leftdock
        self.leftdock_file = 'File'
        self.leftdock_view = 'View'
        self.leftdock_showing = 'Showing'
        self.leftdock_entire = 'Entire'
        self.leftdock_selected = 'Selected'
        self.leftdock_prediction = 'Prediction'
        self.leftdock_areamode = 'Area Mode'
        self.leftdock_rectangle = 'Rectangle'
        self.leftdock_quadrangle = 'Quadrangle'
        self.leftdock_predmode = ['image', 'document']

    notification = 'Notification'
    closetext = 'Edited results has not saved yet.\nAre you sure to quit this application?'

class Japanese(English):
    def __init__(self):
        super().__init__()
        self.leftdock_file = 'ファイル'
        self.leftdock_view = '表示'
        self.leftdock_showing = '表示形式'
        self.leftdock_entire = '全体'
        self.leftdock_selected = '選択'
        self.leftdock_prediction = '予測'
        self.leftdock_areamode = '選択形式'
        self.leftdock_rectangle = '長方形'
        self.leftdock_quadrangle = '四角形'
        self.leftdock_predmode = ['画像', '文書']