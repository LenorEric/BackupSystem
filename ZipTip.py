import base64
import time
import os

backup_location = ".\\Backup1"


def getCRC(file_path):
    cmd = os.getcwd() + "\\p7z\\7za.exe h " + '"' + file_path + '" -scrc CRC32 -mmt=on'
    ret = os.popen(cmd).read().split()
    ret = ret[ret.index("data:") + 1]
    return str(ret)


def backupFile(target, location):
    def backup(current_target):
        for file in current_target:
            if type(file) == list:
                backup(file)
            else:
                try:
                    if os.path.isfile(file):
                        zip_name = backup_location + "\\" + location + "\\" + os.path.basename(file) + '_' + getCRC(
                            file) + '.7z'
                        if os.path.exists(zip_name):
                            continue
                        cmd = '.\\p7z\\7za.exe a "' + zip_name + '" "' + file + '" -t7z -mx=7 -mmt=8'
                        os.system(cmd)
                        dir_file.write(str(base64.b64encode(str(zip_name).encode("utf-8"))) + "\n")
                except Exception as error:
                    print("Proceeding Target: ", file, " , Error: ", error)

    if not os.access(backup_location, os.F_OK):
        os.mkdir(backup_location)
    if not os.access(backup_location + "\\" + location, os.F_OK):
        os.mkdir(backup_location + "\\" + location)
    dir_file = open(backup_location + "\\" + location + "\\dir_file_" + str(int(time.time())) + ".dat", mode='w',
                    encoding="utf-8")
    dir_file.write(str(base64.b64encode(str(target).encode("utf-8"))) + "\n")
    backup(target)
    dir_file.close()
