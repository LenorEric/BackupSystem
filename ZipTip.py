import base64
import time
import os
import json
from zlib import crc32


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
        for file in current_target:
            if type(file) == list:
                backup(file)
            else:
                try:
                    if os.path.isfile(file):
                        zip_name = backup_location + "\\" + task_name + "\\" + "data\\" + os.path.basename(
                            file) + '_' + getCRCBuiltin(file) + '.7z'
                        dir_file.write(base64.b64encode(str(zip_name).encode("utf-8")).decode("utf-8") + "\n")
                        if os.path.exists(zip_name):
                            continue
                        cmd = '.\\p7z\\7za.exe a "' + zip_name + '" "' + file + '" -t7z -mx=7 -mmt=8'
                        os.system(cmd)
                except Exception as error:
                    print("Proceeding Target: ", file, " , Error: ", error)

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
        return
    dir_file = open(dir_file_name, mode='w', encoding="utf-8")
    target_for_write = json.dumps(target)
    dir_file.write(base64.b64encode(target_for_write.encode("utf-8")).decode("utf-8") + "\n")
    backup(target)
    dir_file.close()
    dir_file = open(dir_file_name, mode='r', encoding="utf-8")
    data_set = dir_file.read().encode("utf-8")

    dir_file.close()


file_name_counter = 0


def restoreFile(target, location, file_names):
    def restore(current_target):
        global file_name_counter
        for file in current_target:
            if type(file) == list:
                restore(file)
            else:
                try:
                    zip_name = file_names[file_name_counter]
                    file_name_counter += 1
                    save_file = os.path.join(location, file[len(root):])
                    if os.path.exists(save_file):
                        continue
                    cmd = '.\\p7z\\7za.exe x "' + zip_name + '" -o "' + save_file
                    os.system(cmd)
                except Exception as error:
                    print("Proceeding Target: ", file, " , Error: ", error)

    file_name_counter = 0
    root = target[0]
    restore(target)
