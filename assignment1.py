import zipfile
import glob
import zlib
import shutil
import sys

# Security 2023 Assignment 1
# Daniël Zee s2063131
# Tested on Python 3.6.9


def bruteforce_archive(zip_path, txt_path):
    """ Try all the passwords in a txt file to extract the content of a zip file to a folder with the same name.

    Parameters:
        zip_path (str): The path of the zip file to be extracted.
        txt_path (str): The path of the txt file where the passwords are taken from.

    Returns:
        (str): The path of the folder where the contents of the zip file were extracted to.
    """
    with zipfile.ZipFile(zip_path, mode="r") as archive:
        with open(txt_path, mode="rb") as txt_file:
            print(f"Archive: {zip_path}\nTrying all passwords in {txt_path}") if verbose else None
            for line in txt_file:
                password = line.strip()
                try:
                    archive.extractall(zip_path[:-4], pwd=password)
                    print(f"Password: {password} was correct!\n") if verbose else None
                    return zip_path[:-4] + "/"
                except (RuntimeError, zlib.error, zipfile.BadZipFile):
                    continue
            shutil.rmtree(zip_path[:-4])
            raise RuntimeError(f"None of the passwords in {txt_path} were correct for {zip_path}.")


verbose = sys.argv[1] == "-v" if len(sys.argv) > 1 else False  # User has the option to show the progress of the script
password_txt_path = glob.glob("*.txt")[0]  # The first txt file the script finds is used for the passwords
working_directory = ""
archives = glob.glob(working_directory + "*.zip")
while archives:  # Continue bruteforcing until the extracted folder does not contain a zip file
    working_directory = bruteforce_archive(archives[0], password_txt_path)
    archives = glob.glob(working_directory + "*.zip")
else:  # Print the content of all the found files to the screen and move the files to the root folder
    for txt_path in glob.glob(working_directory + "*"):
        with open(txt_path, mode="r") as t:
            print(t.read())
        shutil.move(txt_path, ".")
    shutil.rmtree(working_directory.split("/", 1)[0])
