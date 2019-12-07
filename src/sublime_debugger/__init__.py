from __future__ import annotations
import logging
from logging.handlers import RotatingFileHandler
import os
import sys

from .config import Config
from .library import set_config, process_cached_logs
from .__header__ import __header__


# Load User Defined Config
DEFAULT_CONFIG_PATH = f'~/.config/{__header__.lower()}'
CONFIG_PATH = os.environ.get(f'{__header__}_CONFIG_PATH', DEFAULT_CONFIG_PATH)
CONFIG = Config(CONFIG_PATH)

# Logging Configuration
logger = logging.getLogger(__header__)
set_config(CONFIG, 'logging.path')
set_config(
    CONFIG,
    'logging.format',
    '%(asctime)s - %(module)s:%(lineno)s - %(levelname)s - %(message)s',
)
set_config(CONFIG, 'logging.level', 'INFO')
loghandler_sys = logging.StreamHandler(sys.stdout)

# Checking if log path is set
if CONFIG.logging_path:
    CONFIG.logging_path += (
        f'{__header__}.log'
        if CONFIG.logging_path[-1] == '/'
        else f'/{__header__}.log'
    )
    # Set default log file options
    set_config(CONFIG, 'logging.backup_count', 3, int)
    set_config(CONFIG, 'logging.rotate_bytes', 512000, int)

    # Configure file handler
    loghandler_file = RotatingFileHandler(
        os.path.expanduser(CONFIG.logging_path),
        'a',
        CONFIG.logging_rotate_bytes,
        CONFIG.logging_backup_count,
    )

    # Add to file formatter
    loghandler_file.setFormatter(logging.Formatter(CONFIG.logging_format))
    logger.addHandler(loghandler_file)

# Configure and add to stdout formatter
loghandler_sys.setFormatter(logging.Formatter(CONFIG.logging_format))
logger.addHandler(loghandler_sys)
logger.setLevel(CONFIG.logging_level)

# Load module environment variables
set_config(CONFIG, 'sublime.project_file')
set_config(CONFIG, 'sublime.virtualenv', os.environ.get('VIRTUAL_ENV'))

# Print logged messages
process_cached_logs(CONFIG, logger)
