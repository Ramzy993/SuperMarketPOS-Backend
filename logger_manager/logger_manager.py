#!/usr/bin/env python3

# lib imports
import os
import logging

# project imports
from config_manager.config_manager import ConfigManager
from utilities.patterns.singleton import SingletonDecorator


app_config = ConfigManager().app_config


@SingletonDecorator
class LogManger:

    def __init__(self):
        self.log_extension = app_config.get('LOGGER', 'log_extension', fallback='.log')
        self.log_name = app_config.get('LOGGER', 'log_name', fallback='dev')
        self.log_file_path = os.path.join(os.path.dirname(__file__), 'logs', self.log_name + self.log_extension)
        self.log_file_mode = app_config.get('LOGGER', 'log_file_mode', fallback='a')
        self.log_level_type = app_config.get('LOGGER', 'log_level', fallback='debug')
        self.log_datetime_format = app_config.get('LOGGER', 'log_datetime_format', fallback='%d-%b-%y %H:%M:%S')

        self.log_level = logging.DEBUG
        self.set_log_level()

        logging.basicConfig(filename=self.log_file_path, filemode=self.log_file_mode, datefmt=self.log_datetime_format,
                            level=self.log_level, format="%(levelname)s %(asctime)s : %(message)s")

    @classmethod
    def get_logger(cls, name):
        return logging.getLogger(name=name)

    def set_log_level(self):
        if self.log_level_type == 'debug':
            self.log_level = logging.DEBUG
        elif self.log_level_type == 'info':
            self.log_level = logging.INFO
        elif self.log_level_type == 'warning':
            self.log_level = logging.WARNING
        elif self.log_level_type == 'error':
            self.log_level = logging.ERROR
        else:
            self.log_level = logging.CRITICAL
