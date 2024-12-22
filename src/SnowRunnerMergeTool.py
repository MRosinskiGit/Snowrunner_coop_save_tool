
from src.config_handling import load_config
from loguru import logger
from enum import Enum
import sys
import global_variables as gv
import os

class SnowRunnerMergeTool:
    def __init__(self):
        self.platform = ...
        if isinstance(gv.CONFIG, ellipsis):
            logger.trace("Config undefined, reading and saving to gv.")
            gv.CONFIG = load_config()

        if gv.CONFIG["custom_path"] is None:
            logger.trace("Path is none, initializing first configuration.")
            self.__initial_config()


    def __initial_config(self):
        while True:
            print("[FIRST RUN]")
            print("Pick your platform:")
            print("\t1. Steam")
            print("\t2. Epic")
            print("\t0. Exit")

            try:
                user_input = int(input())
            except ValueError:
                print("Incorrect entry.")
                continue

            if user_input == 0:
                sys.exit(0)
            try:
                self.platform = self.__PlatformEnum(user_input)
                break
            except ValueError:
                print("Incorrect entry.")
                continue
        save_directory = self.__find_save_directory()
        return True



    class __PlatformEnum(Enum):
        """
Enum of handling platform
        """
        STEAM = 1
        EPIC = 2


        # l = get_local_save_path()
        # local_dir = get_save_dirs(l, typ="local")
        # d = dict(DEFAULT_CONFIG)
        # d["colors"] = CONFIG["colors"]
        # CONFIG = d
        # CONFIG["id_counter"] = get_last_id(local_dir)
        # set_colors()
        # CONFIG["first_run"] = False
        # save_config()
        # print(green("Config created."))

    def __find_save_directory(self):
        if self.platform == SnowRunnerMergeTool.__PlatformEnum.EPIC:
            save_path_documents = f"C:\\Users\\{os.getlogin()}\\Documents\\My Games\\SnowRunner\\base\\storage"
            if os.path.isdir(save_path_documents):
                return save_path_documents
            if not os.path.isdir(local_dp):
            save_path_onedrive = f"C:\\Users\\{os.getlogin()}\\OneDrive\\Documents\\My Games\\SnowRunner\\base\\storage"



def get_local_save_path():
    local_dp = (
        f"C:\\Users\\{os.getlogin()}\\Documents\\My Games\\SnowRunner\\base\\storage"
    )
    if not os.path.isdir(local_dp):
        if not CONFIG["custom_path"]:
            print(red("Save directory not found, checking OneDrive."))
            local_dp = f"C:\\Users\\{os.getlogin()}\\OneDrive\\Documents\\My Games\\SnowRunner\\base\\storage"
            if not os.path.isdir(local_dp):
                print(red("OneDrive directory not found."))
                # look for steam directory
                found_files = []
                for root, _, f in os.walk(r"C:\Program Files (x86)\Steam\userdata"):
                    if "CompleteSave.cfg" in f and root not in ["backups","Backup"]:
                        found_files.append(root)
                if len(found_files) == 1:
                    local_dp = os.path.split(found_files[0])[0]
                    print(green("Steam directory found"))
                else:
                    print(
                        f"More than one dicetory found or zero finding: {found_files}"
                    )

                    local_dp = input(
                        "Paste your snowrunner save (storage folder) directory path here (SnowRunner folder in Documents\\My Games, to paste copy and press right mouse button).\n> "
                    )
            CONFIG["custom_path"] = local_dp
            save_config()
        else:
            local_dp = CONFIG["custom_path"]
            print(green("Loaded custom save directory"))

    return os.path.join(local_dp)

