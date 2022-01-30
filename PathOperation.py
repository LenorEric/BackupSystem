import os


def getPath(path):
    def sweep(path_):
        file_path = [path_]
        try:
            files = os.listdir(path_)
            for f in files:
                if os.path.isdir(path_ + '\\' + f):
                    file_path.append(sweep(path_ + '\\' + f))
                if os.path.isfile(path_ + '\\' + f):
                    file_path.append(path_ + '\\' + f)
            return file_path
        except Exception as error:
            print("Proceeding Path: ", path_, " , Error: ", error)

    print("get path")
    path_tree = sweep(path)
    print("get path success")
    return path_tree
