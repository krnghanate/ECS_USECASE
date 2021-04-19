import datetime
import os, sys, logging,traceback
sys.path = [os.path.abspath("site-packages") ]+ sys.path
import subprocess
import re
from os import listdir
from os.path import isfile, join


def read_folder(folder_path):
    dirs = os.path.join(folder_path)
    sh_files = []
    # subfiles = [x for x in dirs]
    subfiles = [f for f in listdir(folder_path) if isfile(join(folder_path, f))]
    for file in subfiles:
        if ".bat" in file:
            sh_files.append(file)
    return sh_files


def read_version_file(version_file_path):
    with open(os.path.join(version_file_path,"Version.txt"),"r") as fp:
        version_no = fp.read()
    version_no = int(str(version_no).split("=")[1])
    return version_no


def update_version_file(version_file_path, version_no):
    with open(os.path.join(version_file_path,"Version.txt"), "r+") as fp:
        old = fp.read()
        fp.seek(0)
        fp.write("Version number=" + str(version_no))
        fp.close()


def execute_shell_script(sh_command):
    print(sh_command)
    output = subprocess.check_output(sh_command)
    log_file_name = str(os.path.basename(sh_command)).split(".")[0]
    fp = open(str(log_file_name+'.log'),'w+')
    for line in output:
        fp.write(str(line))
    fp.close()


def validate_sh_file(shfile_name):
        if " " in shfile_name:
            return False
        if re.match(r"^\d+.*$", str(shfile_name)):
            return True
        elif re.match(r"^([!@#$%^&*_]).*$/i", str(shfile_name)):
            return False
        else:
            logging.error("File Name does not start with number")
            return False

def sep_no_from_file(file_name):
    file_no = int(str(file_name).split(".")[0])
    return file_no

def iterate_sh_files(folder_path,version_path):
    try:
        sh_files = read_folder(folder_path)
        for file in sh_files:
            try:
                logging.info("==============START TIME===============\n"+"START TIME =>"+str(datetime.datetime.now()))
                logging.info("Current File Name=>" + str(file))
                version_no = read_version_file(version_path)
                logging.info("Current Version Number=>" + str(version_no))
                validate = validate_sh_file(file)
                if validate:
                    logging.info("File Validated Successfully")
                    file_no = sep_no_from_file(file)
                    if file_no >= version_no:
                        file_path=os.path.join(folder_path,file)
                        execute_shell_script(file_path)
                        update_version_file(version_path, file_no)
                        logging.info("==============END TIME===============\n" + "END TIME =>" + str(datetime.datetime.now()))
                else:
                    logging.error("File format not in correct format")
            except Exception as e:
                print(traceback.format_exc())
                logging.error(traceback.format_exc())
    except Exception as e:
        print(traceback.format_exc())







if __name__ == '__main__':
    memory_store = {}
    memory_store["Folder_path"] = sys.argv[1]
    memory_store["Version_path"] = sys.argv[2]
    log_file_name = datetime.datetime.now().strftime("mylogfile_%H_%M_%d_%m_%Y.log")
    logging.basicConfig(filename=log_file_name, filemode='w', format='%(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    iterate_sh_files(memory_store["Folder_path"], memory_store["Version_path"])
