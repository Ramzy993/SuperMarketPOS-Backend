#!/usr/bin/env python3

# lib imports
import os
from configparser import ConfigParser, ExtendedInterpolation

# project imports
from utilities.patterns.singleton import Singleton


class ConfigManager(Singleton):

    def __init__(self):
        pass

    def init(self):
        self.stage = 'dev'
        self.config_files_path = os.path.abspath(os.path.join(__file__, '..', 'configs'))
        self.config_file_ending = '.env.config.ini'
        self.env_config_file_path = os.path.join(self.config_files_path, self.stage + self.config_file_ending)

        self.app_config = ConfigParser(interpolation=ExtendedInterpolation())
        self.app_config.read(self.env_config_file_path)

