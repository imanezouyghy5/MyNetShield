import os
import sys
import logging
from waitress import serve
from app.dashboard import create_app

from pathlib import Path

# Determine log file path (use APPDATA if frozen, else local dir)
if getattr(sys, 'frozen', False):
    log_dir = Path(os.environ.get('APPDATA', str(Path.home()))) / "MyNetShield"
    log_dir.mkdir(parents=True, exist_ok=True)
    log_path = log_dir / "production_server.log"
else:
    log_path = "production_server.log"

# Set up handlers
log_handlers: list[logging.Handler] = [logging.FileHandler(log_path, encoding="utf-8")]
if not getattr(sys, 'frozen', False):
    log_handlers.append(logging.StreamHandler(sys.stdout))

# Set up logging for production
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=log_handlers
)

logger = logging.getLogger("waitress")

def run_production():
    """Run the MyNetShield application with Waitress."""
    # Ensure secret key is set
    if not os.environ.get("SECRET_KEY"):
        logger.warning("SECRET_KEY not found in environment. Using default (not recommended for production).")
    
    app = create_app()
    
    port = int(os.environ.get("PORT", 5173))

    logger.info(f"Starting MyNetShield Production Server on port {port}...")
    logger.info("Serving frontend from app/dashboard/frontend/dist")
    
    # Run the server (configured for ngrok/proxies)
    serve(
        app, 
        host='0.0.0.0', 
        port=port, 
        threads=8,
        url_scheme='https',          # Help Flask know it's behind HTTPS (ngrok)
        trusted_proxy='*',           # Trust ngrok proxy
        trusted_proxy_count=1,       
        clear_untrusted_proxy_headers=False
    )


if __name__ == "__main__":
    try:
        run_production()
    except KeyboardInterrupt:
        logger.info("Server stopped by user.")
    except Exception as e:
        logger.error(f"Critical error during server startup: {e}", exc_info=True)
