import tempfile
import shutil
import venv
import subprocess
from os.path import join
import sys

def figdate_wrap():
    path = tempfile.mkdtemp()
    venv.create(path, with_pip=True)
    subprocess.run([join(path, 'bin', 'pip'), 'install', 'pyfiglet'])
    subprocess.run([join(path, 'bin', 'python3'), '-m', 'figdate', *sys.argv[1:]])
    shutil.rmtree(path)
