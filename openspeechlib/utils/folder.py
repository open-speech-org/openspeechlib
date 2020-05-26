"""
Utilities for folders
"""
import glob
import os


def get_all_files_by_extension_in_folder(folder, extension='wav'):
    """
    Returns a list with all the absolute paths of files with :extension: within the :folder:
    :param folder: OS Folder
    :param extension: File Extension
    :return: List with files
    """
    return glob.glob(os.path.join(folder, '**', f'*.{extension}'), recursive=True)
