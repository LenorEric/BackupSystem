import json
import PathOperation as PaOp
import ZipTip as ZiTi

if __name__ == '__main__':
    task_list_file = open("TaskList.json", 'r', encoding="utf-8")
    task_list = json.loads(task_list_file.read())
    for task in task_list:
        print(task["from path"])
        ZiTi.backupFile(task["task name"], PaOp.getPath(task["from path"]), task["to path"])
    task_list_file.close()
