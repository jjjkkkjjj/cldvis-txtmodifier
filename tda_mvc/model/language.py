
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

        # menu
        self.menu_file = '&File'
        self.menu_viewer = '&View'
        self.menu_prediction = '&Prediction'
        self.menu_help = '&Help'
        
        self.menu_action_openfolder = '&Open Folder'
        self.menu_action_openfiles = '&Open Files'
        self.menu_action_savetda = '&Save'
        self.menu_action_saveastda = '&Save as tda'
        self.menu_action_loadtda = '&Load tda'
        self.menu_action_backfile = '&Back File'
        self.menu_action_forwardfile = '&Forward File'
        self.menu_action_exportCSV = '&Export File'
        self.menu_action_exportDataset = '&Export Dataset'
        self.menu_action_exit = '&Exit'

        self.menu_action_zoomin = '&Zoom In'
        self.menu_action_zoomout = '&Zoom Out'
        self.menu_action_showentire = '&Show Entire Image'
        self.menu_action_showselected = '&Show Selected Image'

        # prediction menu
        self.menu_action_predict = '&Predict Table'
        self.menu_action_done = '&Done'
        self.menu_action_discard = '&Discard'
        self.menu_action_areaRectMode = '&Rectangle Mode'
        self.menu_action_areaQuadMode = '&Quadrangle Mode'
        self.menu_action_predictImageMode = '&Image mode'
        self.menu_action_predictDocumentMode = '&Document mode'

        # help menu
        self.menu_action_about = '&About'
        self.menu_action_preferences = '&Preferences'

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

        # menu
        self.menu_file = '&ファイル'
        self.menu_viewer = '&表示'
        self.menu_prediction = '&予測'
        self.menu_help = '&Help'

        self.menu_action_openfolder = '&フォルダを開く'
        self.menu_action_openfiles = '&ファイルを開く'
        self.menu_action_savetda = '&保存'
        self.menu_action_saveastda = '&tdaファイルを名前を付けて保存'
        self.menu_action_loadtda = '&tdaファイルを読み込む'
        self.menu_action_backfile = '&前のファイルへ'
        self.menu_action_forwardfile = '&次のファイルへ'
        self.menu_action_exportCSV = '&表形式ファイルを出力'
        self.menu_action_exportDataset = '&データセットファイルを出力'
        self.menu_action_exit = '&終了'

        self.menu_action_zoomin = '&拡大'
        self.menu_action_zoomout = '&縮小'
        self.menu_action_showentire = '&全体画像を表示'
        self.menu_action_showselected = '&選択画像を表示'

        # prediction menu
        self.menu_action_predict = '&予測'
        self.menu_action_done = '&編集を終了'
        self.menu_action_discard = '&破棄'
        self.menu_action_areaRectMode = '&長方形モード'
        self.menu_action_areaQuadMode = '&四角形モード'
        self.menu_action_predictImageMode = '&画像モード'
        self.menu_action_predictDocumentMode = '&文書モード'

        # help menu
        self.menu_action_about = '&cldvisについて'
        self.menu_action_preferences = '&設定'