"""
Utilities for foles
"""
import logging
import os

LOGGER = logging.getLogger(__name__)


def get_home_folder():
    """
    Return the home folder for the user that executes the process
    :return:
    """
    return os.path.expanduser("~")


def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        logging.debug(f"Directory {path} created")
    else:
        if os.path.isdir(path):
            logging.debug(f"Directory {path} already exists, skipping")
        else:
            logging.error(f"{path} exists and is not a directory")
            raise FileExistsError(f"{path} exists and is not a directory")


