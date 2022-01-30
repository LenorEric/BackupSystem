import base64
import time
import os
import json
from zlib import crc32
from subprocess import run


def getCRCBuiltin(file_path):
    with open(file_path, 'rb') as f:
        checksum = crc32(f.read()) & 0xffffffff
        return str(hex(checksum)).upper()[2:].rjust(8, '0')


def getCRC(file_path):
    cmd = os.getcwd() + "\\p7z\\7za.exe h " + '"' + file_path + '" -scrc CRC32 -mmt=on'
    ret = os.popen(cmd).read().split()
    ret = ret[ret.index("data:") + 1]
    return str(ret)


def backupFile(task_name, target, location=".\\data"):
    def backup(current_target):
        for i in range(len(current_target)):
            if i == 0:
                continue
            if type(current_target[i]) == list:
                backup(current_target[i])
            else:
                zip_name = "ERROR"
                try:
                    zip_name = backup_location + "\\" + task_name + "\\" + "data\\" + os.path.basename(
                        current_target[i]) + '_' + getCRCBuiltin(current_target[i]) + '.7z'
                    if not os.path.exists(zip_name):
                        cmd = '.\\p7z\\7za.exe a "' + zip_name + '" "' + current_target[i] + '" -t7z -mx=7 -mmt'
                        if os.path.exists(current_target[i]):
                            run(cmd, shell=True)
                        else:
                            print("FNE: ", end='')
                    else:
                        print("AE: ", end='')
                except Exception as error:
                    print("Proceeding Target: ", current_target[i], " , Error: ", error)
                dir_file.write(base64.b64encode(str(zip_name).encode("utf-8")).decode("utf-8") + "\n")
                print(zip_name)

    backup_location = location
    if not os.access(backup_location, os.F_OK):
        os.mkdir(backup_location)
    if not os.access(backup_location + "\\" + task_name, os.F_OK):
        os.mkdir(backup_location + "\\" + task_name)
    formatted_time = time.localtime(time.time())
    dir_file_name = \
        backup_location + "\\" + task_name + "\\dir_file_" + "%02d" % (formatted_time[0] - 2000) \
        + "%02d" % formatted_time[1] + "%02d" % formatted_time[2] + "%02d" % formatted_time[3] \
        + "%02d" % formatted_time[4] + ".dat"
    if os.access(dir_file_name, os.F_OK):
        print("Redundant backup warning")
        os.system("pause")
        exit()
    dir_file = open(dir_file_name, mode='w', encoding="utf-8")
    target_for_write = json.dumps(target)
    dir_file.write(base64.b64encode(target_for_write.encode("utf-8")).decode("utf-8") + "\n")
    backup(target)
    dir_file.close()
    dir_file = open(dir_file_name, mode='r', encoding="utf-8")

    dir_file.close()


file_name_counter = 0


def restoreFile(target, location, file_names):
    def restore(current_target):
        global file_name_counter
        for i in range(len(current_target)):
            if i == 0:
                continue
            if type(current_target[i]) == list:
                restore(current_target[i])
            else:
                try:
                    zip_name = file_names[file_name_counter]
                    file_name_counter += 1
                    save_file = os.path.join(location, current_target[i][len(root):])
                    if not os.path.exists(save_file):
                        if os.path.exists(zip_name):
                            cmd = '.\\p7z\\7za.exe x "' + zip_name + '" -o"' + os.path.split(save_file)[0]
                            run(cmd, shell=True)
                        else:
                            print("FNE: ")
                    else:
                        print("AE: ")
                except Exception as error:
                    print("Proceeding Target: ", current_target[i], " , Error: ", error)
                print(current_target[i])

    file_name_counter = 0
    root = target[0] + os.sep
    restore(target)
