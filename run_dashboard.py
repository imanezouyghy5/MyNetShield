import sys
import ctypes
import os

# Load .env file if present (for GROQ_API_KEY and other env vars)
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(_env_path):
    with open(_env_path) as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#") and "=" in _line:
                _k, _v = _line.split("=", 1)
                os.environ.setdefault(_k.strip(), _v.strip())

# Setup basic logging to file for debugging
import logging

logging.basicConfig(
    level=logging.DEBUG,
    filename="flask_debug.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

from app.dashboard import create_app


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == "__main__":
    if not is_admin():
        print(
            "Elevating privileges... Please click 'Yes' on the User Account Control prompt."
        )
        # Re-run the program with admin rights
        # Parameters: hwnd, Operation, File, Parameters, Directory, ShowCmd
        # ShowCmd = 1 (SW_SHOWNORMAL)
        ret = ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        if ret <= 32:
            print("Elevation failed or cancelled by user.")
        sys.exit()

    print("Running with Administrator privileges.")
    app = create_app()
    print("Starting Dashboard...")
    app.run(host="0.0.0.0", port=5000, debug=True)
