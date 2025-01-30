from fastapi.templating import Jinja2Templates
from src.utils.logger import setup_package_logger

setup_package_logger()
templates = Jinja2Templates(directory="src/frontend")