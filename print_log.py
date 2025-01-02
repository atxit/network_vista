import random

from colorlog import ColoredFormatter

COLOUR_LOG_FORMAT = (
    " %(log_color)s%(levelname)-8s%(reset)s| "
    "%(asctime)s | %(log_color)s%(message)s%(reset)s"
)


def print_to_screen(log_str, log_level="info"):
    """
    logger setup
    :return:
    """
    import logging

    logging.root.setLevel(logging.DEBUG)
    colour_formatter = ColoredFormatter(COLOUR_LOG_FORMAT)
    stream = logging.StreamHandler()
    stream.setLevel(logging.DEBUG)
    stream.setFormatter(colour_formatter)
    log_screen = logging.getLogger(str(random.randint(0, 1000)))
    log_screen.setLevel(logging.DEBUG)
    log_screen.addHandler(stream)

    if log_level == "info":
        log_screen.info(log_str)
    elif log_level == "error":
        log_screen.error(log_str)
    elif log_level == "warning":
        log_screen.warning(log_str)
    elif log_level == "debug":
        log_screen.debug(log_str)
