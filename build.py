# Tools for build
import PyInstaller.__main__
import pyinstaller_versionfile
from main import version
import platform
import shutil
import os

# Variables
app_name = "Extras"
app_description = "Extras for SmartDatabase."

folders_to_remove = ('dist', 'build')
for item in folders_to_remove:
    if os.path.exists(item):
        shutil.rmtree(item)

if platform.system() == 'Windows':
    # Make version file for exe
    pyinstaller_versionfile.create_versionfile(
        output_file="version_file.txt",
        version=version,
        file_description=app_description,
        internal_name=app_name,
        original_filename=app_name + ".exe",
        product_name=app_name,
        translations=[1033, 1252, 1251]
    )

# Build application
PyInstaller.__main__.run([
    'main.spec'
])
