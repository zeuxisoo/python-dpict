#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import logging
from .crawlers import AlphabetListProducer

class Robot(object):

    def __init__(self):
        self.logger = self.get_logger()

    def get_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        logger_stream_handler = logging.StreamHandler()
        logger_stream_handler.setLevel(logging.DEBUG)
        logger_stream_handler.setFormatter(logger_formatter)
        logger.addHandler(logger_stream_handler)

        return logger

    def create_database(self):
        from .models import Word
        Word.create_table()

    def alphabet_list(self):
        return list(string.lowercase)

    def run(self):
        producer = AlphabetListProducer(self.logger, self.alphabet_list())
        producer.start()
