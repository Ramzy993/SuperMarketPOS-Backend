#!/usr/bin/env python3

# lib imports
from abc import ABCMeta
from sqlalchemy.ext.declarative import declarative_base


base_model = declarative_base()


class AbstractDBDriver(metaclass=ABCMeta):
    def __init__(self):
        pass

    def __del__(self):
        pass
