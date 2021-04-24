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
```bash
pip install Pyside2 opencv-python pandas openpyxl lxml pyinstaller
pip install --upgrade google-cloud-vision
pip install --upgrade google-cloud-documentai
```

Or

```bash
pip install -f requirements.txt
pip install pyinstaller
```

## build

```bash
cd exe
pyinstaller cldvis.spec
```

or simply double-click `windows.bat` in `exe

## debug
When you want to debug the exe created by Pyinstaller, you should call exe from command line like this;

```bash
cd exe
pyinstaller cldvis-debug.spec
dist\cldviscldvis.exe
```

you can see the log outputs;

```bash
...
[13560] LOADER: extracted pyimod02_archive
[13560] LOADER: callfunction returned...
[13560] LOADER: extracted pyimod03_importers
[13560] LOADER: callfunction returned...
[13560] LOADER: Installing PYZ archive with Python modules.
[13560] LOADER: PYZ archive: PYZ-00.pyz
[13560] LOADER: Running pyiboot01_bootstrap.py
[13560] LOADER: Running pyi_rth_pyside2.py
[13560] LOADER: Running pyi_rth_pkgres.py
[13560] LOADER: Running pyi_rth_certifi.py
[13560] LOADER: Running pyi_rth_multiprocessing.py
[13560] LOADER: Running app_mvc.py
...
```

## trouble shooting
### `pkg_resources.DistributionNotFound: The 'google-cloud-core' distribution was not found and is required by the application`
If you catch `pkg_resources.DistributionNotFound: The 'google-cloud-core' distribution was not found and is required by the application`
, you should try to reisntall `google-cloud-core`!

```bash
pip install google-cloud-core
```

or, set hook.

```bash
cd ~~/site-packages/Pyinstaller/hooks
vi hook-google-cloud.py
```

### `Exception ignored in: 'grpc._cython.cygrpc.ssl_roots_override_callback'

```bash
Exception ignored in: 'grpc._cython.cygrpc.ssl_roots_override_callback'
E0424 14:05:13.995000000  7832 src/core/lib/security/security_connector/ssl_utils.cc:555] assertion failed: pem_root_certs != nullptr
```
