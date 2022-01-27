import os


def getPath(path):
    file_path = [path]
    try:
        files = os.listdir(path)
        for f in files:
            if os.path.isdir(path + '/' + f):
                file_path.append(getPath(path + '/' + f))
            if os.path.isfile(path + '/' + f):
                file_path.append(path + '/' + f)
        return file_path
    except Exception as error:
        print("Proceeding Path: ", path, " , Error: ", error)
