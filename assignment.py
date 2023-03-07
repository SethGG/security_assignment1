import zipfile
import glob
import zlib
import shutil
import sys

verbose = sys.argv[1] == "-v" if len(sys.argv) > 1 else False
password_txt_path = glob.glob("*.txt")[0]
working_directory = ""


def bruteforce_archive(zip_path, txt_path):
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


archives = glob.glob(working_directory + "*.zip")
while archives:
    working_directory = bruteforce_archive(archives[0], password_txt_path)
    archives = glob.glob(working_directory + "*.zip")
else:
    for txt_path in glob.glob(working_directory + "*.txt"):
        with open(txt_path, mode="r") as t:
            print(t.read())
        shutil.move(txt_path, ".")
    shutil.rmtree(working_directory.split("/", 1)[0])
