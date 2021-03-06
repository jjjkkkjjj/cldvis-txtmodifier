
class English(object):
    
    ##### Common #####
    file = 'File'
    view = 'View'
    showing = 'Showing'
    entire = 'Entire'
    selected = 'Selected'
    prediction = 'Prediction'
    areamode = 'Area Mode'
    rectangle = 'Rectangle'
    quadrangle = 'Quadrangle'
    languagemode_list = ['English', 'Japanese']
    predmode_list = ['image', 'document']
    areamode_list = ['Rectangle', 'Quadrangle']
    filename = 'Filename'
    savename = 'Savename'
    text = 'Text'
    remove = 'Remove'
    cancel = 'Cancel'
    ok = 'OK'
    open = 'Open'

    ##### menu ######
    menu_file = '&File'
    menu_edit = '&Edit'
    menu_viewer = '&View'
    menu_prediction = '&Prediction'
    menu_help = '&Help'
    
    menu_action_openfolder = '&Open Folder'
    menu_action_openfiles = '&Open Files'
    menu_action_savetda = '&Save'
    menu_action_saveastda = '&Save as tda'
    menu_action_loadtda = '&Load tda'
    menu_action_backfile = '&Back File'
    menu_action_forwardfile = '&Forward File'
    menu_action_exportCSV = '&Export File'
    menu_action_exportDataset = '&Export Dataset'
    menu_action_exit = '&Exit'

    menu_action_undo = '&Undo'
    menu_action_redo = '&Redo'

    menu_action_zoomin = '&Zoom In'
    menu_action_zoomout = '&Zoom Out'
    menu_action_showentire = '&Show Entire Image'
    menu_action_showselected = '&Show Selected Image'

    menu_action_predict = '&Predict Table'
    menu_action_done = '&Done'
    menu_action_discard = '&Discard'
    menu_action_areaRectMode = '&Rectangle Mode'
    menu_action_areaQuadMode = '&Quadrangle Mode'
    menu_action_predictImageMode = '&Image mode'
    menu_action_predictDocumentMode = '&Document mode'

    menu_action_about = '&About'
    menu_action_preferences = '&Preferences'

    ##### preferences #####
    pref_title = 'Preferences'
    pref_basic = 'Basic Settings'
    pref_languagemode = 'Language:'
    pref_defaultareamode = 'Default Area mode:'
    pref_defaultpredmode = 'Default Prediction mode:'
    pref_readJsonpath = 'Read Json'
    pref_export = 'Export'
    pref_exportfileformat = 'Default File Format:'
    pref_exportSameRowY = 'Same Rows within:'
    pref_exportConcatColX = 'Concatenate Columns within:'
    pref_datasetformat = 'Dataset Format:'
    pref_datasetdir = 'Dataset Directory:'
    pref_notselected = 'Not selected'
    pref_jsonInvalidStatus = '{} is invalid'
    pref_openjsonfile = 'Open Credential Json File'
    pref_opendatasetdir = 'Open Dataset Directory to be exported'

    ##### dialog #####
    notification = 'Notification'
    appclosetext = 'Edited results has not saved yet.\nAre you sure to quit this application?'
    openfiles = 'Open Files'
    warning = 'Warning'
    notselectedtext = 'Not selected image files!!'
    opendir = 'Open Directory'
    existfiletext = '{} has already existed\nAre you sure to overwrite it?'
    exportfileas = 'Export a file as'
    saved = 'Saved'
    savedtotext = 'Saved to {}'
    opentdabinary = 'Open a TDA Binary File'
    discardallresults = 'Discard all results'
    discardallresultstext = 'Are you sure you want to discard all results?'
    discardarea = 'Discard selection'
    discardarreatext = 'Are you sure you want to discard selection area?'
    savedasdataset = 'Saved as dataset'
    savedasdatasettext = 'Saved to {} as {} format'
    exportdataset = 'Export a Dataset File'
    couldntpredict = 'Couldn\'t predict'
    couldntpredicttext = 'Couldn\'t predict texts.\nThe error code is\n{}'
    unexpectederror = 'Unexpected  Error'
    unexpectederrortext = 'Unexpected error was occurred.\nThe error code is\n{}'
    predictedtext = 'Predicted!\nThe results were saved in {}'
    setsavenametitle = 'Set default save filename'
    selectfilenametitle = 'Select a iamge filename'
    selectfilenametext = 'Current image filepath: {}'
    waitingtitle = 'Predicting'
    waitingtext = 'Now Predicting...'

    ##### Edit dialog #####
    edittext = 'Edit {}'

class Japanese(English):
    ##### Common #####
    file = 'ファイル'
    view = '表示'
    showing = '表示形式'
    entire = '全体'
    selected = '選択'
    prediction = '予測'
    areamode = '選択形式'
    rectangle = '長方形'
    quadrangle = '四角形'
    languagemode_list = ['英語', '日本語']
    predmode_list = ['画像', '文書']
    areamode_list = ['長方形', '四角形']
    filename = 'ファイル名'
    savename = '保存名'
    text = '文字'
    remove = '削除'
    cancel = 'キャンセル'
    ok = '完了'
    open = '開く'

    ##### menu #####
    menu_file = '&ファイル'
    menu_edit = '&編集'
    menu_viewer = '&表示'
    menu_prediction = '&予測'
    menu_help = '&ヘルプ'

    menu_action_openfolder = '&フォルダを開く'
    menu_action_openfiles = '&ファイルを開く'
    menu_action_savetda = '&保存'
    menu_action_saveastda = '&tdaファイルを名前を付けて保存'
    menu_action_loadtda = '&tdaファイルを読み込む'
    menu_action_backfile = '&前のファイルへ'
    menu_action_forwardfile = '&次のファイルへ'
    menu_action_exportCSV = '&表形式ファイルを出力'
    menu_action_exportDataset = '&データセットファイルを出力'
    menu_action_exit = '&終了'

    menu_action_undo = '&元に戻す'
    menu_action_redo = '&やり直す'

    menu_action_zoomin = '&拡大'
    menu_action_zoomout = '&縮小'
    menu_action_showentire = '&全体画像を表示'
    menu_action_showselected = '&選択画像を表示'

    menu_action_predict = '&予測'
    menu_action_done = '&編集を終了'
    menu_action_discard = '&破棄'
    menu_action_areaRectMode = '&長方形モード'
    menu_action_areaQuadMode = '&四角形モード'
    menu_action_predictImageMode = '&画像モード'
    menu_action_predictDocumentMode = '&文書モード'

    menu_action_about = '&cldvisについて'
    menu_action_preferences = '&設定'

    ##### preferences #####
    pref_title = '設定'
    pref_basic = '基本設定'
    pref_languagemode = '言語:'
    pref_defaultareamode = 'デフォルトの選択モード:'
    pref_defaultpredmode = 'デフォルトの予測モード:'
    pref_readJsonpath = 'Jsonを読み込む'
    pref_export = '出力'
    pref_exportfileformat = 'デフォルトの表形式ファイルフォーマット:'
    pref_exportSameRowY = '同じ行とみなす範囲:'
    pref_exportConcatColX = '文字列を結合する範囲:'
    pref_datasetformat = 'データセットフォーマット:'
    pref_datasetdir = 'データセットを保存するフォルダ:'


    pref_notselected = '未選択'
    pref_jsonInvalidStatus = '{}は無効なパスです'
    pref_openjsonfile = 'Json鍵ファイルを開く'
    pref_opendatasetdir = '開く'

    ##### dialog #####
    notification = '通知'
    appclosetext = '編集したものが保存されていません．\nこのアプリを閉じますか？'
    openfiles = 'ファイルを開く'
    warning = '警告'
    notselectedtext = '画像ファイルが選択されていません！'
    opendir = 'フォルダを開く'
    existfiletext = '{}は既に存在しています．\n上書きしますか？'
    exportfileas = 'ファイル出力'
    saved = '保存しました'
    savedtotext = '{}に保存しました'
    opentdabinary = 'TDAバイナリファイルを開く'
    discardallresults = '全ての結果の破棄'
    discardallresultstext = '全ての結果を破棄しますか？'
    discardarea = '選択エリアの破棄'
    discardarreatext = '選択エリアを破棄しますか？'
    savedasdataset = 'データセットとして保存'
    savedasdatasettext = '{}に{}フォーマットで保存しました．'
    exportdataset = 'データセットファイルを出力'
    couldntpredict = '予測不可'
    couldntpredicttext = '文字を予測できませんでした．\nエラーコードは以下の通りです．\n{}'
    unexpectederror = '予期せぬエラー'
    unexpectederrortext = '予期せぬエラーが発生しました．\nエラーコードは以下の通りです．\n{}'
    predictedtext = '予測しました！\n結果は{}に保存されています．'
    setsavenametitle = '保存名の設定'
    selectfilenametitle = '画像ファイルの選択'
    selectfilenametext = '現在の画像ファイルのパス: {}'
    waitingtitle = '予測中'
    waitingtext = '予測中...'

    ##### Edit dialog #####
    edittext = '\'{}\'の編集'