#!/usr/bin/env python3

# lib imports

# project imports
from web_app.app import start_app
from logger_manager.logger_manager import LogManger


logger = LogManger().get_logger(__name__)


if __name__ == '__main__':
    logger.info("Welcome to SuperPos system ....")
    start_app()
