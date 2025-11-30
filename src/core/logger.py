import logging


def configure_logger(level: int = logging.INFO):
    """
    Congifures the logging for the app

    Args:
        level: The log level, defaults to INFO
    """

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Add handleers
    if not root_logger.handlers:
        consoler_handler = logging.StreamHandler()
        consoler_handler.setLevel(level)

        # Format
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
        )
        consoler_handler.setFormatter(formatter)

        # Add
        root_logger.addHandler(consoler_handler)

    print(
        f"Configured Root logger with ID: {id(root_logger)} with level: {logging.getLevelName(root_logger.level)}"
    )
