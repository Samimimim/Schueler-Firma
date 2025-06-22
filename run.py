import sys
import os

# Prüfen, ob im venv
if sys.prefix == sys.base_prefix:
    venv_python = os.path.join("venv", "Scripts", "python.exe") if os.name == "nt" else os.path.join("venv", "bin", "python")
    os.execv(venv_python, [venv_python] + sys.argv)

from app import main

if __name__ == '__main__':
    main.app.run(host='0.0.0.0',debug=True, port=5000)
