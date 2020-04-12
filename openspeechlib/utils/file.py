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


def insert_content_into_file_name(content, file_name):
    with open(file_name, 'w+') as f:
        f.write(content)


def get_content_from_file(file_name):
    try:
        with open(file_name) as f:
            return f.read()
    except FileNotFoundError:
        return None
