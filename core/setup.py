import os
import subprocess
import sys
from definitions import ROOT_DIR
settings = ROOT_DIR+"\\settings.txt"

_string = "pip install -r requirements.txt"

def setup():
    try:
        file = open(settings, 'r')
        string = file.readline().split("==")[-1].replace("\n","")
        file.close()
        if string.lower() == "false":
            install()
    except:
        install()

def install():
    subprocess.call(_string.replace("-r ", f"-r {ROOT_DIR}\\"))
    file = open(settings, 'w')
    file.write("requirements_installed==True")
    file.close()

def _write_batch():
    path = ROOT_DIR+"\\setup.bat"
    python_path = sys.executable
    script_path = os.path.abspath(__file__)
    string = f"@echo off\n{python_path} {script_path}"
    print(1)

def test():
    print('test')
    python_path = sys.executable
    script_path = ROOT_DIR+"\\core\\setup.py"
    subprocess.call(f"{python_path} {script_path}")

if __name__ == "__main__":
    setup()