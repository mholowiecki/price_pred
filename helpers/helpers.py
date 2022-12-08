import configparser
import logging
from dataclasses import dataclass
import csv
from urllib.error import HTTPError, URLError

import pandas as pd
from datetime import datetime
from typing import Tuple
import typer
from pandas.core.series import Series


@dataclass
class AppSettings:
    config = configparser.ConfigParser()
    config.read('config/settings.ini')
    return_console_messages = int(config['APP_SETTINGS']['return_console_messages'])
    use_logs = int(config['APP_SETTINGS']['use_logs'])
    logging_level = int(config['APP_SETTINGS']['logging_level'])