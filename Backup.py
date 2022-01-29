import json
import PathOperation as PaOp
import ZipTip as ZiTi
import os

need_reconfirm = True


def loadConfig(config_file=".\\Config.json"):
    global need_reconfirm
    with open(config_file, 'r') as config_f:
        config = config_f.read()
        config = json.loads(config)
        need_reconfirm = config["need_reconfirm"]
        if type(need_reconfirm) != bool:
            print("Wrong config: ", "need_reconfirm")


if __name__ == '__main__':
    loadConfig()
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
