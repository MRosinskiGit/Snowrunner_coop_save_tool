import fnmatch
import shutil
from datetime import datetime

from config_handling import save_config
from src.config_handling import load_config
from src.enums import _PlatformEnum
from loguru import logger

import sys
import src.global_variables as gv
import os
import re


class SnowRunnerMergeTool:
    def __init__(self):
        self.platform = ...
        if gv.CONFIG is Ellipsis:
            logger.trace("Config undefined, reading and saving to gv.")
            gv.CONFIG = load_config()

        if gv.CONFIG["save_path"] is None:
            logger.trace("Path is none, initializing first configuration.")
            self.__initial_config()
        if not os.path.isdir(os.path.join(gv.ROOT_DIRECTORY, "export")):
            os.mkdir(os.path.join(gv.ROOT_DIRECTORY, "export"))

        if not os.path.isdir(os.path.join(gv.ROOT_DIRECTORY, "saves")):
            os.mkdir(os.path.join(gv.ROOT_DIRECTORY, "saves"))

        if not os.path.isdir(os.path.join(gv.ROOT_DIRECTORY, "backups")):
            os.mkdir(os.path.join(gv.ROOT_DIRECTORY, "backups"))

        # Define files to skip during copying or creating backup
        self.__files_to_skip = ["CommonSslSave.*", "user_profile.*", "user_settings.*", "user_social_data.*"]

    def __initial_config(self):
        while True:
            print("[FIRST RUN]")
            print("Pick your platform:")
            print("\t1. Steam")
            print("\t2. Epic")
            print("\t0. Exit")
            # TODO Refactor with Rich
            try:
                user_input = int(input())
            except ValueError:
                print("Incorrect entry.")
                continue

            if user_input == 0:
                sys.exit(0)
            try:
                self.platform = _PlatformEnum(user_input)
                break
            except ValueError:
                print("Incorrect entry.")
                continue
        gv.CONFIG["save_path"] = self.__find_save_directory()
        save_config(gv.CONFIG)
        return True
        # CONFIG["id_counter"] = get_last_id(local_dir)

    def export_save(self):
        # Select files to export
        print(f"\n[CHOOSING LOCAL SAVE FILE] - {gv.CONFIG['save_path']}")
        files_to_copy = [
            os.path.join(gv.CONFIG["save_path"], file)
            for file in os.listdir(gv.CONFIG["save_path"])
            if not self.__should_file_be_skipped(file)
        ]
        completesaves_in_save_directory = [file for file in files_to_copy if "CompleteSave" in os.path.split(file)[1]]

        if len(completesaves_in_save_directory) == 0:
            print("No save found.")
        if len(completesaves_in_save_directory) > 1:
            print("Multiple files detected, pick correct one")
            for index, file in enumerate(completesaves_in_save_directory):
                file_modification_date = datetime.fromtimestamp(os.path.getmtime(file)).strftime("%m/%d/%Y, %H:%M:%S")
                print(f"{index+1}: {os.path.split(file)[1]} Modification date: {file_modification_date}")
            user_choice = int(input())
            completesaves_in_save_directory.pop(user_choice - 1)
            for f in completesaves_in_save_directory:
                files_to_copy.remove(f)

        # Prepare for exporting
        illegal_chars = ("<", ":", '"', "/", "\\", "|", "?", "*")

        while True:
            save_name = input("File name (optional, leave blank for default name): ")
            if not save_name:
                save_name = "Save_export_" + datetime.now().strftime("%m-%d-%Y_%H-%M-%S")

            if any(char in save_name for char in illegal_chars):
                print(f"File name cannot contain following characters {' '.join(illegal_chars)}.")
                continue
            break

        tmp_export_dir = os.path.join(gv.ROOT_DIRECTORY, "export", "tmp")
        if os.path.isdir(tmp_export_dir):
            shutil.rmtree(tmp_export_dir)
        os.mkdir(tmp_export_dir)

        # Prepare and create archive
        for file in files_to_copy:
            shutil.copyfile(file, os.path.join(tmp_export_dir, os.path.split(file)[1]))

        shutil.make_archive(os.path.join(os.path.split(tmp_export_dir)[0], save_name), "zip", tmp_export_dir)
        shutil.rmtree(tmp_export_dir)

    def _create_backup(self):
        backup_directory_name = "Backup_" + datetime.now().strftime("%m-%d-%Y_%H-%M-%S")
        backup_directory = os.path.join(gv.ROOT_DIRECTORY, "backups", backup_directory_name)
        os.mkdir(backup_directory)

        files_to_copy = [os.path.join(gv.CONFIG["save_path"], file) for file in os.listdir(gv.CONFIG["save_path"])]
        for file in files_to_copy:
            shutil.copyfile(file, os.path.join(backup_directory, os.path.split(file)[1]))


    def import_save(self):
        pass

    def __should_file_be_skipped(self, filename):
        return any(fnmatch.fnmatch(filename, pattern) for pattern in self.__files_to_skip)

    def __find_save_directory(self):
        if self.platform == _PlatformEnum.EPIC:
            save_path_documents = f"C:\\Users\\{os.getlogin()}\\Documents\\My Games\\SnowRunner\\base\\storage"
            if os.path.isdir(save_path_documents):
                return save_path_documents
            save_path_onedrive = f"C:\\Users\\{os.getlogin()}\\OneDrive\\Documents\\My Games\\SnowRunner\\base\\storage"
            if os.path.isdir(save_path_onedrive):
                return save_path_onedrive

        elif self.platform == _PlatformEnum.STEAM:
            snowrunner_directory_id = "1465360"
            steam_user_dir = "C:\\Program Files (x86)\\Steam\\userdata"
            found_paths = []
            if os.path.isdir(steam_user_dir):
                for root, dirs, file in os.walk(steam_user_dir):
                    if (
                        snowrunner_directory_id in root
                        and "backups" not in root
                        and bool(re.search("CompleteSave.*", str(file)))
                    ):
                        found_paths.append(root)
                if len(found_paths) == 1:
                    return found_paths[0]
                    # TODO check when multiple paths was found

        print("Save path was not found")
        print("Please provide path to 'storage' drectory (Epic) or 'remote' (Steam)")
        # TODO make this input bulletproof
        user_input = input()
        user_path = os.path.normpath(user_input)
        files = os.listdir(user_path)
        is_save_found = bool(re.search("CompleteSave.*", str(files)))
        if is_save_found:
            return user_path
        else:
            raise FileNotFoundError("Save not found in provided directory.")


if __name__ == "__main__":
    x = SnowRunnerMergeTool()
    x.export_save()
