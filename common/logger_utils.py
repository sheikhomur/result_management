import logging, os

formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")


def setup_logger(name, log_file, level="info"):
    if level == "info":
        level = logging.INFO
    elif level == "debug":
        level = logging.DEBUG
    elif level == "error":
        level = logging.ERROR
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


info_logger = setup_logger(name="info_logger", log_file=os.path.abspath(os.path.join("logs", "info.log")), level="info")
error_logger = setup_logger(name="error_logger", log_file=os.path.abspath(os.path.join("logs", "error.log")), level="error")
