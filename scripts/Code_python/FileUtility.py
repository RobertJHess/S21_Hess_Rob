import os
from itertools import islice


class FileUtility:


    def __init__(self):
        pass

    @staticmethod
    def get_topN_lines_from_file(file_name, n):
        """Utility that returns list of the top N lines in a file.

        Args:
            file_name (string): file path
            n (int): number of lines

        Returns:
            list: a list of lines from file
        """
        with open(file_name) as myfile:
            head = list(islice(myfile, n))
        return head

    @staticmethod
    def read_all_lines(file_name):
        try:
            with open(file_name) as myfile:
                lines = list()
                for line in myfile:
                    lines.append(line)
        except FileNotFoundError:
            print("File: " + file_name + "is not found")
        return lines

    @staticmethod
    def write_lines(file_name, list_to_write, mode="w"):
        try:
            with open(file_name, mode=mode) as file:
                for line in list_to_write:
                    file.write(line)
                    file.write("\n")
        except FileNotFoundError:
            print("File: " + file_name + "is not found")

    @staticmethod
    def get_list_of_filenames_of_type(type, root_dir):
        """ Utility function that searches a directory and sub directories for a file type then returns a list of
        the paths of each file with that extension

        Args:
            type (string): file extension. ex: csv, txt, etc...
            root (string): root path to the top directory where wanted files are found

        Returns:
            list: a list of paths to files with the given file extension.
        """

        file_names = []
        for subdir, dirs, files in os.walk(root_dir):
            for file in files:
                if file[-len(type):] == type:
                    file_names.append(os.path.join(subdir, file))
        return file_names

    @staticmethod
    def __read_dictionary_from_file(mydict=None, file_name="", comment_char='#', separator='='):
        if mydict is None:
            mydict = {}

        try:
            with open(file_name) as f:
                for line in f:
                    line_stripped = line.strip()
                    if line_stripped.find(comment_char) != -1:
                        line_stripped = line_stripped[0:line_stripped.find(comment_char)]
                    if line_stripped and not line_stripped.startswith(comment_char):
                        (key, val) = line_stripped.split(separator)
                        mydict[str(key).strip()] = val.strip()
        except FileNotFoundError:
            print("File: " + file_name + "is not found")
        
        return mydict
