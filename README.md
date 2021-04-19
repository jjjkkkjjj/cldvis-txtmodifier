# Cloud Vision Text Modifier
This GUI App allows us to modify results predicted by Google cloud vision OCR.

# Installation
Set up cloud vision api settings following [official](https://cloud.google.com/vision/docs/quickstart-client-libraries).


```
conda install -c conda-forge pyside2 opencv matplotlib pandas openpyxl lxml
pip install --upgrade google-cloud-vision
pip install --upgrade google-cloud-documentai
```

# For developer

## Installation
```
pip install Pyside2 opencv-python pandas openpyxl lxml pyinstaller
pip install --upgrade google-cloud-vision
pip install --upgrade google-cloud-documentai
```

Or

```
pip install -f requirements.txt
pip install pyinstaller
```

## build

```buildoutcfg
cd exe
pyinstaller cldvis.spec
```

or simply double-click `windows.bat` in `exe

If you catch `pkg_resources.DistributionNotFound: The 'google-cloud-core' distribution was not found and is required by the application`
, you should try to reisntall `google-cloud-core`!


```buildoutcfg
cd ~~/site-packages/Pyinstaller/hooks
vi hook-google-cloud.py
```

```buildoutcfg
pip install google-cloud-core
```