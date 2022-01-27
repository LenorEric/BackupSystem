import json
import PathOperation as PaOp
import ZipTip as ZiTi

if __name__ == '__main__':
    task_list = open("TaskList.txt", 'r', encoding="utf-8")
    for task in task_list:
        current_task_path = str(task)
        current_task_path = current_task_path.rstrip()
        current_task_path = current_task_path.lstrip()
        comment_pos = current_task_path.find('#')
        if comment_pos != -1:
            if comment_pos == 0:
                continue
            current_task_path = current_task_path[0:comment_pos]
        current_task_name = current_task_path.split()[0]
        current_task_path = current_task_path[current_task_path.find(' ')+1:]
        ZiTi.backupFile(PaOp.getPath(current_task_path), current_task_name)
    task_list.close()
