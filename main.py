import subprocess
import platform
import argparse
import shutil
import sys
import os

version = '1.0.0'
root_path = os.path.dirname(os.path.abspath(sys.argv[0]))


def finishing_update(folder_path):
    directory_exists = os.path.exists(folder_path)
    while directory_exists:
        try:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                directory_exists = False
        except PermissionError:
            directory_exists = True


parser = argparse.ArgumentParser()
parser.add_argument("--finishing_update", action='store_true', help="Finishing update argument")
parser.add_argument("--temp_directory", type=str, help="Temp directory")
parser.add_argument("--app_name", type=str, help="Open app name")
args = parser.parse_args()
temp_directory = args.temp_directory
app_name = args.app_name
if args.finishing_update:
    finishing_update(temp_directory)
    if platform.system() == 'Darwin':
        open_command = ['open', '-a', os.path.join(root_path + '/../../../', app_name + '.app')]
    elif platform.system() == 'Windows':
        open_command = [os.path.join(root_path, app_name) + '.exe']
    else:
        open_command = []
    if len(open_command) != 0:
        subprocess.Popen(open_command)
        sys.exit()
