from app.dashboard import create_app
import os

if __name__ == "__main__":
    # Load .env file
    _env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    if os.path.exists(_env_path):
        with open(_env_path) as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ.setdefault(_k.strip(), _v.strip())

    app = create_app()
    print("Starting Dashboard (Simple Mode)...")
    app.run(host="0.0.0.0", port=5000, debug=True)
