import sys
import os
import platform
import subprocess
import argparse
import zipfile
import shutil
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QProgressBar,
    QMessageBox,
    QWidget
)

# Version
version = '1.0.1.0'
is_debug = True

root_path = os.path.dirname(os.path.abspath(sys.argv[0]))


def remove_old_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if filename in ignore_files:
            continue
        elif os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def extract_zip_file():
    progress_bar.setValue(0)
    zip_file = zipfile.ZipFile(update_file_path)
    files = zip_file.namelist()
    text_label.setText("Updating... Please, wait.")
    for i, file in enumerate(files, start=1):
        zip_file.extract(file, path=destination_path)
        progress_bar.setValue(i / len(files) * 100)
        app.processEvents()
    zip_file.close()


def update_progress_bar(progress_bar_example, value):
    progress_bar_example.setValue(value)
    app.processEvents()


def copy2_with_progress(src, dst, *, follow_symlinks=True):
    shutil.copy2(src, dst, follow_symlinks=follow_symlinks)
    update_progress_bar(progress_bar, progress_bar.value() + 1)


def install_from_dmg():
    text_label.setText("Installing updates...")
    progress_bar.setValue(0)
    app.processEvents()
    mount_cmd = ['hdiutil', 'attach', update_file_path, '-nobrowse', '-noverify', '-noautoopen']
    mount_output = subprocess.check_output(mount_cmd, stderr=subprocess.STDOUT).decode('utf-8')
    mount_point = os.path.dirname(update_file_path)

    # Extract the mount point from the output
    for line in mount_output.split('\n'):
        if 'Volumes' in line:
            mount_point = line.split('\t')[-1]
            break
    app.processEvents()

    # Copy all files from the mounted volume to the destination directory
    shutil.copytree(mount_point, destination_path, symlinks=False, dirs_exist_ok=True,
                    copy_function=copy2_with_progress,
                    ignore=shutil.ignore_patterns('.DS_Store', '.VolumeIcon.icns'))
    app.processEvents()

    # Unmount the .dmg file
    subprocess.run(['hdiutil', 'detach', mount_point, '-force'])


def preparing_for_update():
    if platform.system() == 'Darwin':
        # Some "hack" to request access to the user storage on start
        os.listdir()


def install_update():
    text_label.setText("Start of the update...")
    progress_bar.setValue(0)
    app.processEvents()
    # Skip removing files if not compiled
    if getattr(sys, 'frozen', False):
        remove_old_files(destination_path)
    if update_file_path[update_file_path.rfind(".") + 1:] == 'dmg':
        # Install from dmg
        install_from_dmg()
    else:
        # Extract zip
        extract_zip_file()


def finishing_the_update():
    text_label.setText("The update is complete.")
    if platform.system() == 'Darwin':
        extras_path = os.path.join(destination_path, app_name + '.app') + '/Contents/Resources/Extras'
    else:
        extras_path = os.path.join(destination_path, 'Extras.exe')
    open_command = [extras_path,
                    '--finishing_update',
                    '--temp_directory', os.path.dirname(update_file_path),
                    '--app_name', app_name]
    QMessageBox.information(
        QWidget(),
        "Updater",
        "Update finished.\nThe program will be opened automatically."
    )
    subprocess.Popen(open_command)
    sys.exit()


# Getting arguments
parser = argparse.ArgumentParser(description='This is a simple Updater for Python programs.')
parser.add_argument('--path', type=str, help='Path to downloaded file.')
parser.add_argument('--app_name', type=str, help='App name')
parser.add_argument('--destination_path', type=str, help='Path to your program.')
parser.add_argument(
    '--ignore_files',
    metavar='file',
    type=str,
    nargs='+',
    help='File names that the program will ignore when updating.'
)
args = parser.parse_args()

# Variables
app_name = args.app_name
update_file_path = args.path
destination_path = args.destination_path
ignore_files = [] + args.ignore_files if args.ignore_files is not None else []
if None not in (update_file_path, destination_path):
    # Creating window
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("Updater")
    window.setFixedSize(500, 100)
    central_widget = QWidget()
    window.setCentralWidget(central_widget)
    layout = QVBoxLayout(central_widget)
    text_label = QLabel("Updating... Please, wait.")
    layout.addWidget(text_label)
    progress_bar = QProgressBar()
    layout.addWidget(progress_bar)
    window.show()

    # Current executable file name
    executable_file_name = os.path.basename(sys.executable)
    if platform.system() == 'Darwin':
        executable_file_name = executable_file_name + '.app'
    ignore_files = ignore_files + [executable_file_name]

    # Prepare
    preparing_for_update()

    # Update
    install_update()

    # Finish
    finishing_the_update()

    app.exec()
    sys.exit(app.exec())
