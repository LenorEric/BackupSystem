import tkinter.filedialog
import base64
import json
import ZipTip as ZiTi
import os

if __name__ == '__main__':
    tk_instance = tkinter.Tk()  # 创建一个Tkinter.Tk()实例
    tk_instance.withdraw()  # 将Tkinter.Tk()实例隐藏
    dir_file_name = tkinter.filedialog.askopenfilename()
    folder_path = os.path.split(dir_file_name)[0]
    dirname = tkinter.filedialog.askdirectory()
    dir_file = open(dir_file_name, mode='r', encoding="utf-8")
    target = base64.b64decode(dir_file.readline().encode("utf-8")).decode("utf-8")
    target = json.loads(target)
    files = dir_file.readlines()
    dir_file.close()
    for i in range(len(files)):
        files[i] = base64.b64decode(files[i].encode("utf-8")).decode("utf-8")
        file_file_name = os.path.split(files[i])[1]
        files[i] = os.path.join(folder_path, "data", file_file_name)
    ZiTi.restoreFile(target, dirname, files)
    print("finished")
    os.system("pause")
