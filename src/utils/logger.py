import logging
from logging.handlers import RotatingFileHandler


def setup_package_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(asctime)s - %(message)s - %(name)s",
        datefmt="%Y-%m-%d %H:%M",
        handlers=[logging.StreamHandler(), RotatingFileHandler(filename="package.log",
                                                               maxBytes=5 * 1024 * 1024,
                                                               backupCount=3)])