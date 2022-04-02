import json
import tkinter.filedialog
import PathOperation as PaOp
import ZipTip as ZiTi
import os

need_reconfirm = True
mode = 0
default_name = ""


def loadConfig(config_file=".\\Config.json"):
    global need_reconfirm, mode, default_name
    with open(config_file, 'r') as config_f:
        config = config_f.read()
        config = json.loads(config)
        need_reconfirm = config["need_reconfirm"]
        mode = config["using_mode"]
        default_name = config["default_name"]
        if type(need_reconfirm) != bool:
            print("Wrong config: ", "need_reconfirm")
        if mode == "user_select":
            mode = 0
        elif mode == "task_list":
            mode = 1


def modifyJsonFile(file, index, value):
    with open(file, 'r', encoding="utf-8") as json_file:
        jsons = json.loads(json_file.read())
        json_file.close()
    with open(file, 'w', encoding="utf-8") as json_file:
        jsons[index] = value
        json_file.write(json.dumps(jsons))
        json_file.close()


if __name__ == '__main__':
    loadConfig()
    task_list = []
    if mode == 0:
        tk_instance = tkinter.Tk()  # 创建一个Tkinter.Tk()实例
        tk_instance.withdraw()  # 将Tkinter.Tk()实例隐藏
        print("Input task name(default by :", default_name, "):", end="")
        task_name = input()
        default_operator = [""]
        if task_name in default_operator:
            task_name = default_name
        else:
            modifyJsonFile("Config.json", "default_name", task_name)
        task_list = [{'task name': task_name, 'from path': tkinter.filedialog.askdirectory()}]
    elif mode == 1:
        with open("TaskList.json", 'r', encoding="utf-8") as task_list_file:
            task_list = json.loads(task_list_file.read())
            task_list_file.close()
        if need_reconfirm:
            if task_list[0] != "":
                print("Please re-confirm")
                os.system("pause")
                exit()
            task_list[0] = "Need Re-confirm"
            with open("TaskList.json", 'w', encoding="utf-8") as task_list_file:
                task_list_file.write(json.dumps(task_list))
                task_list_file.close()
        task_list = task_list[1:]
    for task in task_list:
        print(task["from path"])
        ZiTi.backupFile(task["task name"], PaOp.getPath(task["from path"]))
    print("finished")
    os.system("pause")
