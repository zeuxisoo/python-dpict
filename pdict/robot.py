#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
from os import path
from urllib import quote_plus
from urllib2 import urlopen
from mimetypes import guess_type
from pyquery import PyQuery as pq
from .crawlers import AlphabetGroupProducer

class Robot(object):

    def __init__(self):
        pass

    def create_database(self):
        from .models import Word
        Word.create_table()

    def alphabet_group(self, group_size):
        alphabet_list = list(string.lowercase)

        return [alphabet_list[i:i+group_size] for i in xrange(0, len(alphabet_list), group_size)]

    def run(self):
        producer = AlphabetGroupProducer(self.alphabet_group(10))
        producer.start()
