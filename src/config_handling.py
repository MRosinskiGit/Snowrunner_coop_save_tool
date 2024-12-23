import global_variables as gv
import json
from loguru import logger


def load_config() -> dict:
    """
    Loads config.json from config_data directory and returns its content as dict.
    """
    try:
        with open(gv.CONFIG_PATH) as f:
            return json.load(f)

    except FileNotFoundError as e:
        logger.critical(f"File in {gv.CONFIG_PATH} was not found.\n" f"Exception: {e}")
    except PermissionError as e:
        logger.critical(
            f"File cannot be open due to permission denied." f"Exception: {e}"
        )
    except json.JSONDecodeError as e:
        logger.critical(f"JSON Structure issue.\n" f"Exception: {e}")
        with open(gv.CONFIG_PATH) as f:
            text = f.read()
        logger.debug(f"config content: {text}")


def save_config(config: dict) -> None:
    """
    Saves provided dict to json format in config_data directory.
        :param config: dict with data to save
    """
    logger.trace(f"Attempting to save config with data: {config}")
    with open(gv.CONFIG_PATH, "w") as f:
        json.dump(config, f)
        logger.trace("Config saved to file")
